from math import radians

class Koordinat:
    '''
    Lagrar information om en viss koordinat.
    '''
    def __init__(self, data: str):
        self.distans, self.vinkel, self.x, self.y = *map(int, data.split(';')),
        self.vinkel = radians(self.vinkel)