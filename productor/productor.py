import pika
from flask import Flask, request, jsonify
import json
import time

app = Flask(__name__)

# Conexión de RabbitMQ
connection = None
while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-soporte', port=5672, heartbeat=600))
        canal = connection.channel()
        canal.queue_declare(queue='cola-soporte6')
        print("Conexión a RabbitMQ exitosa")
        break
    except Exception as e:
        print("Error al conectar con RabbitMQ:", e)
        time.sleep(5)


@app.route('/soporte', methods=['POST'])
def recibir_requerimiento():
    body = request.get_json()
    nombre = body.get('nombre')
    telefono = body.get('telefono')
    requerimiento = body.get('requerimiento')

    if not nombre or not telefono or not requerimiento:
        return jsonify({"error": "Faltan datos en la solicitud"}), 400

    mensaje = {
        "nombre": nombre,
        "telefono": telefono,
        "requerimiento": requerimiento
    }

    try:
        # Convertir el mensaje a JSON y enviarlo a la cola
        canal.basic_publish(exchange='', routing_key='cola-soporte6', body=json.dumps(mensaje), properties=pika.BasicProperties(delivery_mode=2)  )
        print("Mensaje enviado a la cola")
        return jsonify({"mensaje": "Solicitud de soporte a sido recibida recibida"}), 201

    except Exception as e:
        print("Error al enviar el mensaje:", e)
        return jsonify({"error": "No se pudo enviar el mensaje a la cola"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
