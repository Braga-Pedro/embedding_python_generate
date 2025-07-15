import requests
from psycopg2.extras import execute_values
from database.utils.connections import get_connection, close_connection
from config import connection_credentials
from bs4 import BeautifulSoup
import html
from time import sleep

MODEL_NAME = "phi"
SLEEP_SECONDS = 0.1

def generate_activity_embeddings(ollama_endpoint):
    conn = get_connection(connection_credentials)

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, atividade, nome_empresa
                FROM companies
                WHERE embedding_status_activity IS NULL OR embedding_status_activity != 'ok'
            """)
            companies = cur.fetchall()

        print(f"[i] Total de empresas para processar (atividades): {len(companies)}")

        all_contexts = []

        for idx, (company_id, atividade, nome_empresa) in enumerate(companies, start=1):
            atividades = [a.strip() for a in atividade.replace(";", ",").split(",") if a.strip()]
            if not atividades:
                continue

            atividades_texto = ', '.join(atividades)
            prompt = f"{normalize_text(nome_empresa)}: {normalize_text(atividades_texto)}"

            try:
                embedding = get_embedding_single(prompt, ollama_endpoint)
                all_contexts.append((company_id, embedding))

                print(f"[✓] Embedding gerado para empresa {idx}/{len(companies)}")

            except Exception as e:
                print(f"[X] Erro ao gerar embedding de atividades para empresa {company_id}: {e}")

        if all_contexts:
            with conn.cursor() as cur:
                execute_values(
                    cur,
                    """
                    INSERT INTO activity_embeddings (company_id, embedding)
                    VALUES %s
                    """,
                    all_contexts
                )
                conn.commit()

                ids_ok = [cid for cid, _ in all_contexts]
                cur.execute("""
                    UPDATE companies
                    SET embedding_status_activity = 'ok'
                    WHERE id = ANY(%s)
                """, (ids_ok,))
                conn.commit()

            print(f"[✓] {len(all_contexts)} embeddings de atividades inseridos com sucesso.")

    except Exception as e:
        conn.rollback()
        print(f"[X] Erro geral no processamento de atividades: {e}")
    finally:
        close_connection(conn)

# ---------- UTILS ----------

def normalize_text(raw_text):
    text = BeautifulSoup(raw_text or '', "html.parser").get_text()
    text = html.unescape(text)
    return ' '.join(text.split())

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

