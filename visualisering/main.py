import sys
from klient import Klient

def main():
    ip = sys.argv[1]

    # Kollar så att porten kan konverteras till ett nummer
    try:
        port = int(sys.argv[2])
    except ValueError:
        print("Port måste vara ett nummer!")
    else:
        # Lyckades
        Klient(ip, port)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        main()
    else:
        print('Användning: python3 main.py [IP] [PORT]')
