#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: procesador_de_posicion.py
# Capitulo: 3 Estilo Publica-Subscribe
# Autor(es): David Reyes, Sandy de la Rosa, Jose Rodriguez & Manuel Marquez.
# Version: 2.0.1 Marzo 2018
# Descripción:
#
#   Esta clase define el rol de un suscriptor, es decir, es un componente que recibe mensajes.
#
#   Las características de ésta clase son las siguientes:
#
#                                     procesador_de_posicion.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |                         |  - Se suscribe a los   |
#           |                       |                         |    eventos generados   |
#           |                       |  - Procesar valores     |    por el wearable     |
#           |     Procesador de     |    extremos de la       |    Xiaomi My Band.     |
#           |        Posicion       |    posicion corporal.   |  - Define el valor ex- |
#           |                       |                         |    tremo de la pisicion|
#           |                       |                         |    corporal en:        |  
#           |                       |                         |    x < 0   & x >10.    |
#           |                       |                         |    y < -10 & y > 2.    |    
#           |                       |                         |    z < -10 y z > 1.    |                                                             
#           |                       |                         |  - Notifica al monitor |
#           |                       |                         |    cuando un valor ex- |
#           |                       |                         |    tremo es detectado. |
#           +-----------------------+-------------------------+------------------------+
#
#   A continuación se describen los métodos que se implementaron en ésta clase:
#
#                                               Métodos:
#           +------------------------+--------------------------+-----------------------+
#           |         Nombre         |        Parámetros        |        Función        |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Recibe los signos  |
#           |       consume()        |          Ninguno         |    vitales vitales    |
#           |                        |                          |    desde el distribui-|
#           |                        |                          |    dor de mensajes.   |
#           +------------------------+--------------------------+-----------------------+
#           |                        |  - ch: propio de Rabbit. |  - Procesa y detecta  |
#           |                        |  - method: propio de     |    valores extremos de|
#           |                        |     Rabbit.              |    la posicion        |
#           |       callback()       |  - properties: propio de |    corporal.          |
#           |                        |     Rabbit.              |                       |
#           |                        |  - body: mensaje recibi- |                       |
#           |                        |     do.                  |                       |
#           +------------------------+--------------------------+-----------------------+
#           |    string_to_json()    |  - string: texto a con-  |  - Convierte un string|
#           |                        |     vertir en JSON.      |    en un objeto JSON. |
#           +------------------------+--------------------------+-----------------------+
#
#
#           Nota: "propio de Rabbit" implica que se utilizan de manera interna para realizar
#            de manera correcta la recepcion de datos, para éste ejemplo no shubo necesidad
#            de utilizarlos y para evitar la sobrecarga de información se han omitido sus
#            detalles. Para más información acerca del funcionamiento interno de RabbitMQ
#            puedes visitar: https://www.rabbitmq.com/
#
#-------------------------------------------------------------------------
import pika
import sys
sys.path.append('../')
from monitor import Monitor
import time


class ProcesadorPosicion:

    def consume(self):
        try:
            # Se establece la conexión con el Distribuidor de Mensajes
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            # Se solicita un canal por el cuál se enviarán los signos vitales
            channel = connection.channel()
            # Se declara una cola para leer los mensajes enviados por el
            # Publicador
            channel.queue_declare(queue='body_position', durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(self.callback, queue='body_position')
            channel.start_consuming()  # Se realiza la suscripción en el Distribuidor de Mensajes
        except (KeyboardInterrupt, SystemExit):
            channel.close()  # Se cierra la conexión
            sys.exit("Conexión finalizada...")
            time.sleep(1)
            sys.exit("Programa terminado...")

    def callback(self, ch, method, properties, body):
        json_message = self.string_to_json(body)
        positions = json_message['body_position'].split('#')
        if (float(positions[0]) < 0) or (float(positions[0]) > 10) or (float(positions[1]) < -10) or (float(positions[1]) > 2) or (float(positions[2]) < -10) or (float(positions[2]) > 1) : 
            monitor = Monitor()
            monitor.print_notification('presenta problemas con la posicion corporal',json_message['datetime'], json_message['id'])

        time.sleep(1)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def string_to_json(self, string):
        message = {}
        string = string.replace('{', '')
        string = string.replace('}', '')
        values = string.split(', ')
        for x in values:
            v = x.split(': ')
            message[v[0].replace('\'', '')] = v[1].replace('\'', '')
        return message

if __name__ == '__main__':
    p_posicion = ProcesadorPosicion()
    p_posicion.consume()
