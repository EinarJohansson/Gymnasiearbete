import pymongo
from datetime import datetime

class Databas:
    '''
    Klass för att lagra och hämta kartor.
    '''
    def __init__(self):
        '''
        Försöker ansluta till databasen.
        '''
        try:
            self.handtag = pymongo.MongoClient("mongodb://localhost:27017/")
            self.db = self.handtag["kartor"]
            self.karta = self.välj()
        except Exception as e:
            print('Starta mongo!')

    def kartor(self) -> list:
        '''
        Hämtar namnet på kartorna som redan finns.
        '''
        return self.db.list_collection_names()

    def kista(self, villkor: dict = {}) -> list:
        '''
        Öppnar upp kistan och returnerar dess koordinater.
        '''
        if self.karta:
            return self.karta.find({}, villkor)
    
    def välj(self):
        '''
        Välj om en ny karta ska skapas eller om en befintlig karta ska användas.
        '''
        kartor = self.kartor()
        antal = len(kartor)

        if antal > 0:
            print('Dessa kartor fanns redan i databasen\n')
            for i in range(antal):
                print('[{}]: {}'.format(i, kartor[i]))

            try:
                skapa = int(input('Vill du använda en befintlig karta? (0/1): '))
            except Exception:
                return self.ny()
            
            if not skapa:
                return self.ny()

            try:
                index = int(input('Vilken karta vill du använda? (0-{}): '.format(antal-1)))
                karta = kartor[index]
            except Exception:
                print('Felaktig inmatning')
            
            return self.db[karta]
        else:
            return self.ny()

    def ny(self):
        '''
        Skapar en ny karta.
        '''
        print('Gör en ny karta')

        tid = datetime.now()
        namn = tid.strftime("%Y-%m-%d %H:%M:%S")
        
        return self.db[namn]

    def spara(self, koordinater: list, position: tuple):
        '''
        Sparar en bunt koordinater som hör ihop med en viss karta i databasen.
        '''
        if self.karta:
            data = {'koordinater': koordinater, 'stegX': position[0], 'stegY': position[1]}
            return self.karta.insert_one(data)
        else:
            print('ingen karta har valts!')
    