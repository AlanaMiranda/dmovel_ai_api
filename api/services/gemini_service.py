# services/gemini_service.py

from api.config import Settings

"""
Serviço para interagir com o modelo de IA do Gemini
"""

class GeminiService:
    def __init__(self):
        self.settings = Settings()
        self.model_name = self.settings.MODEL_NAME
        self.google_api_key = self.settings.GOOGLE_API_KEY

    def is_working(self):
        return True

    def get_model_name(self):
        return self.model_name
    
    def close(self):
        """
        Método para encerrar o serviço e limpar recursos
        """
        pass