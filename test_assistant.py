import asyncio
from api.services.gemini_service import GeminiService
from api.services.vector_store_service import VectorStoreService
from api.chain.assistant_chain import AssistantChain

gemini = GeminiService()
vs = VectorStoreService()
vs.build()

chain = AssistantChain(llm=gemini.llm, retriever=vs.get_retriever())

async def test():
    perguntas = [
        "Como faço para avaliar um local?",
        "How do I change the app language?",
        "Was ist ein POI",
    ]
    for pergunta in perguntas:
        print(f"\nPergunta: {pergunta}")
        resposta = await chain.answer(pergunta)
        print(f"Resposta: {resposta}")

asyncio.run(test())