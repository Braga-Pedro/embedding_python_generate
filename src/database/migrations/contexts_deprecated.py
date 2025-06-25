# pegar conexão com o banco de dados
# se não existir, criar tabela contexts com colunas:
#   id → serial
#   context → text
#   embedding → vector(306) # olhar tamanho do embedding do modelo phi-2

from database.connection import get_connection, close_connection
from config import connection_credentials

def create_contexts_table():
    """
    Cria a tabela 'contexts' no banco de dados PostgreSQL para armazenar embeddings de texto.
    """
    conn = get_connection(connection_credentials)

    try:
        with conn.cursor() as cur:
            # Extensão vector (pgvector) necessária para embeddings
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

            # Criação da tabela contexts
            cur.execute("""
                CREATE TABLE IF NOT EXISTS contexts (
                    id SERIAL PRIMARY KEY,
                    company_id BIGINT REFERENCES companies(id) ON DELETE CASCADE,
                    context TEXT NOT NULL,
                    text_embedding VECTOR(512),
                    activity_embedding VECTOR(512),
                );
            """)

            conn.commit()
            print("[✔] Tabela 'contexts' criada com sucesso.")

    except Exception as e:
        conn.rollback()
        raise Exception(f"[✖] Erro ao criar tabela 'contexts': {e}")
    
    finally:
        close_connection(conn)
