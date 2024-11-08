import json
import pika
import pdfkit
from jinja2 import Environment, FileSystemLoader

# Configurar o ambiente Jinja2 para renderizar o template HTML
env = Environment(loader=FileSystemLoader('Template'))
template = env.get_template('template.html')

def consume_from_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672))
    channel = connection.channel()
    
    channel.queue_declare(queue='certificado_queue')

    def callback(ch, method, properties, body):
        data = json.loads(body)
        print(f"Recebido: {data}")

        # Preenche o template com os dados do JSON
        html_content = template.render(data)

        # Caminho do arquivo PDF gerado
        pdf_path = f"./SaveCertificado/{data['nome']}_certificado.pdf"

        # Configuração do wkhtmltopdf
        config = pdfkit.configuration()
        config.wkhtmltopdf = '/usr/bin/wkhtmltopdf'

        # Opções para a geração do PDF (como tamanho da página, margens, etc.)
        options = {
             'page-size': 'A4',
             'orientation': 'Landscape',
             'no-outline': None,
             'margin-top': '0mm',
             'margin-right': '0mm',
             'margin-bottom': '0mm',
             'margin-left': '0mm',
             'disable-smart-shrinking': None  # Evita encolhimento do conteúdo
        }

        # Gera o PDF a partir do HTML
        pdfkit.from_string(html_content, pdf_path, configuration=config, options=options)
        #pdfkit.from_string(html_content, pdf_path)
        print(f"PDF gerado: {pdf_path}")

    channel.basic_consume(queue='certificado_queue', on_message_callback=callback, auto_ack=True)
    print('Aguardando mensagens...')

    channel.start_consuming()

if __name__ == "__main__":
    consume_from_rabbitmq()
