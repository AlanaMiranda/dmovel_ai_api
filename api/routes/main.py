from fastapi import APIRouter, Request, HTTPException
from typing import Dict
import logging

# Configuração do logger
logger = logging.getLogger(__name__)

router = APIRouter(tags=["main"])


@router.get(
    "/health-check",
    response_model=Dict[str, str],
    summary="Verifica a saúde da API",
    description="Endpoint de verificação de saúde que retorna o status atual da API.",
)
async def health_check(request: Request):
    """
    Verifica a saúde da API.

    Returns:
        Dict[str, str]: Dicionário contendo:
            - status (str): Status atual da API
            - message (str): Mensagem descritiva do status

    Raises:
        HTTPException: Em caso de erro interno do servidor
    """
    # Verifica se o GeminiService está funcionando
    if not request.app.state.gemini_service.is_working():
        raise HTTPException(status_code=500, detail="GeminiService is not working.")

    return {"status": "ok", "message": "API is running and healthy."}
