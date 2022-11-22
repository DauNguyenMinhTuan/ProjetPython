from Model.Worker import Worker


class Random_Worker(Worker):

    def __init__(self, long_patrol, short_patrol, spawn_road):
        super().__init__()
        self.speed = 640  # tiles per year
        self.long_patrol = long_patrol
        self.short_patrol = short_patrol
        self.long_patrol_probability = 1 / 4
        self.spawn_road = spawn_road
