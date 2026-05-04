import logging 
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from langchain_chroma import Chroma
from api.config import settings

logger = logging.getLogger(__name__)

KNOWLEDGE_PATH = "knowledge/manual_dmovel.md"
CHROMA_PATH = "chroma_db"

class VectorStoreService:
    def __init__(self):
        os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )
        self.vector_store = None

    def build(self):
        """
        Carrega o manual, divide em chuncks e cria o vector store.
        Executado uma vez na inicialização da aplicação.
        """
        try:
            logger.info("Carregando manual do Dmovel...")
            loader = UnstructuredMarkdownLoader (KNOWLEDGE_PATH)
            documents = loader.load()

            logger.info("Dividindo em chunks...")
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            chunks = splitter.split_documents(documents)
            logger.info(f"{len(chunks)} chunks gerados.")

            logger.info("Criando vector store...")
            self.vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=CHROMA_PATH
            )
            logger.info("Vector store criado com sucesso.")
        
        except Exception as e:
            logger.error(f"Erro ao criar vector store: {e}")
            raise
    def get_retriever(self):
        """
        Retorna o retriever para busca de chunks relevantes.
        """
        if not self.vector_store:
            raise Exception("Vector store não inicializado. Execute build() primeiro.")
        return self.vector_store.as_retriever(search_kwargs={"k": 4})