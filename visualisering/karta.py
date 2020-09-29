import threading, queue
import matplotlib.pyplot as plt 
import numpy as np

class Karta:
    '''
    Klass för att visualisera data från roboten.
    '''
    def __init__(self):
        '''
        Initierar kartan med lista för koordinaterna.
        '''
        self.koordinater = list()
        
        self.fig = plt.figure()

        self.ax = self.fig.gca()
        self.ax.set_xticks(np.arange(0, 1, 0.1))
        self.ax.set_yticks(np.arange(0, 1., 0.1))

    def läs(self, kö: queue.Queue):
        '''
        Hämta och spara senaste koordinaten från kön.
        '''
        while True:
            data = kö.get()
            print('Från kö:', data)
            self.koordinater.append(data)
            kö.task_done()

    def visa(self):
        x = np.arange(0, 1, 0.05)
        y = np.power(x, 2)

        plt.grid()
        plt.scatter(x, y)
        plt.show()