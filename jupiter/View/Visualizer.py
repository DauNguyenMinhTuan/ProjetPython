from operator import imod
import pygame as pg
import tkinter as tk
from Model.Engineer_Post import Engineer_Post
from Model.House import House
from Model.Map import Map, MAP_DIM
import Images as img
import sys, os
from Model.Prefecture import Prefecture
from Model.Road import Road
from Model.Collapsed import Collapsed
from random import randint

# Get full screen size
root = tk.Tk()
WINDOW_WIDTH = root.winfo_screenwidth()
WINDOW_HEIGHT = root.winfo_screenheight()

# Just colors
LIGHTGREY = (100, 100, 100)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
DGREEN = (55, 125, 35)
BLACK = (0, 0, 0)

# Size of cell according to zoom
cellSizeDict = {60: 30, 70: 35, 80: 40, 90: 45, 100: 50, 150: 75, 200: 100, 300: 150}
DEFAULT_ZOOM = 60

# Takes x and y cartesian coordinates and transform into isometrics ones
def cartToIso(point):
    isoX = point[0] - point[1]
    isoY = (point[0] + point[1]) / 2
    return [isoX, isoY]

class Visualizer:

    showGrid = False
    deplacementX = 0
    deplacementY = 0
    tmpDeplacementX = 0
    tmpDeplacementY = 0
    GAME_WIDTH = WINDOW_WIDTH
    GAME_HEIGHT = WINDOW_HEIGHT
    zoom = DEFAULT_ZOOM

    def __init__(self):
        # Create pygame window
        self.window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        return

    def update(self, map):
        # Edge of each cell of the grid is 20px in cartesian
        # self.zoom = 100
        cellSize = cellSizeDict[self.zoom]
        # Draw the tiles
        self.window.fill(BLACK)
        self.placeIsoTiles(cellSize, 
                        [self.GAME_HEIGHT / 2 + self.GAME_WIDTH / 4 - (cellSize * MAP_DIM) / 2
                        ,self.GAME_HEIGHT / 2 - self.GAME_WIDTH / 4 - (cellSize * MAP_DIM) / 2], 
                        map)
        # Then the grid
        if self.showGrid:
            self.drawIsometricGrid([self.GAME_HEIGHT / 2 + self.GAME_WIDTH / 4 - (cellSize * MAP_DIM) / 2,
                        self.GAME_HEIGHT / 2 - self.GAME_WIDTH / 4 - (cellSize * MAP_DIM) / 2],
                        MAP_DIM, cellSize)
        return

    def displayImage(self, mapRow, mapCol, tileDIM, origin, imgName, imgCode, compensateX, compensateY):
        originX = origin[0]
        originY = origin[1]
        scriptDir = sys.path[0]
        imagePath = os.path.join(scriptDir + '/Images/' + imgName + '_' + imgCode + '.png')
        displayImg = pg.image.load(imagePath)
        imgSize = (displayImg.get_width() * self.zoom / DEFAULT_ZOOM,
                    displayImg.get_height() * self.zoom / DEFAULT_ZOOM)
        displayImg = pg.transform.scale(displayImg, imgSize)
        coordinates = cartToIso([originX + (tileDIM * mapRow), originY + (tileDIM * mapCol)])
        coordinates[0] -= compensateX
        coordinates[1] -= compensateY
        coordinates[0] += self.deplacementX + self.tmpDeplacementX
        coordinates[1] += self.deplacementY + self.tmpDeplacementY
        self.window.blit(displayImg, (coordinates[0], coordinates[1]))

    # Display the tiles(cells) of the map
    # self is the display, cellSize is length of each cell, origin is 2D coordinates of the origin,
    # Map is the table of value of each cell
    def placeIsoTiles(self, cellSize, origin, MAP):
        tileDIM = cellSize
        originX, originY = origin[0], origin[1]
        for row in range(MAP_DIM):
            for column in range(MAP_DIM):
                # We display differently for each value of map cell
                match MAP[column][row]:
                    case 0: # test value
                        tilePoints = [  
                                    cartToIso([originX + (tileDIM * row), originY + (tileDIM * column)]),
                                    cartToIso([originX + (tileDIM * (row + 1)), originY + (tileDIM * column)]),
                                    cartToIso([originX + (tileDIM * (row + 1)), originY + (tileDIM * (column + 1))]),
                                    cartToIso([originX + (tileDIM * row), originY + (tileDIM * (column + 1))])
                                    ]
                        pg.draw.polygon(self.window, GREEN, tilePoints, )
                    case House():
                        if MAP[column][row].burning:
                            imgName = 'Collapsed'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = 0
                            self.displayImage(row, column, tileDIM, origin, imgName, imgCode, compenX, compenY)
                            imgName = 'Burning'
                            imgCode = f'0000{randint(1, 8)}'
                            compenX = cellSize / 2
                            compenY = cellSize / 4
                        else:
                            imgName = 'SmallTent'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = 0
                        self.displayImage(row, column, tileDIM, origin, imgName, imgCode, compenX, compenY)
                    case 'Grass':
                        imgName = 'Grass'
                        imgCode = '00010'
                        compenX = cellSize
                        compenY = 0
                        self.displayImage(row, column, tileDIM, origin, imgName, imgCode, compenX, compenY)
                    case Prefecture():
                        if MAP[column][row].burning:
                            imgName = 'Collapsed'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = 0
                            self.displayImage(row, column, tileDIM, origin, imgName, imgCode, compenX, compenY)
                            imgName = 'Burning'
                            imgCode = f'0000{randint(1, 8)}'
                            compenX = cellSize / 2
                            compenY = cellSize / 4
                        else:
                            imgName = 'Prefecture'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = cellSize / 4
                        self.displayImage(row, column, tileDIM, origin, imgName, imgCode, compenX, compenY)
                    case Road():
                        roadType = 0
                        roadType += 1 if (column > 0 and isinstance(MAP[column - 1][row], Road)) else 0
                        roadType += 2 if (row > 0 and isinstance(MAP[column][row - 1], Road)) else 0
                        roadType += 4 if (column < MAP_DIM and isinstance(MAP[column + 1][row], Road)) else 0
                        roadType += 8 if (row < MAP_DIM and isinstance(MAP[column][row + 1], Road)) else 0
                        if roadType == 0:
                            roadType = 5
                        imgCode = '000' + (f'0{roadType}' if roadType < 10 else f'{roadType}')
                        imgName = 'Road'
                        compenX = cellSize
                        compenY = 0
                        self.displayImage(row, column, tileDIM, origin, imgName, imgCode, compenX, compenY)
                    case Collapsed():
                        imgName = 'Collapsed'
                        imgCode = '00001'
                        compenX = cellSize
                        compenY = 0
                        self.displayImage(row, column, tileDIM, origin, imgName, imgCode, compenX, compenY)
                    case Engineer_Post():
                        if MAP[column][row].burning:
                            imgName = 'Collapsed'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = 0
                            self.displayImage(row, column, tileDIM, origin, imgName, imgCode, compenX, compenY)
                            imgName = 'Burning'
                            imgCode = f'0000{randint(1, 8)}'
                            compenX = cellSize / 2
                            compenY = cellSize / 4
                        else:
                            imgName = 'EngineerPost'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = cellSize * 3 / 4
                        self.displayImage(row, column, tileDIM, origin, imgName, imgCode, compenX, compenY)

    # Display the grid of the map
    # self: display, origin: 2D coordinates of origin, size: map's dimension
    # cellSize: edge's length of cell
    def drawIsometricGrid(self, origin, size, cellSize):
        hw = cellSize * size
        gridColor = BLUE
        borderPoints = [cartToIso(origin),
                        cartToIso([origin[0], origin[1] + hw]),
                        cartToIso([origin[0] + hw, origin[1] + hw]),
                        cartToIso([origin[0] + hw, origin[1]])]
        for bP in borderPoints:
            bP[0] += self.deplacementX + self.tmpDeplacementX - 1
            bP[1] += self.deplacementY + self.tmpDeplacementY - 1
        # Draw grid's border
        pg.draw.polygon(self.window, gridColor, borderPoints, 2)
        # Draw inner lines
        for colRow in range(1, size):
            dim = cellSize * colRow
            start_point = cartToIso([origin[0], origin[1] + dim])
            start_point[0] += self.deplacementX + self.tmpDeplacementX - 1
            start_point[1] += self.deplacementY + self.tmpDeplacementY - 1
            end_point = cartToIso([hw + origin[0], origin[1] + dim])
            end_point[0] += self.deplacementX + self.tmpDeplacementX - 1
            end_point[1] += self.deplacementY + self.tmpDeplacementY - 1 
            pg.draw.line(self.window, gridColor, start_point, end_point, 1)
            start_point = cartToIso([origin[0] + dim, origin[1]])
            start_point[0] += self.deplacementX + self.tmpDeplacementX - 1
            start_point[1] += self.deplacementY + self.tmpDeplacementY - 1
            end_point = cartToIso([origin[0] + dim, origin[1] + hw])
            end_point[0] += self.deplacementX + self.tmpDeplacementX - 1
            end_point[1] += self.deplacementY + self.tmpDeplacementY - 1
            pg.draw.line(self.window, gridColor, start_point, end_point, 1)
