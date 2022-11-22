from dataclasses import dataclass
from Model.House import House
from Model.Prefecture import Prefecture
from Model.Engineer_Post import Engineer_Post
from Model.Collapsed import Collapsed
from Model.Road import Road


@dataclass
class Building_Data:
    price: int


building_data = {House: Building_Data(10),
                 Prefecture: Building_Data(30),
                 Road: Building_Data(4),
                 Engineer_Post: Building_Data(30),
                 Collapsed: Building_Data(0)}
