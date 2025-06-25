from config import CSV_PATH_EMPRESAS_ATIVAS, CSV_PATH_EMPRESAS_INATIVAS, LLM_URL, validate_env
from database.validation import validate_tables
from formatters.get_csv import load_csv_data
from database.migrations.companies import create_companies_table
from database.migrations.text_embeddings import create_text_embeddings_table
from database.migrations.activity_embeddings import create_activity_embeddings_table
from database.factories.companies import insert_companies
from database.utils.drop_tables import drop_table
from database.embeddings.activity import generate_activity_embeddings
from database.embeddings.text import generate_text_embeddings

def main():
    validate_env()
    # Verifica se as tabelas existem e possuem dados
    if validate_tables():
        print("[✔] Dados já inseridos no banco de dados.")
    else:
        print("[⚠] Dados ausentes. Executando o pipeline de ingestão...")    
        
        drop_table()

        # Cria tabelas no banco de dados
        create_companies_table()
        create_text_embeddings_table()
        create_activity_embeddings_table()

        # Carrega os arquivos CSV
        df_ativas, df_inativas = load_csv_data(CSV_PATH_EMPRESAS_ATIVAS, CSV_PATH_EMPRESAS_INATIVAS)
        insert_companies(df_ativas, df_inativas)

        generate_activity_embeddings(LLM_URL)
        generate_text_embeddings(LLM_URL)

        # drop_table()

if __name__ == '__main__':
    main()