from fastapi import APIRouter, Request, HTTPException, status
import logging
from api.models.schemas import AssistantRequest, AssistantResponse, ErrorResponse
 

logger = logging.getLogger(__name__)

router = APIRouter(tags=["assistant"])

@router.post(
    "/chat/support",
    response_model=AssistantResponse,
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
    summary="Assistente virtual do Dmovel",
    description="Responde perguntas sobre como usar o Dmovel baseando-se no manual do usuário.",
)
async def chat_support(request: AssistantRequest, fastapi_request: Request):
    """
    Recebe uma pergunta do usuário e retorna uma resposta baseada no manual do DMovel.

    Args:
        request: Dados da requisição contendo a pergunta
        fastapi_request: Objeto Request do FastAPI para acessar app.state

    Returns:
        AssistantResponse com a resposta gerada pelo assistente
    """
    try:
        gemini_service = fastapi_request.app.state.gemini_service
        vector_store_service = fastapi_request.app.state.vector_store_service

        if not gemini_service or not hasattr(gemini_service, 'llm'):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Serviço Gemini não disponível"
            )
        assistant_chain = fastapi_request.app.state.assistant_chain

        answer = await assistant_chain.answer(request.question)
        logger.debug(f"Resposta gerada para: {request.question[:50]}...")
        return AssistantResponse(answer=answer)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro inesperado no assistente virtual: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar pergunta. Tente novamente."
        )
