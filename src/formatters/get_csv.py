import pandas as pd

def load_csv_data(path_ativa, path_inativa):

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
