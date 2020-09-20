from server import Server
from karta import Karta
import threading

def main():
    '''
    Programmets main funktion
    '''
    server = Server()   # Vår server som roboten pratar med.
    karta = Karta()     # Visualisera vår data.

    tråd1 = threading.Thread(target=server.lyssna, daemon=True)
    tråd2 = threading.Thread(target=karta.läs, args=(server.kö,))
    
    tråd1.start()
    tråd2.start()

if __name__ == '__main__':
    main()