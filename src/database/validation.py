# pega conexão feita em connection.py e valida se as tabelas companies e contexts existem e se já há dados inseridos nelas
# validar de forma isolada, se uma das duas tabelas não existir ou se não houver dados inseridos nelas, retornar False
# se ambas as tabelas existirem e já houver dados inseridos nelas, retornar True

from database.connection import get_connection, close_connection
from config import connection_credentials

def table_exists_and_has_data(cursor, table_name):
    """
    Verifica se uma tabela existe e contém ao menos um registro.

    Args:
        cursor (psycopg2.cursor): Cursor ativo do banco de dados.
        table_name (str): Nome da tabela a ser verificada.

    Retorna:
        bool: True se a tabela existe e possui dados, False caso contrário.
    """
    try:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name = %s
            );
        """, (table_name,))
        exists = cursor.fetchone()[0]

        if not exists:
            print(f"[!] Tabela '{table_name}' não existe.")
            return False

        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]

        if count == 0:
            print(f"[!] Tabela '{table_name}' está vazia.")
            return False

        return True

    except Exception as e:
        print(f"[✖] Erro ao validar a tabela '{table_name}': {e}")
        return False

def validate_tables():
    """
    Valida a existência e presença de dados nas tabelas 'companies' e 'contexts'.

    Retorna:
        bool: True se ambas as tabelas existem e contêm dados, False caso contrário.
    """
    # conn = None
    conn = get_connection(connection_credentials)

    try:
        cursor = conn.cursor()

        companies_ok = table_exists_and_has_data(cursor, "companies")
        activity_embeddings_ok = table_exists_and_has_data(cursor, "activity_embeddings")
        text_embeddings_ok = table_exists_and_has_data(cursor, "text_embeddings")

        return companies_ok and activity_embeddings_ok and text_embeddings_ok

    finally:
        close_connection(conn)
