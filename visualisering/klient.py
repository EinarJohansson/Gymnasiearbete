import socket

class Klient:
    def __init__(self, ip: str, port: int):
        self.address = (ip, port)
        self.test()

    def test(self):
        print(self.address)