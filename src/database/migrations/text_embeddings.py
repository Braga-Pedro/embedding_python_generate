from database.utils.connections import get_connection, close_connection
from config import connection_credentials

def create_text_embeddings_table():
    
    conn = get_connection(connection_credentials)

    try:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

            cur.execute("""
                CREATE TABLE IF NOT EXISTS text_embeddings (
                    id SERIAL PRIMARY KEY,
                    company_id BIGINT REFERENCES companies(id) ON DELETE CASCADE,
                    embedding VECTOR(2560),
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW(),
                    deleted_at TIMESTAMP DEFAULT NULL
                );
            """)

            cur.execute("""
                CREATE OR REPLACE FUNCTION update_updated_at_column()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.updated_at = NOW();
                    RETURN NEW;
                END;
                $$ language 'plpgsql';
            """)

            cur.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_trigger WHERE tgname = 'set_updated_at_trigger'
                    ) THEN
                        CREATE TRIGGER set_updated_at_trigger
                        BEFORE UPDATE ON text_embeddings
                        FOR EACH ROW
                        EXECUTE FUNCTION update_updated_at_column();
                    END IF;
                END;
                $$;
            """)

            conn.commit()
            print("[✔] Tabela 'text_embeddings' criada com sucesso.")

    except Exception as e:
        conn.rollback()
        raise Exception(f"[✖] Erro ao criar tabela 'text_embeddings': {e}")
    
    finally:
        close_connection(conn)
