from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import logging
from contextlib import asynccontextmanager

from api.routes.router import routes
from api.services.gemini_service import GeminiService

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialização
    try:
        # Inicializa o GeminiService e armazena no app.state
        app.state.gemini_service = GeminiService()
        app.state.logger.info("GeminiService inicializado com sucesso")

    except Exception as e:
        app.state.logger.error(f"Erro ao inicializar pool de conexões: {str(e)}")
        raise
    
    yield
    
    # Encerramento
    app.state.logger.info("Encerrando GeminiService")
    app.state.gemini_service.close()
    app.state.logger.info("GeminiService encerrado")

def create_api(config_name):

    # Definir o nível de log baseado no ambiente
    log_level = logging.INFO if config_name == "production" else logging.DEBUG

    # Configuração correta do logging
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],  # Envia logs para stdout
    )
    
    app = FastAPI(
        title="API para servir modelos de IA para a aplicação DMóvel",
        description="Esta API serve rotas para a aplicação DMóvel que utilizam modelos de IA, tanto para tradução, geração de resumos, etc.",
        version="1.0.0",
        lifespan=lifespan
    )

    # Handler global para padronizar erros 422 (validação)
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc: RequestValidationError):
        try:
            errors = exc.errors() or []
            messages = []
            for err in errors:
                loc = " -> ".join(str(x) for x in err.get("loc", []))
                msg = err.get("msg", "Erro de validação")
                messages.append(f"{loc}: {msg}")
            detail = "; ".join(messages) if messages else "Erro de validação nos dados de entrada"
        except Exception:
            detail = "Erro de validação nos dados de entrada"
        return JSONResponse(status_code=422, content={"detail": detail})

    # Adicionar o middleware CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Lista de origens permitidas
        allow_credentials=True,
        allow_methods=["*"],  # Permite todos os métodos HTTP
        allow_headers=["*"],  # Permite todos os headers
    )

    # Redireciona a rota raiz (/) para a documentação Swagger (/docs)
    @app.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/docs")

    # Criar logger principal da API e armazenar em `app.state`
    app.state.logger = logging.getLogger("api")
    app.state.logger.setLevel(log_level)
    app.state.logger.info(f"API iniciada no ambiente: {config_name}")

    # Registrar as rotas
    try:
        for route in routes:
            app.include_router(route, prefix="")
        app.state.logger.info(f"Routers registrados com sucesso: {len(routes)} routers")
    except Exception as e:
        app.state.logger.error(f"Erro ao registrar routers: {str(e)}")
        raise

    return app
