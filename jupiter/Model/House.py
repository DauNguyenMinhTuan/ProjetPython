from Model.Building import Building
from enum import Enum
from dataclasses import dataclass


class House_Level(Enum):
    # Les maisons avec un 2 a la fin sont les memes que sans mais plus grande
    # le jeu "fusionne" les maisons quand il y en a plusieurs pareil a coté
    # on verra pour l'implémenter après, je pense que c'est beaucoup de travail
    # pour pas grand chose
    Small_Tent = 1
    # Small_Tent2 = 2
    Large_Tent = 3
    # Large_Tent2 = 4
    Small_Shack = 5
    # Small_Shack2 = 6
    Large_Shack = 7
    # Large_Shack2 = 8
    # ...


@dataclass
class House_Property:
    # taille de la maison, carré de côté 'size'
    sizex: int
    sizey: int
    population: int


house_property = {House_Level.Small_Tent: House_Property(1, 1, 5),
                  # House_Level.Small_Tent2: House_Property(4, 20),
                  House_Level.Large_Tent: House_Property(1, 1, 7),
                  # House_Level.Large_Tent2: House_Property(4, 28),
                  House_Level.Small_Shack: House_Property(1, 1, 9),
                  # House_Level.Small_Shack2: House_Property(4, 36),
                  House_Level.Large_Shack: House_Property(1, 1, 11)
                  # House_Level.Large_Shack2: House_Property(4, 44)
                  }


class House(Building):

    def __init__(self, posx, posy):
        self.level = House_Level.Small_Tent
        self.population = house_property[self.level].population
        super().__init__(house_property[self.level].sizex,
                         house_property[self.level].sizey, posx, posy, job_offered=0)

    def __repr__(self):
        return "House"

    def evolve(self):
        # regarder dans 'house_property' pour modifier les attributs
        return

    def devolve(self):
        # regarder dans 'house_property' pour modifier les attributs
        return
