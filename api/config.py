import os
from dotenv import load_dotenv

load_dotenv() # Carrega as variáveis de ambiente do arquivo .env

class Settings:
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "") # Chave da API do Google para usar o Gemini
    MODEL_NAME: str = os.getenv("MODEL_NAME", "") # Nome do modelo do Gemini que será usado

    """
    Dados do banco do DMóvel...
    """ 

settings = Settings()