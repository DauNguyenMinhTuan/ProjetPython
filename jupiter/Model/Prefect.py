from Model.Random_Worker import Random_Worker


class Prefect(Random_Worker):

    def __init__(self, prefecture, spawn_road):
        # long patrol 52 tiles
        # short patrol 43 tiles
        super().__init__(52, 43, spawn_road)
        self.prefecture = prefecture
        self.spawn()

    def spawn(self):
        return
