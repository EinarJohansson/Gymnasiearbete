import socket

class Klient:
    def __init__(self):
        '''
        Inititerar Klient klassen.
        '''
        self.address = (self.klientIP(), 8888)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def skicka(self, meddelande: str):
        '''
        Skickar ett meddelande till servern.
        '''
        self.sock.sendto(str.encode(meddelande), self.address)
        # Buffert på 1024 bytes
        data, addr = self.sock.recvfrom(1024)
        return str(data, 'utf-8')

    def klientIP(self) -> str:
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
        return ip