class Koordinat:
    '''
    Lagrar information om en viss koordinat.
    '''
    def __init__(self, data: str):
        self.distans, self.vinkel, self.x, self.y = data.split(';', 3)
    