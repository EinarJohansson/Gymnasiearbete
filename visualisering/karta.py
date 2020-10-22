import threading, queue
import matplotlib.pyplot as plt 
import matplotlib.animation as anim
from koordinat import Koordinat
from math import cos, sin, pi

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
        self.ax.set_ylabel('cm')
        self.ax.set_xlabel('cm')

        self.position = (0, 0)

        plt.grid() # Rutnät över grafen

    def läs(self, kö: queue.Queue):
        '''
        Hämta och spara senaste koordinaten från kön.
        '''
        while True:
            data = kö.get() 
            koord = Koordinat(data)
            
            if (self.position is not (koord.x, koord.y)):
                self.position = (koord.x, koord.y)

            vägg = self.konvertera(koord)
            self.koordinater.append(vägg)    
    
            kö.task_done()

    def konvertera(self, koordinat: Koordinat) -> tuple:
        '''
        Hemmasnickrad matte, inte säker på om det fungerar men ger lovande resultat.
        '''
        x = koordinat.distans * cos(pi/2 - koordinat.vinkel) + koordinat.x
        y = koordinat.distans * sin(pi/2 - koordinat.vinkel) + koordinat.y
        
        return (x, y)

    def visa(self):
        '''
        Visa kartan.
        '''
        a = anim.FuncAnimation(self.fig, self.uppdatera, repeat=True, interval=3000)
        plt.show()

    def uppdatera(self, i):
        ''' 
        Uppdatera kartan med nya värden.
        '''
        if self.koordinater:
            x = [kord[0] for kord in self.koordinater]
            y = [kord[1] for kord in self.koordinater]
            
            plt.scatter(x, y) # Markera väggarnas position med en prick
            plt.plot(self.position, '*') # Markera vart roboten är i koordinatsystemet
