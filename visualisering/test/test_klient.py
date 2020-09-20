import socket
import random

class Klient:
    '''
    Prototyp som replikerar robotens kommunikation med servern.\n
    Denna klient är endast till för att testa och säkerställa att roboten\n
    och servern kan prata med och förstå varandra.  
    '''
    def __init__(self):
        '''
        Öppnar upp en socket för klienten så den kan kommunicera med serven.
        '''
        self.address = (self.serverIP(), 8888) # Serverns adress
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def serverIP(self) -> str:
        '''
        Returnerar serverns ip-adress.\n
        Öppnar upp en ny socket bara för att få tag på ip addressen, sen tas den bort.
        '''
        dummy = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Spelar ingen roll om vi kan nå adressen eller inte.
            dummy.connect(('8.8.8.8', 1))
            ip = dummy.getsockname()[0]
        except Exception:
            # Be användaren manuellt skriva in serverns IP.
            print('Kunde inte serverns din IP')
            ip = input('Skriv in serverns IP: ')
        finally:
            # Ta bort dummy.
            dummy.close()
            del dummy

        print('Serverns ip:', ip)
        return ip

    def skicka(self, meddelande: str):
        '''
        Skicka ett meddelande till servern.
        '''
        self.sock.sendto(str.encode(meddelande), self.address)

    def motta(self):
        '''
        Ta emot ett meddelande från servern.
        '''
        try:
            data, addr = self.sock.recvfrom(1024)
        except KeyboardInterrupt:
            self.sock.close()
            return
        
        print('tog emot:', data)

def main():
    klient = Klient()

    for vinkel in range(180):
        distans = random.randint(0, 450) # 0cm till 450cm
        steg = [str(random.randint(0, 100)) for i in range(4)]
        meddelande = str(distans) + ';' + str(vinkel) + ';' + ';'.join(steg)

        klient.skicka(meddelande)

    klient.motta()
    klient.sock.close()

if __name__ == "__main__":
    main()