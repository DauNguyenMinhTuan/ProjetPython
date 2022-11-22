from datetime import timedelta
from random import random


COLLAPSE_PROBABILITY = 0.005
BURN_PROBABILITY = 0.005
STAGES_BEFORE_BURN = 5
STAGES_BEFORE_COLLAPSE = 5

# in hours
BURNING_TIME_BEFORE_COLLAPSE = 5 * 24


class Building:

    def __init__(self, sizex, sizey, posx, posy, job_offered):
        self.sizex = sizex
        self.sizey = sizey
        self.burn_stage = 0
        self.collapse_stage = 0
        self.posx = posx
        self.posy = posy
        self.employees = 0
        self.job_offered = job_offered
        # ONE of the road by which the building is connected, None if not connected
        self.road_connection = None
        self.burning = False
        self.burning_start = None
        self.collapsed = False

    def __str__(self):
        string = self.__repr__()
        string += f" ({self.posx}, {self.posy})"
        string += f"\n\tBurn stage: {self.burn_stage}"
        string += f"\n\tCollapse stage: {self.collapse_stage}"
        string += f"\n\tJobs: {self.employees}/{self.job_offered}"
        string += "\n\tRoad connections: "
        if self.road_connection:
            string += f"({self.road_connection.posx}, {self.road_connection.posy})"
        else:
            string += "None"
        return string

    # return True if collapsing, else False
    def burn(self, time):
        if not self.burning:
            self.burn_stage += 1 if random() < BURN_PROBABILITY else 0
            if self.burn_stage > STAGES_BEFORE_BURN:
                self.burning = True
                self.burning_start = time
        else:
            if time - self.burning_start > timedelta(hours=BURNING_TIME_BEFORE_COLLAPSE):
                return True

        return False

    def put_out_fire(self):
        self.burning = False
        self.burning_start = None

    # return True if collapsing, else False
    def collapse(self):
        self.collapse_stage += 1 if random() < COLLAPSE_PROBABILITY else 0
        return self.collapse_stage > STAGES_BEFORE_COLLAPSE

    def employ(self):
        return

    def offer_jobs(self):
        return self.employees < self.job_offered
