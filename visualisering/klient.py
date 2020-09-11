import socket

class Klient:
    def __init__(self, ip: str, port: int):
        self.validera(ip, port)

    def validera(self, ip, port):
        try:
            socket.inet_aton(ip)
        except socket.error:
            raise Exception('Felaktig ip')
        else:
            if 1 <= port <= 65535:
                # Lyckades validera Ip-adressen och porten
                self.adress = (ip, port)
                self.setup()
            else:
                raise Exception('Port måste vara mellan 1 och 65535')

    def setup(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('kommer hit')
    
    def kommunicera(self):
        pass
