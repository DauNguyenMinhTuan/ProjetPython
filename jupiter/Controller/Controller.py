from Model.Map import MAP_DIM
from View.Visualizer import Visualizer, cellSizeDict
from Model.Game import Game
from Model.House import House
from Model.Prefecture import Prefecture
from Model.Engineer_Post import Engineer_Post
from Model.Road import Road
from Model.Collapsed import Collapsed
import pygame as pg
from datetime import date, timedelta
from time import time_ns, sleep

FRAMES_PER_SECONDS = 20
TIME_NS_PER_FRAME = 1 / FRAMES_PER_SECONDS * 1e9

class Controller:

    MODE_DECALAGE = False
    ORIGIN_DECALAGE = (0, 0)

    def __init__(self):
        pg.init()
        self.visualizer = Visualizer()
        self.game = Game(10000)
        self.last_frame = time_ns()
        self.run()

    def run(self):
        self.game.build(0, MAP_DIM - 1, Prefecture)
        self.game.build(0, 0, House)
        self.game.build(1, 1, Road)
        self.game.build(1, 2, Road)
        self.game.build(1, 3, Road)
        self.game.build(2, 3, Road)
        self.game.build(2, 4, Road)
        self.game.build(3, 3, Road)
        self.game.build(10, 10, Road)
        self.game.build(10, 0, Engineer_Post)
        self.game.build(15, 15, Prefecture)
        self.game.build(15, 16, House)
        self.game.build(15, 17, Prefecture)
        self.game.build(15, 18, Prefecture)
        while True:
            self.game.advance_time()
            self.checkEvents()

            self.game.burn()
            self.game.collapse()

            self.visualizer.update(self.game.map.grid)
            pg.display.update()

            self.wait_next_frame()

        print(self.game)

        return

    def wait_next_frame(self):
        time_now = time_ns()
        delta = time_now - self.last_frame
        sleep_time = TIME_NS_PER_FRAME - delta if TIME_NS_PER_FRAME - delta > 0 else 0
        sleep(sleep_time * 1e-9)
        self.last_frame = time_ns()

    def checkEvents(self):
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    print("Trying to exit...")
                    pg.quit()
                    exit()
                case pg.KEYDOWN:
                    print("Pressed ", event.unicode)
                case pg.KEYUP:
                    print("Released ", event.unicode)
                case pg.MOUSEBUTTONDOWN:
                    if event.button == pg.BUTTON_LEFT:
                        # print("Left button pressed at (x, y) = ", event.pos)
                        if event.pos[0] <= self.visualizer.GAME_WIDTH and event.pos[1] <= self.visualizer.GAME_HEIGHT:
                            self.MODE_DECALAGE = True
                            self.ORIGIN_DECALAGE = event.pos
                    elif event.button == pg.BUTTON_RIGHT:
                        print("Right button pressed at (x, y) = ", event.pos)
                case pg.MOUSEBUTTONUP:
                    if event.button == pg.BUTTON_LEFT:
                        # print("Left button released at (x, y) = ", event.pos)
                        if self.MODE_DECALAGE:
                            self.MODE_DECALAGE = False
                            mouse_pos = event.pos
                            self.visualizer.tmpDeplacementX = mouse_pos[0] - self.ORIGIN_DECALAGE[0]
                            self.visualizer.tmpDeplacementY = mouse_pos[1] - self.ORIGIN_DECALAGE[1]
                            self.visualizer.deplacementX += self.visualizer.tmpDeplacementX
                            self.visualizer.deplacementY += self.visualizer.tmpDeplacementY
                            self.visualizer.tmpDeplacementX = 0
                            self.visualizer.tmpDeplacementY = 0
                    elif event.button == pg.BUTTON_RIGHT:
                        print("Right button released at (x, y) = ", event.pos)
                case pg.MOUSEMOTION:
                    if self.MODE_DECALAGE:
                        mouse_pos = event.pos
                        self.visualizer.tmpDeplacementX = mouse_pos[0] - self.ORIGIN_DECALAGE[0]
                        self.visualizer.tmpDeplacementY = mouse_pos[1] - self.ORIGIN_DECALAGE[1]
                case pg.MOUSEWHEEL:
                    if not self.MODE_DECALAGE and event.y != 0:
                        if event.y > 0:
                            # zoom in
                            new_zoom_percentage = max(cellSizeDict.keys())
                            for zoom_percentage in cellSizeDict.keys():
                                if zoom_percentage > self.visualizer.zoom and zoom_percentage < new_zoom_percentage:
                                    new_zoom_percentage = zoom_percentage
                            if new_zoom_percentage != self.visualizer.zoom:
                                self.visualizer.deplacementX = self.visualizer.deplacementX * new_zoom_percentage / self.visualizer.zoom
                                self.visualizer.deplacementY = self.visualizer.deplacementY * new_zoom_percentage / self.visualizer.zoom
                        else:
                            # zoom out
                            new_zoom_percentage = min(cellSizeDict.keys())
                            for zoom_percentage in cellSizeDict.keys():
                                if zoom_percentage < self.visualizer.zoom and zoom_percentage > new_zoom_percentage:
                                    new_zoom_percentage = zoom_percentage
                            if new_zoom_percentage != self.visualizer.zoom:
                                # self.visualizer.deplacementX += self.visualizer.GAME_WIDTH / 4
                                # self.visualizer.deplacementY += self.visualizer.GAME_HEIGHT / 4
                                self.visualizer.deplacementX *= new_zoom_percentage
                                self.visualizer.deplacementY *= new_zoom_percentage
                                self.visualizer.deplacementX /= self.visualizer.zoom
                                self.visualizer.deplacementY /= self.visualizer.zoom
                        self.visualizer.zoom = new_zoom_percentage
                case _:
                    # print(pg.event.event_name(event.type), "occured")
                    break
