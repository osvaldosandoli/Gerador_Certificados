# Use a imagem oficial do Python
FROM python:3.11-slim


#Para rodar o wkhtmltopdf
RUN apt-get update && \
    apt-get install -y \
    wkhtmltopdf \
    && apt-get clean

    

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie o arquivo de dependências para o container
COPY ./Worker/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt



# Copie o código do Worker para dentro do container
COPY ./Worker /app/Worker
COPY ./Model /app/Model
COPY ./Database /app/Database
COPY ./wait-script/wait-for-it.sh /app/wait-for-it.sh

# Conceda permissão de execução ao script
RUN chmod +x /app/wait-for-it.sh
#COPY ./SaveCertificado /app/SaveCertificado

# Copie os templates HTML da pasta 'Template' para dentro do container
COPY ./Worker/Template /app/Template

# Exponha a porta necessária (se necessário)
#EXPOSE 5672  

#Porta do RabbitMQ, se o Worker for se comunicar diretamente com ele

# Comando para rodar o Worker
CMD ["/app/wait-for-it.sh", "rabbitmq:5672", "--", "python", "Worker/app.py"]
