import threading, queue
import matplotlib.pyplot as plt 
import matplotlib.animation as anim
from koordinat import Koordinat
from databas import Databas
from math import cos, sin, pi, sqrt

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

        self.fig, self.axs = plt.subplots(1, 2)

        self.cb = None;

        self.position = (0, 0) # Robotens startpostion markeras från origo

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
        # Hemmasnickrad matte, inte säker på om det fungerar men ger lovande resultat.
        x = koordinat.distans * cos(pi - koordinat.vinkel) + koordinat.x
        y = koordinat.distans * sin(pi - koordinat.vinkel) + koordinat.y
        
        # Returnera informationen som ska lagras i databasen tillsammans med positionen.
        return {'x': x, 'y': y}

    def visa(self):
        '''
        Visa kartan.
        '''
        self.uppdatera()
        plt.show()

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
        self.axs[1].grid()

        cursor = self.db.kista({'_id': 0, 'koordinater': 1})

        x, y = [], []

        for koordinater in cursor:
           for koordinat in koordinater['koordinater']:
               x.append(koordinat['x'])
               y.append(koordinat['y'])

        # https://en.wikipedia.org/wiki/Histogram#Square-root_choice
        uppdelning = int(sqrt(len(x)))

        # Visa frekvensen av träffar för alla väggars koordinater
        counts, xedges, yedges, im = self.axs[0].hist2d(x, y, bins=uppdelning, cmap=plt.cm.Reds)
        
        self.axs[0].plot(*self.position, '^')       # Markera vart roboten är i histogramet

        self.cb = plt.colorbar(im, ax=self.axs[0])  # Visar histogramets färger innebär med en colorbar
        self.cb.ax.set_ylabel('Antal träffar')      # Förtydligar vad colorbaren betyder
        
        self.axs[1].scatter(x[-180:], y[-180:])     # Visa senaste skanningen i ett koordinatsystem
        self.axs[1].plot(*self.position, '^')       # Markera vart roboten är i koordinatsystemet

        plt.draw()                                  # Rita de uppdaterade värdena

        cursor.close()                              # Stäng ner handtaget till databasen