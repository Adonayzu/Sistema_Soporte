import sys
import pika
import mysql.connector
import json

def main():
    #conexión a MySQL
    try:
        conexion_bd = {
            'host': 'mysql-cola-sms',
            'database': 'sistema_soporte2024',
            'user': 'adonay',
            'password': '12345',
            'port': 3306
        }

    except mysql.connector.Error as err:
        print("Error al conectar con MySQL:", err)
        exit(1)  # el 1 indica que el programa terminó debido a un error

    # Configurar conexión a RabbitMQ
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-cola'))
        canal = connection.channel()
        canal.queue_declare(queue='cola-soporte6')
    except Exception as e:
        print("Error al conectar con RabbitMQ:", e)
        exit(1)   # el 1 indica que el programa terminó debido a un error

    # Callback para procesar mensajes de la cola
    def callback(ch, method, properties, body):
        try:
            # Procesar mensaje de la cola
            data = json.loads(body)
            nombre = data['nombre']
            telefono = data['telefono']
            requerimiento = data['requerimiento']

            # Insertar en la base de datos
            conexion = mysql.connector.connect(**conexion_bd)
            cursor = conexion.cursor() # cursor es un objeto que permite ejecutar sentencias sql
            sql = "INSERT INTO Requerimiento (nombre, telefono, requerimiento) VALUES (%s, %s, %s)"
            valores = (nombre, telefono, requerimiento)
            cursor.execute(sql, valores)
            conexion.commit() # se asegura para que se guarden los datos en la base de datos

            print("Requerimiento guardado en la base de datos")

        except Exception as e:
            print("Error al procesar el mensaje:", e)

        finally:
            cursor.close() # cierra el cursor
            conexion.close() # cierra la conexión

    # Configurar la cola para recibir mensajes
    canal.basic_consume(queue='cola-soporte', on_message_callback=callback, auto_ack=True)

    print('[*] Para salir presione CTRL + C')

    canal.start_consuming() #comienza a consumir mensajes de la cola


if __name__ == '__main__':
    # Llamar al método principal y luego dar control c y salir
    try:
        main()
    except KeyboardInterrupt:
        print('Interrumpido')
        try:
            sys.exit(0) # Salir con código de éxito
        except SystemExit:
            sys.exit(0)
