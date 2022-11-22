from Model.Random_Worker import Random_Worker


class Engineer(Random_Worker):

    def __init__(self, post, spawn_road):
        # long patrol 52 tiles
        # short patrol 43 tiles
        super().__init__(52, 43, spawn_road)
        self.post = post
        self.spawn()

    def spawn(self):
        return
