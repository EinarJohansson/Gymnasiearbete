import threading, queue
import matplotlib.pyplot as plt 
import matplotlib.animation as anim
import numpy as np
from koordinat import Koordinat

class Karta:
    '''
    Klass för att visualisera data från roboten.
    '''
    def __init__(self):
        '''
        Initierar kartan.
        '''
        self.koordinater = list()
        self.fig = plt.figure()
        self.ax = self.fig.gca() 

        plt.grid() # Rutnät över grafen

    def läs(self, kö: queue.Queue):
        '''
        Hämta och spara senaste koordinaten från kön.
        '''
        while True:
            data = kö.get()
            print('Från kö:', data)
            self.koordinater.append(Koordinat(data))
            kö.task_done()

    def visa(self):
        '''
        Visa kartan.
        '''
        a = anim.FuncAnimation(self.fig, self.uppdatera, repeat=True, interval=2000)
        plt.show()

    def uppdatera(self, i):
        ''' 
        Uppdatera kartan med nya värden.
        '''
        if self.koordinater:
            x = [kord.x for kord in self.koordinater]
            y = [kord.y for kord in self.koordinater]
            
            plt.scatter(x, y) # Markera robotens position med en prick
