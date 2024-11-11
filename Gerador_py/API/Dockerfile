FROM python:3.9-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o contêiner e instale as dependências
COPY ./API/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o código da pasta API e Model para dentro do contêiner
COPY ./API /app/API
COPY ./Model /app/Model
COPY ./Database /app/Database


# Defina a variável de ambiente para o Python não gerar arquivos de bytecode
ENV PYTHONDONTWRITEBYTECODE 1

# Defina o comando para rodar a aplicação Flask
CMD ["python", "API/app.py"]
