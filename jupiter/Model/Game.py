from Model.Map import Map
from Model.House import House
from Model.Collapsed import Collapsed
# from Model.Prefecture import Prefecture
from Model.Road import Road
from Model.Models_Data import building_data
from random import seed
from datetime import datetime, timedelta


# min par frame
TIME_PER_FRAME = 50


class Game:

    def __init__(self, denarii):
        self.map = Map()
        self.wheat = 0
        self.denarii = denarii
        self.population = 0
        self.unemployed = 0
        self.workers = []
        self.buildings = []
        # TODO la date commence a -340 normalement mais python ne prends les date qu'a
        # partir de 1
        self.date = datetime(1, 1, 1)

    def __str__(self):
        string = str(self.map)
        string += f"\nDenarii: {self.denarii}"
        string += f"\nUnemployed: {self.unemployed}/{self.population}"
        for w in self.workers:
            string += f"\n{w}"
        for b in self.buildings:
            string += f"\n{b}"
        return string

    def pay(self):
        return

    def build(self, posx, posy, type):
        assert type in building_data, "type to build not in 'model_data'"

        if self.map.grid[posx][posy] != 'Grass':
            return

        if building_data[type].price <= self.denarii:
            self.denarii -= building_data[type].price
        else:
            return

        self.map.build(posx, posy, type)

        building = self.map.grid[posx][posy]

        if type == House:
            additional_population = building.population
            self.population += additional_population
            self.unemployed += additional_population

        if type == Road:
            # check every building for road connection
            self.road_connect()
        else:
            # only check for the new building because it doesn't impact the others
            self.road_connect([building])

        self.buildings.append(building)

    def destroy(self, posx, posy):
        building = self.map.grid[posx][posy]
        if building == 'Grass':
            return

        building_type = type(building)
        if building_type == House:
            removed_population = building.population
            self.population -= removed_population
            self.unemployed -= removed_population
        self.unemployed += building.employees

        self.buildings.remove(building)

        self.map.destroy(posx, posy)

        if building_type == Road:
            self.road_connect()
            for w in self.workers:
                if w.spawn_road == building:
                    # TODO respawn a new one because his spawn point (=end point)
                    # got destroyed
                    pass

    def job_hunt(self):
        if self.unemployed < 0:
            # a house got destroyed and its inhabitant were working, we need to
            # remove them inhabitants from where they were working
            for b in reversed(self.buildings):
                if self.unemployed == 0:
                    break
                if b.employees > 0:
                    new_unemployed = b.employees \
                        if b.employees > -self.unemployed else -self.unemployed
                    b.employees -= new_unemployed
                    self.unemployed += new_unemployed
        else:
            # we have unemployed peoples, let's search if they can work anywhere
            for b in self.buildings:
                if self.unemployed == 0:
                    break
                if b.offer_jobs():
                    new_employees = b.job_offered - b.employees if b.job_offered -\
                        b.employees <= self.unemployed else self.unemployed
                    b.employees += new_employees
                    self.unemployed -= new_employees

    def road_connect(self, buildings=None):
        # hack because we can't use 'self' in the default value
        if buildings is None:
            buildings = self.buildings
        for b in buildings:
            if isinstance(b, Road):
                continue
            b.road_connection = self.map.road_connection(b)

    def burn(self):
        seed()  # random.seed
        for b in self.buildings:
            if isinstance(b, Road) or isinstance(b, Collapsed):
                continue
            if b.burn(self.date):
                posx, posy = b.posx, b.posy
                self.destroy(posx, posy)
                self.build(posx, posy, Collapsed)

    def collapse(self):
        seed()  # random.seed
        for b in self.buildings:
            if isinstance(b, Road) or isinstance(b, Collapsed):
                continue
            if b.collapse():
                posx, posy = b.posx, b.posy
                self.destroy(posx, posy)
                self.build(posx, posy, Collapsed)

    def advance_time(self):
        delta = timedelta(minutes=TIME_PER_FRAME)
        self.date += delta

    def save(self):
        return
