import psycopg2

def get_connection(credentials):

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
    if conn:
        conn.close()
        print("[X] Conexão com o banco de dados encerrada.")
    else:
        print("[X] Nenhuma conexão ativa para encerrar.")
