from Model.Building import Building
from Model.Prefect import Prefect


class Prefecture(Building):

    def __init__(self, posx, posy):
        # size 1
        super().__init__(1, 1, posx, posy, job_offered=6)
        self.prefect = Prefect(self, self.road_connection)

    def __repr__(self):
        return "Prefecture"
