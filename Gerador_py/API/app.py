import sys
import os

import pika

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from Database.config import Config
from Model.Certificados import Certificado, db
from flask import Flask, request, jsonify

import json

app = Flask(__name__)
app.config.from_object(Config)

# Inicializando o banco de dados
db.init_app(app)


# Função para enviar o JSON para a fila RabbitMQ
def send_to_rabbitmq(data):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Declara a fila se ela ainda não existir
    channel.queue_declare(queue='certificado_queue')

    # Publica a mensagem JSON na fila
    channel.basic_publish(exchange='', routing_key='certificado_queue', body=json.dumps(data))
    print("JSON enviado para a fila RabbitMQ")
    connection.close()


@app.route('/certificado', methods=['POST'])
def criar_certificado():
    data = request.get_json()  # Recebe os dados JSON do corpo da requisição
    
    
    try:
        # Criando o objeto Certificado com os dados recebidos
        novo_certificado = Certificado(
            nome=data['nome'],
            nacionalidade=data['nacionalidade'],
            estado=data['estado'],
            data_nascimento=data['data_nascimento'],
            documento=data['documento'],
            data_conclusao=data['data_conclusao'],
            curso=data['curso'],
            carga_horaria=data['carga_horaria'],
            data_emissao=data['data_emissao'],
            nome_assinatura=data['nome_assinatura'],
            cargo=data['cargo']
        )
        
        # Salvando no banco de dados
        db.session.add(novo_certificado)
        db.session.commit()

        send_to_rabbitmq(data)

        return jsonify({'message': 'Certificado criado com sucesso!'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/certificado', methods=['GET'])
def vrf():
        return jsonify({'message': 'sucesso!'}), 201
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
