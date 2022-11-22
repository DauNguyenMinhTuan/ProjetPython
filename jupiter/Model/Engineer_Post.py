from Model.Building import Building
from Model.Engineer import Engineer


class Engineer_Post(Building):

    def __init__(self, posx, posy):
        # size 1
        super().__init__(1, 1, posx, posy, job_offered=6)
        self.engineer = Engineer(self, self.road_connection)

    def __repr__(self):
        return "Engineer_Post"
