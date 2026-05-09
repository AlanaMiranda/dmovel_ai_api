from fastapi import APIRouter, Request, HTTPException, status
from typing import Dict
import logging

from api.models.schemas import SummarizeCommentsResponse, SummarizeCommentsRequest, ErrorResponse
from api.chain.summarize_comments_chain import SummarizeCommentsChain

# Configuração do logger
logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Principal"],
    responses={
        500: {"model": ErrorResponse, "description": "Erro interno do servidor"}
    }
)


@router.get(
    "/health-check",
    response_model=Dict[str, str],
    summary="Verificação de Saúde da API",
    description="""
    Endpoint de health check que verifica se a API e seus serviços dependentes estão funcionando corretamente.
    
    Este endpoint é útil para:
    - Monitoramento de uptime
    - Load balancers verificarem disponibilidade
    - Testes automatizados de infraestrututra

    Retorna:
    - 'status': "ok" se todos os serviços estão funcionando
    - 'message':  Mensagem descritiva do status

    Códigos de resposta:
    - '200': API funcionando normalmente
    - '500': Erro interno (GeminiService indisponível)
    """,
    response_description="Status de saúde da API",
    responses={
        200: {
            "description": "API funcionando normalmente",
            "content": {
                "application/json": {
                    "example": {
                        "status": "ok",
                        "message": "API is running and healthy."
                    }
                }
            }
        },
        500: {
            "description": "Serviço de IA indisponível",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "GeminiService is not working."
                    }
                }
            }
        }
    },
    tags=["Monitoramento"]
)
async def health_check(request: Request):
    """
    Verifica a saúde da API e a disponibilidade do GeminiService.

    Args:
        request: Objeto Request do FastAPI para acessar app.state

    Returns:
        Dict contendo status e mensagem

    Raises:
        HTTPException: 500 se o GeminiService não estiver disponível
    """
    # Verifica se o GeminiService está funcionando
    if not request.app.state.gemini_service.is_working():
        raise HTTPException(status_code=500, detail="GeminiService is not working.")

    return {"status": "ok", "message": "API is running and healthy."}

# Endpoint para sumarização de comentários
@router.post(
    "/summarize-comments",
    response_model=SummarizeCommentsResponse,
    summary="Sumarização Automática de Avaliações de Acessibilidade",
    description="""
    Processa múltiplos comentários de usuários sobre um local e gera um resumo
    coeso e informativo utilizando Large Language Models (Google Gemini).

    Funcionalidades:
    - Sumarização multilíngue (português, inglês, alemão)
    - Identificação automática de aspectos de acessibilidade
    - Geração de texto narrativo único (não lista comentários individualmente)
    - Equilíbrio entre pontos positivos e negativos

    Aspectos de Acessibilidade Identificados:
    - Arquitetônica: Rampas, elevadores, banheiros adaptados, piso tátil
    - Comunicacional: Libras, braile, audiodescrição, sinalização clara
    - Atitudinal: Gentileza, inclusão, tratamento respeitoso pela equipe
    - Tecnológica: Sites, aplicativos e sistemas adaptados

    Idiomas Suportados:
    - 'pt-BR': Português do Brasil
    - 'en': Inglês
    - 'de': Alemão

    Limites:
    - Resumo gerado entre 100-200 palavras
    - Suporta até 50 comentários por requisição
    - Tempo de resposta aproximado: 2-5 segundos
    """,
    response_description="Resumo gerado e aspectos de acessibilidade identificados",
    responses={
        200: {
            "description": "Sumarização realizada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "summary": "O local apresenta excelente acessibilidade arquitetônica, com rampas bem projetadas e elevadores funcionais. O atendimento da equipe é elogiado pela gentileza e atenção às necessidades de pessoas com deficiência. Porém, a sinalização em braile é insuficiente, e o site não possui recursos de acessibilidade adequados para leitores de tela.",
                        "accessibility_aspects": [
                            "Arquitetônica",
                            "Atitudinal",
                            "Comunicacional",
                            "Tecnológica"
                        ]
                    }
                }
            }
        },
        422: {
            "model": ErrorResponse,
            "description": "Dados de entrada inválidos",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "field required: language"
                    }
                }
            }
        },
        500: {
            "model": ErrorResponse,
            "description": "Erro interno do servidor",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Erro interno ao sumarizar comentários. Tente novamente."
                    }
                }
            }
        }
    },
    tags=["Sumarização"]
)
async def summarize_comments(request: SummarizeCommentsRequest, fastapi_request: Request):
    """
    Sumariza comentários de acessibilidade usando Google Gemini via LangChain.
    
    Args:
        request: Dados da requisição (comentários e idioma)
        fastapi_request: Objeto Request para acessar app.state

    Returns:
        SummarizeCommentsResponse: Resumo e aspectos identificados
        
    Raises:
        HTTPException: 422 para validação ou 500 para erros internos
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