# services/gemini_service.py
import os
import logging
from api.config import settings
from langchain_google_genai import ChatGoogleGenerativeAI
from api.config import Settings

"""
Serviço para interagir com o modelo de IA do Gemini
"""

# Configuração do logger
logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.settings = Settings()
        self.model_name = self.settings.MODEL_NAME
        self.google_api_key = self.settings.GOOGLE_API_KEY

        try:
            os.environ["GOOGLE_API_KEY"] = self.google_api_key
            # Configura o modelo Gemini
            self.llm = ChatGoogleGenerativeAI(
                model=self.model_name,
                temperature=0.1
            )
        except Exception as e:
            logger.error(f"Erro ao inicializar GeminiService: {e}")
            raise
    
    def is_working(self):
        """
        Verifica se o serviço Gemini está funcionando
        """
        return bool(self.llm)

    def get_model_name(self):
        return self.model_name
    
    def close(self):
        """
        Método para encerrar o serviço e limpar recursos
        """
        pass