# pega o csv do diretório ../../../data/empresas_ativas.csv && ../../../data/empresas_inativas.csv
# este metodo vai ser utilizado para pegar o csv que será utilizado por data_formatter.py para formatar/limpar os dados do csv


import pandas as pd

def load_csv_data(path_ativa, path_inativa):
    """
    Carrega os arquivos CSV de empresas ativas e inativas.

    Retorna:
        tuple: (df_empresas_ativas, df_empresas_inativas)
    """

    if not path_ativa or not path_inativa:
        raise FileNotFoundError("Caminhos para os arquivos CSV não definidos no .env")

    try:
        df_ativas = pd.read_csv(path_ativa, encoding="utf-8").drop_duplicates()
        df_inativas = pd.read_csv(path_inativa, encoding="utf-8").drop_duplicates()
        
        df_ativas.columns = [col.lower() for col in df_ativas.columns]
        df_inativas.columns = [col.lower() for col in df_inativas.columns]
        
        print(df_ativas.head())
        print(df_inativas.head())

        print(f"[✔] CSVs carregados com sucesso:\n - Ativas: {len(df_ativas)} linhas\n - Inativas: {len(df_inativas)} linhas")
        return df_ativas, df_inativas

    except FileNotFoundError as e:
        raise FileNotFoundError(f"[✖] Arquivo CSV não encontrado: {e}")
    except Exception as e:
        raise Exception(f"[✖] Erro ao carregar CSVs: {e}")
