from fastapi import APIRouter, Request, HTTPException, status
from typing import Dict
import logging

from api.models.schemas import SummarizeCommentsResponse, SummarizeCommentsRequest, ErrorResponse
from api.chain.summarize_comments_chain import SummarizeCommentsChain

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

# Endpoint para sumarização de comentários
@router.post(
    "/summarize-comments",
    response_model=SummarizeCommentsResponse,
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "description": "Erro de validação nos dados de entrada",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponse,
            "description": "Erro interno do servidor",
        },
    },
    summary="Sumariza os comentários baseado no prompt do usuário",
    description="""
    Analisa os comentários e sumariza os comentários baseado nos aspectos de acessibilidade.
    Retorna o texto resumido e os aspectos de acessibilidade.
    """,
)
async def summarize_comments(request: SummarizeCommentsRequest, fastapi_request: Request):
    """
    Sumariza os comentários baseado nos aspectos de acessibilidade.
    
    Args:
        request: Dados da requisição contendo os comentários e o idioma
        fastapi_request: Objeto Request do FastAPI para acessar app.state

    Returns:
        ReportSelectionResponse: Resposta contendo o relatório selecionado e justificativa
        
    Raises:
        HTTPException: Em caso de erro na sumarização dos comentários
    """
    try:
        # Obter o serviço Gemini do app state
        gemini_service = fastapi_request.app.state.gemini_service
        if not gemini_service or not hasattr(gemini_service, 'llm'):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Serviço Gemini não disponível"
            )
        
        # Inicializar a chain de sumarização de comentários
        summarize_comments_chain = SummarizeCommentsChain(
            llm=gemini_service.llm,
            language=request.language
        )
        
        # Executar a seleção
        result = await summarize_comments_chain.summarize_comments(
            comments=request.comments
        )
        
        logger.debug(f"Comentário sumarizado: {result.summary}")
        return result
        
    except HTTPException:
        # Re-raise HTTPExceptions
        raise
    except Exception as e:
        # Log do erro e retorno de erro genérico
        logger.error(f"Erro inesperado na sumarização de comentários: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao sumarizar comentários. Tente novamente."
        )