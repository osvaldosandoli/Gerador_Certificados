import json
import pika
import pdfkit
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Model.Certificados import Certificado
from jinja2 import Environment, FileSystemLoader
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database import config

# Configurar o ambiente Jinja2 para renderizar o template HTML
env = Environment(loader=FileSystemLoader('Template'))
template = env.get_template('template.html')

# Configuração do banco de dados
DATABASE_URI = config.Config.SQLALCHEMY_DATABASE_URI
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

# Método responsavel por incluir um contador no nome do certificado impedindo nomes duplicados
def renameCertificado(base_path, nome):
    counter = 1
    base_path = "./SaveCertificado"
    pdf_path = f"{base_path}/{nome}_certificado.pdf"
    
    # Incrementa o contador até encontrar um nome de arquivo não utilizado
    while os.path.exists(pdf_path):
        pdf_path = f"{base_path}/{nome}_{counter}_certificado.pdf"
        counter += 1
    return pdf_path

# Método para consumir os dados na lista do Rabbit
def consume_rabbit():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672))
    channel = connection.channel()
    
    channel.queue_declare(queue='certificado_queue')

    def callback(ch, method, properties, body):
        data = json.loads(body)
        print(f"Recebido: {data}")

        # Recebendo os dados do JSON
        html_content = template.render(data)

        # Definindo o conteudo do Caminho e do Nome do arquivo
        base_path = "./SaveCertificado"
        pdf_path = renameCertificado(base_path, data['nome'])

        # Configuração do wkhtmltopdf
        config_pdfkit = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

        # Opções de layout para a geração do PDF
        options = {
            'orientation': 'Landscape',
        }

        # Gera o PDF a partir do HTML
        pdfkit.from_string(html_content, pdf_path, configuration=config_pdfkit, options=options)
        print(f"PDF gerado: {pdf_path}")

        # Conectar ao SQL e atualizar a coluna de Caminho
        session = Session()
        try:
            # Consulta o certificado correspondente para atualização do caminho
            certificado = session.query(Certificado).filter_by(nome=data['nome']).order_by(Certificado.id.desc()).first()
            if certificado:
                certificado.caminho = pdf_path
                session.commit()
                print(f"Caminho do PDF atualizado: {pdf_path}")
            else:
                print("Certificado não encontrado para atualizar o caminho.")
        except Exception as e:
            print(f"Erro ao atualizar o banco de dados: {e}")
            session.rollback()
        finally:
            session.close()

    channel.basic_consume(queue='certificado_queue', on_message_callback=callback, auto_ack=True)
    print('Aguardando mensagens...')

    channel.start_consuming()


if __name__ == "__main__":
    consume_rabbit()
