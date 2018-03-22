#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: simulador.py
# Capitulo: 3 Patrón Publica-Subscribe
# Autor(es): Perla Velasco & Yonathan Mtz.
# Version: 2.0.1 Mayo 2017
# Descripción:
#
#   Esta clase define el rol de un set-up, es decir, simular el funcionamiento de los wearables del caso de estudio.
#
#   Las características de ésta clase son las siguientes:
#
#                                          simulador.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |  - Iniciar el entorno   |  - Define el id inicial|
#           |        set-up         |    de simulación.       |    a partir del cuál se|
#           |                       |                         |    iniciarán los weara-|
#           |                       |                         |    bles y temporizador.|
#           +-----------------------+-------------------------+------------------------+
#
#   A continuación se describen los métodos que se implementaron en ésta clase:
#
#                                               Métodos:
#           +-----------------------------+--------------------------+-----------------------+
#           |         Nombre              |        Parámetros        |        Función        |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Inicializa los     |
#           |                             |                          |    publicadores       |
#           |set_up_sensors_temporizador()|          Ninguno         |    necesarios para co-|
#           |                             |                          |    menzar la simula-  |
#           |                             |                          |    ción.              |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Ejecuta el método  |
#           |                             |                          |    publish de cada    |
#           |     start_sensors()         |          Ninguno         |    sensor para publi- |
#           |                             |                          |    car los signos vi- |
#           |                             |                          |    tales.             |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Ejecuta el método  |
#           |                             |                          |    publish del        |
#           |     start_temporizador()    |          Ninguno         |    temporizador para  |
#           |                             |                          |    publicar los signos|
#           |                             |                          |    alarmas.           |
#           +-----------------------------+--------------------------+-----------------------+
#-------------------------------------------------------------------------
import sys
import progressbar
from time import sleep
sys.path.append('publicadores')
from xiaomi_my_band import XiaomiMyBand
from temporizador import MyTemporizador
from pyfiglet import figlet_format
import random
import threading
import time

class Simulador:
    sensores = []
    id_inicial = 39722608
    grupos = []
    medicamentos =([["Paracetamol","01:19","1"],["Ibuprofeno","01:09",".5"],["Insulina","01:19","2"],["Furosemida","01:20","1.5"],["Piroxicam","01:20",".5"],["Tolbutamida","01:21","2"]])

    def set_up_sensors_temporizador(self):
        print('cargando')
        self.draw_progress_bar(10)
        print(figlet_format('Bienvenido'))
        print('Tarea 1: arquitecturas Publica - Suscribe')
        print('Cargando simulador')
        self.draw_progress_bar(20)
        print('+---------------------------------------------+')
        print('|        CONFIGURACIÓN DE LA SIMULACIÓN       |')
        print('+---------------------------------------------+')
        adultos_mayores = raw_input('|ingresa el número de adultos mayores: ')
        print('+---------------------------------------------+')
        raw_input('presiona enter para continuar: ')
        print('+---------------------------------------------+')
        print('|            ASIGNACIÓN DE SENSORES           |')
        print('+---------------------------------------------+')

        for x in xrange(0, int(adultos_mayores)):
            s = XiaomiMyBand(self.id_inicial)
            self.sensores.append(s)
            print('| wearable Xiaomi My Band asignado, id: ' + str(self.id_inicial))
            print('+---------------------------------------------+')
            self.id_inicial += 1

        for x in xrange(0,len(self.sensores)):
            item=[self.sensores[x].id, random.randint(0, len(self.medicamentos))]
            self.grupos.append(item)

        print('+---------------------------------------------+')
        print('|        LISTO PARA INICIAR SIMULACIÓN        |')
        print('+---------------------------------------------+')
        print('')
        print('*Nota: Se enviarán 1000 mensajes como parte de la simulación')
        raw_input('presiona enter para iniciar: ')

        hilo_temporizador = threading.Thread(target=self.start_temporizador)
        hilo_temporizador.daemon = 1
        hilo_sensores = threading.Thread(target=self.start_sensors)
        hilo_sensores.daemon = 1
        hilo_temporizador.start()
        hilo_sensores.start()
        
        while 1:
            time.sleep(1)

    def start_sensors(self):
        for x in xrange(0, 1000):
            for s in self.sensores:
                s.publish()
        
    def start_temporizador(self):
        t = MyTemporizador(self.medicamentos, self.grupos)
        t.publish()

    def draw_progress_bar(self, value):
        bar = progressbar.ProgressBar(maxval=value, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()
        for i in xrange(value):
            bar.update(i+1)
            sleep(0.2)
        bar.finish()

if __name__ == '__main__':
    simulador = Simulador()
    simulador.set_up_sensors_temporizador()

