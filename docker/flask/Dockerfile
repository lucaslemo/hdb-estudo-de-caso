# Imagem base oficial do Python
FROM python:3.10.15-slim

# Atualiza as dependencias do sistema 
RUN apt-get update && apt-get install -y --no-install-recommends \
  && rm -rf /var/lib/apt/lists/*

# Atualiza o pip da imagem 
RUN pip install --no-cache-dir --upgrade pip

# Diretório de trabalho dentro do container
WORKDIR /var/www/app

# Copia o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências do arquivo de requisitos
RUN pip install --no-cache-dir -r requirements.txt

# Atualiza setuptools para remover a vulnerabilidade CVE-2024-6345
RUN pip install --no-cache-dir --upgrade setuptools

# Copia o código do projeto para o container
COPY todo_project/ .

# CriadDiretório para o banco de dados
RUN mkdir -p /usr/hdb/db

# Libera a porta do container
ARG PORT=5000
EXPOSE ${PORT}