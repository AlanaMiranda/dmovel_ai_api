import json
import logging
from typing import Dict, Any, List, Union
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from api.models.schemas import SummarizeCommentsResponse, Comment

# Configuração do logger
logger = logging.getLogger(__name__)


class SummarizeCommentsChain:
    """
    Langchain para sumarizar os comentários baseado no prompt do usuário.
    """

    def __init__(self, llm, language):
        """
        Inicializa a chain de sumarização de comentários.

        Args:
            llm: Instância do modelo de linguagem (Gemini)
        """
        self.llm = llm
        self.language = language
        self.output_parser = PydanticOutputParser(
            pydantic_object=SummarizeCommentsResponse
        )

        # Template do prompt para sumarização de comentários
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
Você é um especialista em acessibilidade e análise de feedback de usuários. Sua tarefa é criar um resumo detalhado e conciso sobre a acessibilidade de um local, baseado nos comentários fornecidos.

O seu foco principal é identificar e sumarizar os pontos de **acessibilidade** e **atitude atitudinal**, tanto os positivos quanto os negativos.

Considere as seguintes áreas de acessibilidade:
- **Acessibilidade arquitetônica:** Rampas, elevadores, banheiros adaptados, piso tátil, corredores largos, etc.
- **Acessibilidade comunicacional:** Informações em formatos acessíveis (libras, braile, áudio-descrição), comunicação clara, equipe que sabe como se comunicar com pessoas com deficiência.
- **Acessibilidade atitudinal:** A forma como a equipe ou outras pessoas no local tratam e interagem com pessoas com deficiência. Gentileza, paciência, disponibilidade para ajudar, inclusão.
- **Acessibilidade tecnológica:** Sites, aplicativos ou sistemas adaptados (fontes ampliadas, leitores de tela).

INSTRUÇÕES IMPORTANTES:
1. Analise cuidadosamente todos os comentários em busca de menções a qualquer um dos tipos de acessibilidade listados acima.
2. Crie um resumo único, coeso e claro. Não liste os comentários um a um.
3. A resposta deve ser redigida no estilo de um comentário de usuário, mas com a autoridade de uma análise completa dos feedbacks existentes.
4. O resumo deve ser objetivo e direto. Não use jargões e evite informações irrelevantes para o tema.
5. Mencione tanto os pontos fortes quanto as fraquezas da acessibilidade do local, baseando-se no que foi dito nos comentários.
6. A resposta deve ser no idioma {language}.
7. A resposta deve ter entre 100 e 200 palavras.

EXEMPLOS DE RESPOSTA (apenas para referência, não copie):
- "A equipe é muito atenciosa e prestativa, o que torna a experiência mais acolhedora. No entanto, muitos comentários apontam a falta de rampas de acesso e banheiros adaptados, dificultando a locomoção."
- "O local tem uma boa estrutura, com elevadores e banheiros acessíveis, mas a comunicação é um ponto a ser melhorado. Alguns usuários relataram que a equipe não estava preparada para auxiliar pessoas com deficiência auditiva."

FORMATO DE RESPOSTA:
{format_instructions}
""",
                ),
                ("human", "Sumarize os comentários: {comments}"),
            ]
        )

        # Cria a chain
        self.chain = self.prompt_template | self.llm | self.output_parser

    def _safe_get(
        self, obj: Union[Dict[str, Any], Comment], field_name: str, default: Any = None
    ) -> Any:
        """
        Obtém um campo de um dict ou de um modelo Pydantic `Comment` de forma segura.

        Args:
            obj: Dicionário ou instância de `Comment`
            field_name: Nome do campo a obter
            default: Valor padrão caso o campo não exista

        Returns:
            Valor do campo solicitado
        """
        # Se for dict
        if isinstance(obj, dict):
            return obj.get(field_name, default)

        # Se for Pydantic v2 (tem model_dump)
        if hasattr(obj, "model_dump"):
            data = obj.model_dump()
            return data.get(field_name, default)

        # Fallback para atributo
        return getattr(obj, field_name, default)

    def _format_comments(self, comments: List[Union[Dict[str, Any], Comment]]) -> str:
        """
        Formata a informação dos comentários para o prompt.

        Args:
            comments: Lista de dicionários com informações dos comentários

        Returns:
            String formatada com informações dos relatórios
        """

        formatted_comments = []

        for i, comment in enumerate(comments, 1):
            comment_info = f"""
{i}. COMENTÁRIO: {self._safe_get(comment, 'comment', 'N/A')}
    ASPECTOS DE ACESSIBILIDADE: {self._safe_get(comment, 'accessibility_aspects', 'N/A')}
"""
            formatted_comments.append(comment_info)

        return "\n".join(formatted_comments)

    async def summarize_comments(
        self, comments: List[Union[Dict[str, Any], Comment]]
    ) -> SummarizeCommentsResponse:
        """
        Seleciona o relatório mais adequado baseado no prompt do usuário.

        Args:
            comments: Lista de dicionários com informações dos comentários

        Returns:
            SummarizeCommentsResponse com o texto resumido e os aspectos de acessibilidade

        Raises:
            Exception: Em caso de erro na sumarização
        """
        try:
            # Formatar informações dos comentários
            comments_list = self._format_comments(comments)

            if not comments_list:
                logger.error("Nenhum comentário encontrado")
                raise Exception("Nenhum comentário disponível para sumarização")

            # Preparar inputs para a chain
            inputs = {
                "comments": comments_list,
                "language": self.language,
                "format_instructions": self.output_parser.get_format_instructions(),
            }

            # Executar a chain
            logger.debug(
                f"Iniciando sumarização de comentários: {comments_list[:10]}..."
            )
            print(inputs)
            result = await self.chain.ainvoke(inputs)

            # A resposta já é um SummarizeCommentsResponse via PydanticOutputParser
            summary = result.summary
            accessibility_aspects = result.accessibility_aspects

            logger.debug(f"Resumo gerado: {summary}")
            return SummarizeCommentsResponse(
                summary=summary,
                accessibility_aspects=accessibility_aspects,
            )

        except Exception as e:
            logger.error(f"Erro na sumarização de comentários: {e}")
            raise Exception(f"Erro ao sumarizar comentários: {str(e)}")
