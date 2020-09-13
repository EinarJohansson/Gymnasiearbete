import socket

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
    
    def serverIP(self) -> str:
        '''
        Returnerar serverns ip-adress.\n
        Öpnnar upp en ny socket bara för att få tag på ip addressen, sen tas den bort.
        '''
        dummy = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Spelar ingen roll om vi kan nå adressen eller inte.
            dummy.connect(('8.8.8.8', 1))
            ip = dummy.getsockname()[0]
        except Exception:
            # Be användaren manuellt skriva in sin IP.
            print('Kunde inte hitta din IP')
            ip = input('Skriv in din IP:')
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
            try:
                # Buffert på 1024 bytes
                data, addr = self.sock.recvfrom(1024)
                print('Tog emot:', str(data, 'utf-8'))

                # Skicka ett svar
                self.sock.sendto(str.encode('Tja!'), addr)
            except KeyboardInterrupt:
                print('\nAvslutar servern')
                self.sock.close()
                break