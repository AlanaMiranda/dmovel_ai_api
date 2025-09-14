FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Expor a porta ${API_PORT}
EXPOSE ${API_PORT}

# Comando para iniciar a aplicação em modo de produção
# Usar 0.0.0.0 para permitir acesso externo, mas com IPs confiáveis restritos
CMD ["uvicorn", "wsgi:app", "--host", "0.0.0.0", "--port", "${API_PORT}", "--workers", "4", "--proxy-headers", "--forwarded-allow-ips", "127.0.0.1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"] 

