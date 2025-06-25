from dotenv import load_dotenv
import os

from database.validation import validate_tables
from formatters.get_csv import load_csv_data
# from sqlalchemy import create_engine

# Carrega variáveis de ambiente
load_dotenv()

# Caminho absoluto para a raiz do projeto com base neste arquivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminhos relativos do .env
relative_path_ativas = os.getenv("CSV_EMPRESA_ATIVA_PATH")
relative_path_inativas = os.getenv("CSV_EMPRESA_INATIVA_PATH")

# Converte os caminhos relativos em absolutos com base em main.py
CSV_PATH_EMPRESAS_ATIVAS = os.path.abspath(os.path.join(BASE_DIR, relative_path_ativas))
CSV_PATH_EMPRESAS_INATIVAS = os.path.abspath(os.path.join(BASE_DIR, relative_path_inativas))

def main():
        print("[⚠] Dados ausentes. Executando o pipeline de ingestão...")    

        # Carrega os arquivos CSV
        print("path ativas:", CSV_PATH_EMPRESAS_ATIVAS)
        print("path inativas:", CSV_PATH_EMPRESAS_INATIVAS)
        df_ativas, df_inativas = load_csv_data(CSV_PATH_EMPRESAS_ATIVAS, CSV_PATH_EMPRESAS_INATIVAS)
        
        # Exibe o conteúdo dos DataFrames
        print("Empresas Ativas:")
        print(df_ativas.head())  # Mostra as primeiras linhas

        print("\nEmpresas Inativas:")
        print(df_inativas.head())

        # Exemplo de normalização e limpeza (ajuste conforme necessário)
        # df_ativas.columns = [col.strip().lower() for col in df_ativas.columns]
        # df_inativas.columns = [col.strip().lower() for col in df_inativas.columns]

        # df_ativas = df_ativas.drop_duplicates()
        # df_inativas = df_inativas.drop_duplicates()

        # # Inserção no banco de dados usando pandas e sqlalchemy

        # db_url = f"postgresql://{connection_credentials['user']}:{connection_credentials['password']}@{connection_credentials['host']}:{connection_credentials['port']}/{connection_credentials['database']}"
        # engine = create_engine(db_url)

        # # Supondo que as tabelas já existem e têm os mesmos nomes dos arquivos (sem extensão)
        # df_ativas.to_sql('empresas_ativas', engine, if_exists='append', index=False)
        # df_inativas.to_sql('empresas_inativas', engine, if_exists='append', index=False)

        # print("[✔] Dados inseridos com sucesso no banco de dados.")

if __name__ == '__main__':
    main()