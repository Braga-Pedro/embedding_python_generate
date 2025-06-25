# faz conexão com o banco de dados PostgreSQL usando psycopg2
# carrega as variáveis de ambiente do arquivo .env 
# e retorna a conexão para ser usada em outros scripts

import psycopg2

def get_connection(credentials):
    """
    Estabelece uma conexão com o banco de dados PostgreSQL.

    Retorna:
        conn (psycopg2.connection): Conexão ativa com o banco.
    Lança:
        Exception: Em caso de falha na conexão.
    """
    print("[i] Tentando conectar ao banco de dados PostgreSQL...")

    try:
        conn = psycopg2.connect(
            host=credentials['host'],
            database=credentials['database'],
            user=credentials['user'],
            password=credentials['password'],
            port=credentials['port'],
            options='-c client_encoding=UTF8'
        )
        print("Conexão com o banco de dados estabelecida.", conn)
        return conn

    except Exception as error:
        raise Exception("Erro ao conectar ao banco de dados: ", error)

def close_connection(conn):
    """
    Fecha uma conexão PostgreSQL ativa, se existir.

    Args:
        conn (psycopg2.connection): Conexão a ser fechada.
    """
    if conn:
        conn.close()
        print("[X] Conexão com o banco de dados encerrada.")
    else:
        print("[X] Nenhuma conexão ativa para encerrar.")
