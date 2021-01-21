import threading, queue
import matplotlib.pyplot as plt 
import matplotlib.animation as anim
from koordinat import Koordinat
from databas import Databas
from math import cos, sin, pi, sqrt, atan, degrees, radians
import numpy as np
from stig import astar, stigTillKoords, koordsTillCell

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

        self.fig, self.axs = plt.subplots(1, 2)     # En rad, två kolumner
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        
        self.cb = None                              # Colorbaren för histogramet
        
        self.grid, self.xedges, self.yedges = None, None, None
        
        self.position = (0, 0)                      # Robotens startpostion markeras från origo
        self.summaV = 0                             # Summan av alla vinklar som svängts
        
    def onclick(self, event):
        # Är vi i histogramet?
        if event.dblclick and event.inaxes is self.axs[0]:
            x, y = event.xdata, event.ydata         # Positionen som klickades
            startCellX, startCellY = koordsTillCell(self.position[0], self.position[1], self.uppdelning, self.xedges, self.yedges)
            goalCellX, goalCellY = koordsTillCell(x, y, self.uppdelning, self.xedges, self.yedges)

            start = (startCellX, startCellY)
            goal = (goalCellX, goalCellY)

            route = astar(self.grid, start, goal)   # Punkter roboten måste ta sig till i ordning
            assert(route != None)
            
            route = route + [start]
            route = route[::-1]

            stig_x, stig_y = stigTillKoords(route, self.uppdelning, self.xedges, self.yedges)
            self.axs[0].plot(stig_x, stig_y)        # Plotta vägen roboten ska gå
            
            steg = tuple(zip(stig_x, stig_y))
            polär_stig = self.polärStig(steg)  # Stigen i polär format
            
            self.axs[0].plot(*self.position, '^')   # Markera vart roboten är i koordinatsystemet

            # Skicka koordinaterna till klienten
            if hasattr(self, 'skicka'):
                print('Skickar t klienten')
                for r, v in polär_stig:
                    data = str(round(degrees(r))) + ';' + str(round(degrees(v)))
                    print(data)
                    self.skicka(data)

            plt.draw()

    def polärStig(self, stig) -> tuple:
        '''
        Konverterar en stig med karteiska koordinater till en stig med polära koordinater.
        '''

        l = []
        for x, y in stig:
            print('Robotens postion: ', self.position)
            print('Nästa postition: ', (x, y))

            dx = x - self.position[0]
            dy = y - self.position[1]

            print('Skillnad mellan x: ', dx)
            print('Skillnad mellan y: ', dy)

            print('SummaV:', self.summaV)
            
            '''
            1 - höger
            2 - vänster
            3 - upp
            4 - ner
            '''
            if dx != 0:     # Gå horizontellt
                riktning = 1 if dx > 0 else 2 
                r = abs(dx)
            elif dy != 0:   # Gå vertikalt
                riktning = 3 if dy > 0 else 4
                r = abs(dy)
            else:           # Gå ingenstans
                r = 0
                v = 0
                riktning = False
            
            # Om vinkelsumman är större än 360, använd periodiciteten
            if self.summaV >= 360:
                self.summaV %= 360

            if self.summaV == 0 or self.summaV == 360:    # nosen fram
                # höger = 90
                # vänster = -90
                # upp = 0
                # ner = 180
                svängningar = [90, -90, 0, 180]
                print('nosen är uppåt')
                if riktning:
                    v = radians(svängningar[riktning-1])
            elif self.summaV == 90 or self.summaV == -270: # nosen åt höger
                # höger = 0
                # vänster = 180
                # upp = -90
                # ner = 90
                svängningar = [0, 180, -90, 90]
                print('nosen är åt höger')
                if riktning:
                    v = radians(svängningar[riktning-1])
            elif self.summaV == 180 or self.summaV == -180: # nosen ner
                # höger = -90
                # vänster = 90
                # upp = 180
                # ner = 0
                svängningar = [-90, 90, 180, 0]
                print('nosen är neråt')
                if riktning:
                    v = radians(svängningar[riktning-1])
            elif self.summaV == 270 or self.summaV == -90: # nosen åt vänster
                # höger = 180
                # vänster = 0
                # upp = 90
                # ner = -90
                print('nosen är åt vänster')
                svängningar = [180, 0, 90, -90]
                if riktning:
                    v = radians(svängningar[riktning-1])
            else:
                print('oj är det nåt skumt med vinkelsumman')
                print('summan av vinklarna är: ', self.summaV)
            
            print('\nr: ', round(r, 1), '\nv: ', round(degrees(v), 1), '\n\n')
            
            if r and v:
                l.append((r, v))

            self.position = (x, y)      # Uppdatera robotens position 
            self.summaV += degrees(v)   # Öka vinkelsumma
        return l

    def läs(self, kö: queue.Queue): # Få med servern
        '''
        Hämta och spara senaste koordinaten från kön.
        '''
        while True:
            data = kö.get() 
            koord = Koordinat(data)
            
            if (self.position is not (koord.x, koord.y)):
                self.position = (koord.x, koord.y)

            print(len(self.koordinater))

            vägg = self.konvertera(koord)
            self.koordinater.append(vägg)

            if len(self.koordinater) == 180:
                # Spara koordianterna
                self.db.spara(self.koordinater, self.position) 
                # Gör rum för nya koordinater
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

    def hämta_data(self):
        '''
        Hämta koordinater från databasen.
        '''
        cursor = self.db.kista({'_id': 0, 'koordinater': 1})
        x, y = [], []

        for koordinater in cursor:
            for koordinat in koordinater['koordinater']:
                x.append(koordinat['x'])
                y.append(koordinat['y'])

        cursor.close()          # Stäng ner handtaget till databasen
        return x, y

    def rita(self, x, y):       # TODO omfaktorisera, för mycket kod
        '''
        Rita ut allt som ska synas på kartan.
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

        # https://en.wikipedia.org/wiki/Histogram#Square-root_choice
        self.uppdelning = int(sqrt(len(x))) or 50
        print('Bins =', self.uppdelning)

        # Visa frekvensen av träffar för alla väggars koordinater
        counts, self.xedges, self.yedges, im = self.axs[0].hist2d(x, y, bins=self.uppdelning, cmap=plt.cm.Reds, cmin=1)
        
        counts = np.array(counts)                   # 2D array representation
        counts[np.isnan(counts)] = 0                # Fria rutor representeras som nollor
        counts[np.greater(counts, 1)] = 1           # Upptagna rutor representeras som ettor
        
        self.grid = counts.astype(np.uint8)         # Gör om floats till unsigned ints

        self.axs[0].plot(*self.position, '^')       # Markera vart roboten är i histogramet

        self.cb = plt.colorbar(im, ax=self.axs[0])  # Visar histogramets färger innebär med en colorbar
        self.cb.ax.set_ylabel('Antal träffar')      # Förtydligar vad colorbaren betyder
        
        self.axs[1].scatter(x[-180:], y[-180:])     # Visa senaste skanningen i ett koordinatsystem
        self.axs[1].plot(*self.position, '^')       # Markera vart roboten är i koordinatsystemet

    def visa(self, skicka):
        ''' 
        Visa kartan första gången.
        '''
        x,y = self.hämta_data()
        self.rita(x,y)
        self.skicka = skicka
        plt.show()

    def uppdatera(self):
        ''' 
        Uppdatera kartan med nya värden.
        '''
        x,y = self.hämta_data()
        self.rita(x,y)
        plt.draw()              # Rita de uppdaterade värdena
