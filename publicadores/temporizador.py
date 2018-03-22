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
            schedule.every().day.at(self.medicamentos[x][1]).do(job,x,self.medicamentos[x][0])

        while True:
            schedule.run_pending()
            time.sleep(1)

def job(message, medicamento):
    #Aqui se publica
    print message
    print medicamento
