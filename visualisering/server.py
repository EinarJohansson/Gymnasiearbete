import socket, queue

class Server:
    '''
    Klass för att hantera inkommande UDP-meddlanden.
    '''
    def __init__(self):
        '''
        Initierar klassen genom att öppna upp en socket för UDP-meddelanden.
        '''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = (self.serverIP(), 8888)
        self.sock.bind(self.address)
        self.kö = queue.Queue()
        self.klient_addr = 0
    
    def __del__(self):
        self.sock.close()
        self.kö.join()

    def serverIP(self) -> str:
        '''
        Returnerar serverns ip-adress.\n
        Öppnar upp en ny socket bara för att få tag på ip addressen, sen tas den bort.
        '''
        dummy = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Spelar ingen roll om det går att nå adressen eller inte.
            dummy.connect(('8.8.8.8', 1))
            ip = dummy.getsockname()[0]
        except Exception:
            # Be användaren skriva in sin IP.
            print('Kunde inte hitta din IP')
            ip = input('Skriv in din IP: ')
        finally:
            # Ta bort dummy.
            dummy.close()
            del dummy

        print('Din ip:', ip)
        return ip

    def lyssna(self):
        '''
        Hantera UDP-meddelanden. 
        '''
        while True:
            # Buffert på 1024 bytes
            data, addr = self.sock.recvfrom(1024)
            if addr != self.klient_addr:
                print(addr)
                self.klient_addr = addr
            
            # print('Tog emot:', str(data, 'utf-8'))

            # Skicka tillbaks ett svar
            #self.sock.sendto(str.encode('Tja!'), self.klient_addr)
            # Lägg till data i kön som kartan sedan avläser
            self.kö.put(str(data, 'utf-8'))
    '''
    Skicka ett meddelande till servern
    '''
    def skicka(self, meddelande):
        if self.klient_addr:
            self.sock.sendto(str.encode(meddelande), self.klient_addr)
        else:
            raise Exception('Servern vet inte vart meddelandet ska') 

if __name__ == "__main__":
    s = Server()
    s.lyssna()