from database.utils.connections import get_connection, close_connection
from config import connection_credentials
import pandas as pd

def insert_companies(df_ativas, df_inativas):

    conn = get_connection(connection_credentials)

    try:
        with conn.cursor() as cur:
            df_ativas['ativa'] = True
            df_inativas['ativa'] = False

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
