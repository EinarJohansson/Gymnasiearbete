import threading, queue

class Karta:
    '''
    Klass för att visualisera data från roboten.
    '''
    def __init__(self):
        '''
        Initierar kartan med lista för koordinaterna.
        '''
        self.koordinater = list()
    
    def läs(self, kö: queue.Queue):
        '''
        Hämta och spara senaste koordinaten från kön.
        '''
        while True:
            data = kö.get()
            print('Från kö:', data)
            self.koordinater.append(data)
            kö.task_done()