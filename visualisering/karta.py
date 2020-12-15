import threading, queue
import matplotlib.pyplot as plt 
import matplotlib.animation as anim
from koordinat import Koordinat
from databas import Databas
from math import cos, sin, pi, sqrt
import numpy as np
from stig import astar, stigTillKoords, koordTillCell

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

        self.fig, self.axs = plt.subplots(1, 2)                 # En rad, två kolumner
        self.cb = None                                          # Colorbaren för histogramet
        
        self.grid, self.xedges, self.yedges = None, None, None  # Bestäms av histogramet i uppdatera
        
        self.position = (0, 0)                                  # Robotens startpostion markeras från origo

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
                # Uppdatera grafen
                self.uppdatera()

            kö.task_done()

    def konvertera(self, koordinat: Koordinat) -> tuple:
        '''
        Konvertera mätningsdata till en punkt i förhållande till roboten.
        '''
        # Konverterar polär koordinat till kartesisk koordinat
        x = koordinat.distans * cos(pi - koordinat.vinkel) + koordinat.x
        y = koordinat.distans * sin(pi - koordinat.vinkel) + koordinat.y
        
        # Returnera informationen som ska lagras i databasen tillsammans med positionen.
        return {'x': x, 'y': y}

    def uppdatera(self):
        ''' 
        Uppdatera kartan med nya värden.
        '''
        self.axs[0].cla()       # Rensa histogramet
        self.axs[1].cla()       # Rensa koordinatsystemet

        if self.cb:
            self.cb.remove()    # Rensa colorbaren

        self.axs[0].set_title('Alla skanningar')
        self.axs[0].set_ylabel('cm')
        self.axs[0].set_xlabel('cm')

        self.axs[1].set_title('Senaste skanningen')
        self.axs[1].set_ylabel('cm')
        self.axs[1].set_xlabel('cm')

        cursor = self.db.kista({'_id': 0, 'koordinater': 1})

        x, y = [], []

        for koordinater in cursor:
           for koordinat in koordinater['koordinater']:
               x.append(koordinat['x'])
               y.append(koordinat['y'])

        # https://en.wikipedia.org/wiki/Histogram#Square-root_choice
        uppdelning = int(sqrt(len(x))) or 50
        print('Bins =', uppdelning)

        # Visa frekvensen av träffar för alla väggars koordinater
        counts, self.xedges, self.yedges, im = self.axs[0].hist2d(x, y, bins=uppdelning, cmap=plt.cm.Reds, cmin=1)
        
        counts = np.array(counts)                   # 2D array representation
        counts[np.isnan(counts)] = 0                # Fria rutor representeras som nollor
        counts[np.greater(counts, 1)] = 1           # Upptagna rutor representeras som ettor
        
        counts = counts.astype(np.uint8)            # Gör om floats till unsigned ints
        self.grid = np.rot90(counts, -1)            # Rotera arrayen -90 grader

        print(self.grid)
        start = (0,0) # Endast test värden for now
        goal = (1,1) # TODO Gör funktion som konverterar cell koordianter till karteiska koordinater

        route = astar(self.grid, start, goal)       # Punkter roboten måste ta sig till i ordning
        assert(route != None)
        print(route)
        
        route = route + [start]
        route = route[::-1]

        print(route)

        stig_x, stig_y = stigTillKoords(route, uppdelning, self.xedges, self.yedges)
        self.axs[0].plot(stig_x, stig_y)            # Plotta vägen roboten ska gå

        self.axs[0].plot(*self.position, '^')       # Markera vart roboten är i histogramet

        self.cb = plt.colorbar(im, ax=self.axs[0])  # Visar histogramets färger innebär med en colorbar
        self.cb.ax.set_ylabel('Antal träffar')      # Förtydligar vad colorbaren betyder
        
        self.axs[1].scatter(x[-180:], y[-180:])     # Visa senaste skanningen i ett koordinatsystem
        self.axs[1].plot(*self.position, '^')       # Markera vart roboten är i koordinatsystemet

        plt.show()                                  # Rita de uppdaterade värdena

        cursor.close()                              # Stäng ner handtaget till databasen