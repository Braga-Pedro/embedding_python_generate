from config import CSV_PATH_EMPRESAS_ATIVAS, CSV_PATH_EMPRESAS_INATIVAS, LLM_URL, validate_env
from database.validation import validate_tables
from formatters.get_csv import load_csv_data
from database.migrations.companies import create_companies_table
from scripts.database.migrations.contexts_deprecated import create_contexts_table
from database.factories.companies import insert_companies
from database.utils.drop_tables import drop_table

def main():
    validate_env()
    # Verifica se as tabelas existem e possuem dados
    if validate_tables():
        print("[✔] Dados já inseridos no banco de dados.")
    else:
        print("[⚠] Dados ausentes. Executando o pipeline de ingestão...")    

        # Cria tabelas no banco de dados
        create_companies_table()
        create_contexts_table()

        # Carrega os arquivos CSV
        df_ativas, df_inativas = load_csv_data(CSV_PATH_EMPRESAS_ATIVAS, CSV_PATH_EMPRESAS_INATIVAS)
        # Insere os dados na tabela companies
        insert_companies(df_ativas, df_inativas)

        drop_table()

if __name__ == '__main__':
    main()