import logging
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

logger = logging.getLogger(__name__)

class AssistantChain:
    """
    Chain do assistente virtual do Dmovel.
    Recebe uma pergunta, busca chunks relevantes no vector store
    e gera uma resposta baseada no manual do usuário.
    """

    def __init__(self, llm, retriever):
        self.llm = llm
        self.retriever = retriever
        self.output_parser = StrOutputParser()

        self.prompt_template = ChatPromptTemplate.from_messages([
            (
                "system",
                """Você é o assistente virtual do aplicativo Dmovel, um app colaborativo de acessibilidade para pessoas com deficiência.

  Sua função é responder perguntas dos usuários sobre como usar o Dmovel, baseando-se exclusivamente no conteúdo do manual fornecido abaixo. 

  REGRAS:
  1. Responda APENAS com base no conteúdo do manual abaixo. Não invente informações.
  2. Se a resposta não estiver no manual, diga no idioma da pergunta que não encontrou a informação e sugira contato pelo e-mail dmovel@ufpa.br.
  3. Detecte o idioma da pergunta do usuário e responda INTEGRALMENTE nesse idioma.
  4. Se a pergunta for em alemão, escreva TUDO em alemão — traduza os nomes dos botões, menus e termos do aplicativo. Nunca deixe palavras em português numa resposta em alemão.
  5. Se a pergunta for em inglês, escreva TUDO em inglês — traduza os nomes dos botões e menus.
  6. Se a pergunta for em francês, escreva TUDO em francês — traduza os nomes dos botões e menus.
  7. Seja claro, objetivo e amigável.
  8. Quando relevante, inclua o passo a passo da funcionalidade.
  9. Não inclua termos originais em português entre parênteses nas respostas em alemão ou inglês. Traduza diretamente sem mostrar o original.
  10. Nunca misture idiomas na mesma resposta.
  11. Nunca mencione que está consultando um "manual" ou "documento". Responda como se o conhecimento fosse seu, de forma natural.

  CONTEÚDO DO MANUAL:
  {context}
  """
            ),
            ("human", "{question}")
        ])

        self.chain = (
            {
                "context": self.retriever | self._format_docs,
                "question": RunnablePassthrough()
            }
            | self.prompt_template
            | self.llm
            | self.output_parser
        )
    
    def _format_docs(self, docs):
        """Formata os chunks recuperados em um único texto."""
        return "\n\n".join(doc.page_content for doc in docs)

    async def answer(self, question: str) -> str:
        """
        Recebe uma pergunta e retorna a resposta do assistente.

        Args: 
            question: Pergunta do usuário em linguagem natural

        Returns:
            Resposta gerada pelo assistente
        """
        try:
            logger.debug(f"Pergunta recebida: {question}")
            result = await self.chain.ainvoke(question)
            logger.debug(f"Resposta gerada: {result[:100]}...")
            return result
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {e}")
            raise 