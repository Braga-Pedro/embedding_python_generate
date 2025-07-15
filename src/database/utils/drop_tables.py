from database.utils.connections import get_connection, close_connection
from config import connection_credentials

def drop_table():
    conn = get_connection(connection_credentials)
    with conn.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS companies CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS activity_embeddings CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS text_embeddings CASCADE;")
    
    conn.commit()
    close_connection(conn)

    print("[✔] Tabelas 'activity_embeddings', 'text_embeddings' e 'companies' removidas com sucesso.")