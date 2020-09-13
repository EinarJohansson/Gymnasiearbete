import sys
from server import Server

def main():
    '''
    Programmets main funktion
    '''
    server = Server()
    server.lyssna()

if __name__ == "__main__":
    main()