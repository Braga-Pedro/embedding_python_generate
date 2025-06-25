# receber conexão com o banco de dados
# criar tabela companies com colunas:
#    id → big_integer
#    codigo → big_integer
#    nome_empresa → string(300)
#    cidade → string(100)
#    bairro → string(150)
#    estado → enum(string(2)) [RN, PB, CE… todas as siglas dos estados brasileiros]
#    texto → text
#    telefone → string(425) | nullable
#    atividade → string(512)

from database.connection import get_connection, close_connection
from config import connection_credentials

def create_companies_table():
    """
    Cria a tabela 'companies' no banco de dados PostgreSQL.

    Args:
        conn (psycopg2.connection): Conexão ativa com o banco de dados.
    """

    conn = get_connection(connection_credentials)

    try:
        with conn.cursor() as cur:
            # Criação do tipo ENUM para estado, se ainda não existir
            cur.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'estado_enum') THEN
                        CREATE TYPE estado_enum AS ENUM (
                            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
                            'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
                            'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
                        );
                    END IF;
                
                    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'status_enum') THEN
                        CREATE TYPE status_enum AS ENUM ('pendente', 'ok', 'erro');
                    END IF;
                END
                $$;
            """)

            # Criação da tabela companies
            cur.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                    id BIGSERIAL PRIMARY KEY,
                    codigo BIGINT NOT NULL,
                    nome_empresa VARCHAR(300) NOT NULL,
                    cidade VARCHAR(100) NOT NULL,
                    bairro VARCHAR(150) NOT NULL,
                    estado estado_enum NOT NULL,
                    texto TEXT NOT NULL,
                    telefone VARCHAR(425),
                    atividade VARCHAR(512) NOT NULL,
                    ativa BOOLEAN NOT NULL,
                    embedding_status_activity status_enum DEFAULT 'pendente',
                    embedding_status_text status_enum DEFAULT 'pendente',
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW(),
                    deleted_at TIMESTAMP DEFAULT NULL
                );
            """)

            # 3. Criar função de trigger para atualizar o campo updated_at
            cur.execute("""
                CREATE OR REPLACE FUNCTION update_updated_at_column()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.updated_at = NOW();
                    RETURN NEW;
                END;
                $$ language 'plpgsql';
            """)

            # 4. Criar trigger associada à tabela companies
            cur.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_trigger WHERE tgname = 'set_updated_at_trigger'
                    ) THEN
                        CREATE TRIGGER set_updated_at_trigger
                        BEFORE UPDATE ON companies
                        FOR EACH ROW
                        EXECUTE FUNCTION update_updated_at_column();
                    END IF;
                END;
                $$;
            """)

            conn.commit()
            print("[✔] Tabela 'companies' criada com sucesso.")

    except Exception as e:
        conn.rollback()
        raise Exception(f"[✖] Erro ao criar tabela 'companies': {e}")
    
    finally:
        close_connection(conn)
