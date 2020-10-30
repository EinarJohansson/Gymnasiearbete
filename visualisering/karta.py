import threading, queue
import matplotlib.pyplot as plt 
import matplotlib.animation as anim
from koordinat import Koordinat
from databas import Databas
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
        self.db = Databas()

        self.fig = plt.figure()

        self.ax = self.fig.gca()
        self.ax.set_ylabel('cm')
        self.ax.set_xlabel('cm')

        self.position = (0, 0) # Robotens startpostion markeras från origo

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

            if len(self.koordinater) == 180:
                self.db.spara(self.koordinater, self.position) 
                self.koordinater.clear()

            kö.task_done()

    def konvertera(self, koordinat: Koordinat) -> tuple:
        '''
        Hemmasnickrad matte, inte säker på om det fungerar men ger lovande resultat.
        '''
        x = koordinat.distans * cos(pi/2 - koordinat.vinkel) + koordinat.x
        y = koordinat.distans * sin(pi/2 - koordinat.vinkel) + koordinat.y
        
        return {'x': x, 'y': y} # Informationen som lagras i databasen tillsammans med positionen.

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
        cursor = self.db.kista({'_id': 0, 'koordinater': 1})

        x, y = [], []

        for koordinater in cursor:
           for koordinat in koordinater['koordinater']:
               x.append(koordinat['x'])
               y.append(koordinat['y'])

        plt.scatter(x, y)               # Markera väggarnas position med en prick
        plt.plot(*self.position, '*')    # Markera vart roboten är i koordinatsystemet
        cursor.close()