from pydantic import BaseModel, Field
from typing import List


class SummarizeCommentsResponse(BaseModel):
    """Resposta da sumarização de comentários."""

    summary: str = Field(
        ...,
        description="Texto resumido coeso integrando todos os comentários",
        example="O local apresenta boa acessibilidade arquitetônica com rampas e elevadores, mas carece de sinalização em braile."
    )
    accessibility_aspects: list[str] = Field(
        ..., 
        description="Lista de aspectos de acessibilidade identificados nos comentários",
        example=["Arquitetônica", "Comunicacional"]
    )

    class Config: 
        json_schema_extra = {
            "example": {
                "summary": "O local é bem avaliado pela acessibilidade física, com rampas adequadas e banheiros adaptados. O atendimento é elogiado, mas falta sinalização tátil.",
                "accessibility_aspects": ["Arquitetônica", "Atitudinal", "Comunicacional"]
            }
        }


class Comment(BaseModel):
    """Estrutura de um comentário individual sobre acessibilidade."""
    
    comment: str = Field(
        ..., 
        description="Texto do comentário descrevendo experiência de acessibilidade no local", 
        min_length=1,
        max_length=1000,
        example="O acesso ao local por rampa é inviável devido à inclinação excessiva."
    )
    accessibility_aspects: list[str] = Field(
        ...,
        description="Aspectos de acessibilidade mencionados no comentário",
        min_items=1,
        example=["Arquitetônica", "Mobilidade"]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "comment": "Rampa de acesso muito íngreme, dificultando para cadeirantes.",
                "accessibility_aspects": ["Arquitetônica"]
            }
        }


class SummarizeCommentsRequest(BaseModel):
    """Requisição para sumarização de comentários."""

    comments: List[Comment] = Field(
        ..., 
        description="Lista de comentários a serem sumarizados",
        min_items=1,
        max_items=50, 
        example=[
            {
                "comment": "Rampa de acesso muito íngreme",
                "accessibility_aspects": ["Arquitetônica"]
            },
            {
                "comment": "Atendimento excelente e atencioso",
                "accessibility_aspects": ["Atitudinal"]
            }
        ]
    )
    language: str = Field(
        ..., 
        description="Código do idioma desejado para o resumo", 
        pattern="^(pt-BR|en|de|fr)$",
        example="pt-BR"
    )

    class Config:
        json_schema_extra={
            "example": {
                "comments": [
                    {
                        "comment": "Rampa muito íngreme, difícil para cadeirantes",
                        "accessibility_aspects": ["Arquitetônica"]
                    },
                    {
                        "comment": "Equipe muito atenciosa e prestativa",
                        "accessibility_aspects": ["Atitudinal"]
                    },
                    {
                        "comment": "Falta sinalização em braile no elevador",
                        "accessibility_aspects": ["Comunicacional"]
                    }
                ],
                "language": "pt-BR"
            }
        }


class ErrorResponse(BaseModel):
    """Estrutura padrão de resposta de erro."""

    detail: str = Field(
        ..., 
        description="Descrição detalhada do erro",
        example="field required: language"
    )

class AssistantRequest(BaseModel):
    question: str = Field(
        ..., description="Pergunta do usuário ao assistente virtual", example="Como faço para avaliar um local?"
    )

class AssistantResponse(BaseModel):
    answer: str = Field(..., description="Resposta gerada pelo assistente virtual")