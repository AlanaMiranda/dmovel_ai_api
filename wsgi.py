from api import create_api
from api.config import settings

# Usar configurações centralizadas
config_name = settings.ENVIRONMENT
port = settings.API_PORT
# Criar a aplicação
app = create_api(config_name)

# Para compatibilidade com WSGI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=port) 