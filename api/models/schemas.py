from pydantic import BaseModel, Field
from typing import List


class SummarizeCommentsResponse(BaseModel):
    summary: str
    accessibility_aspects: list[str]


class Comment(BaseModel):
    comment: str = Field(
        ..., description="Comentário a ser sumarizado", example="O acesso ao local por rampa é inviável."
    )
    accessibility_aspects: list[str] = Field(
        ...,
        description="Lista de aspectos de acessibilidade do comentário",
        example=["Acessibilidade", "Usabilidade", "Desempenho"],
    )


class SummarizeCommentsRequest(BaseModel):
    comments: List[Comment] = Field(
        ..., description="Lista de comentários a serem sumarizados"
    )
    language: str = Field(..., description="Idioma do texto resumido", example="pt-BR")


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Descrição detalhada do erro")
