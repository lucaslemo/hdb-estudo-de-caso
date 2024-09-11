# Imagem base oficial do Python
FROM python:3.9.20-slim

# Diretório de trabalho dentro do container
WORKDIR /var/www/app

# Copia o arquivo de requisitos para o diretório de trabalho
COPY ../../../requirements.txt .

# Instala as dependências do arquivo de requisitos
RUN pip install --no-cache-dir -r requirements.txt

# Instala o python-dotenv para carregar as variáveis de ambiente 
RUN pip install --no-cache-dir python-dotenv

# Instala o gunicorn para o servidor http
RUN pip install --no-cache-dir gunicorn

# Copia o código do projeto para o container
COPY ./todo_project .

# Libera a porta do container
ARG PORT
EXPOSE ${PORT}