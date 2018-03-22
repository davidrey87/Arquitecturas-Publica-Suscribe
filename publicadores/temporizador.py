#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------
# Archivo: xiaomi_my_band.py
# Capitulo: 3 Patrón Publica-Subscribe
# Autor(es): David Reyes, Sandy de la Rosa, Jose Rodriguez & Manuel Marquez.
# Version: 1.0.1 Mayo 2017
# Descripción:
#
#   Ésta clase define el rol de un publicador, es decir, es un componente que envia mensajes.
#
#   Las características de ésta clase son las siguientes:
#
#                                       xiaomi_my_band.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |  - Enviar mensajes      |  - Simula información  |
#           |      Publicador       |                         |    sobre alarmas.      |
#           +-----------------------+-------------------------+------------------------+
#
#   A continuación se describen los métodos que se implementaron en ésta clase:
#
#                                             Métodos:
#           +-----------------------------+--------------------------+-----------------------+
#           |         Nombre              |        Parámetros        |        Función        |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Inicializa el      |
#           |       __init__()            |       medicamento: []    |    temporizador.      |
#           |                             |       grupos: []         |                       |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             | x:int                    |  - Envia los mensajes |
#           |        job()                | medicamento : str        |    a la broker desde  | 
#           |                             | adultos: str             |    publush().         |
#           |                             | dosis: str               |                       |
#           |                             | tiempo: str              |                       |
#           |                             | datetime: str            |                       |         
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Envía las          |
#           |        publish()            |          Ninguno         |    alarmas al metodo  | 
#           |                             |                          |    job para programar |
#           |                             |                          |    la publicacion del |
#           |                             |                          |    mensaje.           |         
#           +-----------------------------+--------------------------+-----------------------+
#           |   simulate_datetime()       |          Ninguno         |  - Simula valores de  |
#           |                             |                          |    fecha y hora.      |
#           +-----------------------------+--------------------------+-----------------------+
#-------------------------------------------------------------------------
import pika
import random
import progressbar
import schedule
import time

class MyTemporizador:
    producer = "Temporizador"
    grupos = []
    medicamentos = []
    
    def __init__(self, medicamentos, grupos):
        self.medicamentos = medicamentos
        self.grupos = grupos

    def publish(self):
        for x in xrange(0,len(self.medicamentos)):
            adultos = ''

            for i in xrange(0,len(self.grupos)):
                if self.grupos[i][1] == x:
                    adultos = adultos+'|'+str(self.grupos[i][0])

            schedule.every().day.at(self.medicamentos[x][1]).do(job,x,self.medicamentos[x][0], adultos, self.medicamentos[x][2], self.medicamentos[x][1],self.simulate_datetime())

        while True:
            schedule.run_pending()
            time.sleep(1)

    def simulate_datetime(self):
        return time.strftime("%d:%m:%Y:%H:%M:%S")

def job(x, medicamento, adultos, dosis, tiempo, datetime):
    #Aqui se publica
    message = {}
    message['medicamento'] = medicamento
    message['grupo'] = str(x)
    message['adultos'] = adultos
    message['dosis'] = dosis
    message['tiempo'] = tiempo
    message['datetime'] = datetime

    # Se establece la conexion con el Distribuidor de Mensajes
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    # Se solicita un canal por el cual se enviaran las alarmas
    channel = connection.channel()
    # Se declara una cola para persistir los mensajes enviados
    channel.queue_declare(queue='medicamento', durable=True)
    print('[x] Publicando alarma grupo '+str(x)+' '+medicamento+' '+adultos)
    channel.basic_publish(exchange='', routing_key='medicamento', body=str(message), properties=pika.BasicProperties(delivery_mode=2,))  
    # Se realiza la publicacion del mensaje en el Distribuidor de Mensajes
    connection.close()  # Se cierra la conexion
    print('[x] Alarma publicada')
    print('')
