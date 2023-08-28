# Use a imagem oficial do Python como imagem base
FROM python:3.11

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o contêiner
COPY requirements.txt .

# Instale as dependências
RUN pip install -r requirements.txt

# Copiar o arquivo app_v2.py para o contêiner
COPY app_v2.py .
# Copiar o arquivo .env para o contêiner
COPY .env .

# Comando para iniciar a aplicação
CMD ["python", "app_v2.py"]
