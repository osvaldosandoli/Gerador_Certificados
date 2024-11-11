FROM python:3.11-slim

#Comando para rodar o wkhtmltopdf no Docker
RUN apt-get update && \
    apt-get install -y \
    wkhtmltopdf \
    && apt-get clean

WORKDIR /app

# Instalandoo as dependencias
COPY ./Worker/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


# Copie o código do Worker para dentro do container
COPY ./Worker /app/Worker
COPY ./Model /app/Model
COPY ./Database /app/Database
COPY ./wait-script/wait-for-it.sh /app/wait-for-it.sh
COPY ./Worker/Template /app/Template

# Conceda permissão de execução ao script, sem o script o Worker tenta ser executando antes do Rabbit estar pronto
RUN chmod +x /app/wait-for-it.sh

# Comando para rodar o Worker
CMD ["/app/wait-for-it.sh", "rabbitmq:5672", "--", "python", "Worker/app.py"]
