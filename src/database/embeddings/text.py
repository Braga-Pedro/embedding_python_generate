import requests
import html
from psycopg2.extras import execute_values
from database.utils.connections import get_connection, close_connection
from config import connection_credentials
from bs4 import BeautifulSoup
from time import sleep

MODEL_NAME = "phi"
MAX_TEXT_LENGTH = 300
SLEEP_SECONDS = 0.1

def generate_text_embeddings(ollama_endpoint):
    conn = get_connection(connection_credentials)

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, nome_empresa, texto
                FROM companies
                WHERE embedding_status_text IS NULL OR embedding_status_text != 'ok'
            """)
            companies = cur.fetchall()

        print(f"[i] Total de empresas para processar (textos): {len(companies)}")

        for idx, (company_id, nome_empresa, texto) in enumerate(companies, start=1):
            print(f"[•] Processando empresa {idx}/{len(companies)}...")

            nome_empresa_limpo = normalize_text(nome_empresa)
            texto_limpo = normalize_text(texto)
            blocos_texto = split_large_text(texto_limpo, max_len=MAX_TEXT_LENGTH)

            embeddings_para_empresa = []

            for bloco in blocos_texto:
                prompt = f"{nome_empresa_limpo}: {bloco}"

                try:
                    embedding = get_embedding_single(prompt, ollama_endpoint)
                    embeddings_para_empresa.append((company_id, embedding))

                except Exception as e:
                    print(f"[X] Erro ao gerar embedding para empresa ID {company_id}: {e}")
                    continue

            if embeddings_para_empresa:
                with conn.cursor() as cur:
                    execute_values(
                        cur,
                        """
                        INSERT INTO text_embeddings (company_id, embedding)
                        VALUES %s
                        """,
                        embeddings_para_empresa
                    )
                    conn.commit()

                    cur.execute("""
                        UPDATE companies
                        SET embedding_status_text = 'ok'
                        WHERE id = %s
                    """, (company_id,))
                    conn.commit()

                print(f"[✓] {len(embeddings_para_empresa)} embeddings inseridos para empresa {company_id}.")

    except Exception as e:
        conn.rollback()
        print(f"[X] Erro geral no processamento de textos: {e}")
    finally:
        close_connection(conn)

# ---------- UTILS ----------

def normalize_text(raw_text):
    text = BeautifulSoup(raw_text or '', "html.parser").get_text()
    text = html.unescape(text)
    return ' '.join(text.split())

def split_large_text(text, max_len=400):
    words = text.split()
    return [' '.join(words[i:i + max_len]) for i in range(0, len(words), max_len)]

def get_embedding_single(prompt, endpoint):
    try:
        response = requests.post(
            url=f"{endpoint}/embeddings",
            json={"model": MODEL_NAME, "prompt": prompt},
            timeout=120
        )
        response.raise_for_status()
        data = response.json()
        sleep(SLEEP_SECONDS)
        return data.get("embedding")
    except Exception as e:
        raise Exception(f"Erro ao chamar API Ollama (prompt único): {e}")
