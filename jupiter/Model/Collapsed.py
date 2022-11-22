from Model.Building import Building


class Collapsed(Building):

    def __init__(self, posx, posy, sizex=1, sizey=1):
        super().__init__(sizex, sizey, posx, posy, 0)

    def __repr__(self):
        return "Collapsed"
