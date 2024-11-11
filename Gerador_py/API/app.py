import sys
import os
import pika
import redis
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Database.config import Config
from Model.Certificados import Certificado, db
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)
app.config.from_object(Config)

# Inicializando o banco de dados
db.init_app(app)

# Configurando o Redis
cache = redis.Redis(host='redis', port=6379)


# Função para enviar o JSON para a fila
def send_rabbit(data):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Declara a fila se ela ainda não existir
    channel.queue_declare(queue='certificado_queue')

    # Publica a mensagem JSON na fila
    channel.basic_publish(exchange='', routing_key='certificado_queue', body=json.dumps(data))
    print("JSON enviado para a fila RabbitMQ")
    connection.close()

# Método POST, para enviar o JSON.
# URL: http://localhost:5000/certificado
@app.route('/certificado', methods=['POST'])
def addCertificado():
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
        
        # Salvando no MySQL
        db.session.add(novo_certificado)
        db.session.commit()

        # Enviando para a Fila
        send_rabbit(data)
        return jsonify({'message': 'Certificado criado com sucesso!'}), 201

    except Exception as e:
        #Caso de errado executando um Rollback no MySQL
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Método GET, para exibir os certificados.
# URL: http://localhost:5000/certificado/?
@app.route('/certificado/<int:id>', methods=['GET'])
def getCertificado(id):
    
    # Tenta recuperar os dados no Redis
    cached_pdf_path = cache.get(f"certificado_{id}")

    if cached_pdf_path:
        # Retorna os dados no metodo se encontrados.
        return send_file(cached_pdf_path.decode('utf-8'), as_attachment=True)

    # Caso não encontre no Redis, procurar no MySQL
    session = db.session()  
    try:
        # Busca o certificado no banco de dados
        certificado = session.query(Certificado).filter_by(id=id).first()

        #Se encontrar o certificado
        if certificado and certificado.caminho:
            # Executa o armazenamento do caminho do PDF no Redis
            cache.set(f"certificado_{id}", certificado.caminho)
            return send_file(certificado.caminho, as_attachment=True)
        else:
            return jsonify({"erro": "Certificado não encontrado"}), 404
    except Exception as e:
        print(f"Erro ao buscar o certificado: {e}")
        return jsonify({"erro": f"Erro no servidor: {str(e)}"}), 500
    finally:
        session.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
