import pika
import random
import progressbar
import schedule
import time

#Poner requirements que SCHEDULE es requerido pip install

class MyTemporizador:
    producer = "Temporizador"
    grupos = []
    medicamentos = []
    
    def __init__(self, medicamentos, grupos):
        self.medicamentos = medicamentos
        self.grupos = grupos

    def publish(self):
        for x in xrange(0,len(self.medicamentos)):
            schedule.every().day.at(self.medicamentos[x][1]).do(job)

        while True:
            schedule.run_pending()
            time.sleep(1)

def job():
    #Aqui se publica
    print("Publicando alarma¡¡¡")
    message = {}
        message['medicamento'] = self.simulate_heart_rate()
        message['grupo'] = str(self.id)
        message['ids'] = self.simulate_datetime()
        message['producer'] = self.producer

    #medicamentos = ([["Paracetamol","13:27"],["ibuprofeno","13:28"],["insulina","13:29"]])
    #grupos =  [[39722608, 0], [39722609, 0], [39722610, 1], [39722611, 2], [39722612, 0], [39722613, 1], [39722614, 0], [39722615, 0], [39722616, 2], [39722617, 1], [39722618, 1], [39722619, 1]]