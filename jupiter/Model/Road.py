from Model.Building import Building


class Road(Building):

    def __init__(self, posx, posy):
        super().__init__(1, 1, posx, posy, job_offered=0)
        self.road_connection = self

    def __repr__(self):
        return "Road"
