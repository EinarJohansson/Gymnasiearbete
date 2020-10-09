import threading, queue
import matplotlib.pyplot as plt 
import matplotlib.animation as anim
import numpy as np
from koordinat import Koordinat
from math import sqrt, pow, cos

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
            
            koord = Koordinat(data)
            
            if koord.vinkel == 0:
                self.referenspunkt = koord
                vägg = (koord.x, koord.y + koord.distans)
            else:
                try: 
                    vägg = self.konvertera(koord)
                    self.koordinater.append(vägg)    
                    kö.task_done()
                except Exception as e:
                    print(e)

    def konvertera(self, koordinat: Koordinat) -> tuple:
        '''
        Hemmasnickrad matte, inte säker på om det fungerar men ger lovande resultat.
        '''

        # h är en sida i en godtycklig triangel jag beräknar med cosinussatsen
        h = abs(sqrt(pow(self.referenspunkt.distans, 2) + pow(koordinat.distans, 2) - (2*self.referenspunkt.distans*koordinat.distans*cos(koordinat.vinkel))))
        
        # Löser ut y genom en annan triangel. 
        '''
        Yv = (Dog^2 + 2*Dog*Yr - h^2 + d^2)/(2d) där d!=0
        https://www.wolframalpha.com/input/?i=solve+for+v%3A+h%5E2+-%28v-d-r%29%5E2+%2B+%28v-r%29%5E2+%3D+x%5E2
        '''
        y = (pow(self.referenspunkt.distans, 2) + 2 * self.referenspunkt.distans * koordinat.y - pow(h, 2) + pow(koordinat.distans, 2))/(2*koordinat.distans)

        # Löser sedan ut x. X har dock två lösningar, en negativ och en positiv. Inte säker på när vilken är rätt.
        '''
        Xv = ± sqrt(-Xr^2 + 2*Xr*Xv - d^2 + 2*d*(Yv - Yr) + h^2 - Yv^2 + 2*Yv*Yr - Yr^2)        
        https://www.wolframalpha.com/input/?i=solve+for+v%3A+v%5E2+%3D+h%5E2+-+%28t-d-u%29%5E2+%2B+2*z*c-c%5E2
        '''
        x = sqrt(pow(h, 2) - pow(y - self.referenspunkt.distans - koordinat.y, 2) + 2 * self.referenspunkt.x * koordinat.x - pow(koordinat.x, 2))
        
        # Antagande, vet inte om detta stämmer alls. Troligtvis inte XD.
        if koordinat.vinkel > 0:
            return (x, y)
        else:
            return(-x, y)

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
            x = [kord[0] for kord in self.koordinater]
            y = [kord[1] for kord in self.koordinater]
            
            plt.scatter(x, y) # Markera väggarnas position med en prick
            plt.plot(self.referenspunkt.x, self.referenspunkt.y, '*') # Markera robotens position med en stjärna
