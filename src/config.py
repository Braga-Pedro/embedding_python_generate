import os
from dotenv import load_dotenv

load_dotenv()

connection_credentials = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_DATABASE"),
    "user": os.getenv("DB_USERNAME"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT", 5432)
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
relative_path_ativas = os.getenv("CSV_EMPRESA_ATIVA_PATH")
relative_path_inativas = os.getenv("CSV_EMPRESA_INATIVA_PATH")

CSV_PATH_EMPRESAS_ATIVAS = os.path.abspath(os.path.join(BASE_DIR, relative_path_ativas))
CSV_PATH_EMPRESAS_INATIVAS = os.path.abspath(os.path.join(BASE_DIR, relative_path_inativas))

LLM_URL = os.getenv("LLM_URL")

def validate_env():
    required_vars = [
        "DB_HOST", "DB_DATABASE", "DB_USERNAME", "DB_PASSWORD", "DB_PORT",
        "CSV_EMPRESA_ATIVA_PATH", "CSV_EMPRESA_INATIVA_PATH", "LLM_URL"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    print("All required environment variables are set.")