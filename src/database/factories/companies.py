# recebe dataframe df_ativas e df_inativas 
# ao inserir os dados do dataframe df_ativas, coluna 'ativa' será True 
# ao inserir os dados do dataframe df_inativas, coluna 'ativa' será False
# levar em conta a seguinte query e tipos de dados da tabela companies:

# cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

# # Criação da tabela contexts
# cur.execute("""
    # CREATE TABLE IF NOT EXISTS contexts (
        # id SERIAL PRIMARY KEY,
        # company_id BIGINT REFERENCES companies(id) ON DELETE CASCADE,
        # context TEXT NOT NULL,
        # embedding VECTOR(384),
        # context_type VARCHAR(50) NOT NULL
    # );
# """)
from database.connection import get_connection, close_connection
from config import connection_credentials
import pandas as pd

def insert_companies(df_ativas, df_inativas):
    """
    Insere os dados das empresas ativas e inativas na tabela 'companies'.

    Args:
        conn: Conexão ativa com o banco de dados.
        df_ativas: DataFrame com dados de empresas ativas.
        df_inativas: DataFrame com dados de empresas inativas.
    """
    conn = get_connection(connection_credentials)

    try:
        with conn.cursor() as cur:
            # Marcar se as empresas estão ativas ou não
            df_ativas['ativa'] = True
            df_inativas['ativa'] = False

            # Concatenar os dois DataFrames
            df_empresas = pd.concat(
                [df_ativas.copy().fillna(''), df_inativas.copy().fillna('')],
                ignore_index=True
            )

            insert_query = """
                INSERT INTO companies (
                    codigo, nome_empresa, cidade, bairro, estado,
                    texto, telefone, atividade, ativa
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            for _, row in df_empresas.iterrows():
                cur.execute(insert_query, (
                    int(row['codigo']),
                    row['nome_empresa'],
                    row['cidade'],
                    row['bairro'],
                    row['estado'],
                    row['texto'],
                    row['telefones'] if row['telefones'] else None,
                    row['atividades'],
                    row['ativa']
                ))

            conn.commit()
            print(f"[✔] {len(df_empresas)} empresas inseridas com sucesso na tabela 'companies'.")

    except Exception as e:
        conn.rollback()
        raise Exception(f"[✖] Erro ao inserir empresas: {e}")
    
    finally:
        close_connection(conn)
