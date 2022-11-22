
from Model.Road import Road
from Model.House import House

MAP_DIM = 20


class Map:

    def __init__(self):
        self.grid = [['Grass' for column in range(MAP_DIM)] for row in range(MAP_DIM)]
        self.sizex = 20
        self.sizey = 20

    def __str__(self):
        string = ""
        for row in self.grid:
            string += str(row) + "\n"
        return string

    def build(self, posx, posy, type):
        # print(posx, ' ', posy)
        self.grid[posx][posy] = type(posx, posy)
        return

    def destroy(self, posx, posy):
        self.grid[posx][posy] = 'Grass'
        return

    def is_type(self, posx, posy, t):
        if posx < 0 or posx >= self.sizex or posy < 0 or posy >= self.sizey:
            return False
        return type(self.grid[posx][posy]) == t

    def road_connection(self, building):
        # Houses can be 1 tile away from the road
        for d in range(2 if isinstance(building, House) else 1):
            for y in range(building.posy, building.posy + building.sizey):
                if self.is_type(building.posx - d - 1, y, Road):
                    return self.grid[building.posx - d - 1][y]
            for x in range(building.posx, building.posx + building.sizex):
                if self.is_type(x, building.posy - d - 1, Road):
                    return self.grid[x][building.posy - d - 1]
            for y in range(building.posy, building.posy + building.sizey):
                if self.is_type(building.posx + building.sizex + d, y, Road):
                    return self.grid[building.posx + building.sizex + d][y]
            for x in range(building.posx, building.posx + building.sizex):
                if self.is_type(x, building.posy + building.sizey + d, Road):
                    return self.grid[x][building.posy + building.sizey + d]
        return None
