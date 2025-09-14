import os
from api import create_api

# Determinar o ambiente baseado em variável de ambiente
config_name = os.getenv("ENVIRONMENT", "production")
port = os.getenv("API_PORT", 8000)
# Criar a aplicação
app = create_api(config_name)

# Para compatibilidade com WSGI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=port) 