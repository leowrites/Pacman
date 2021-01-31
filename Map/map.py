import numpy as np
import pygame

TILE_SIZE = (30, 30)
WALL_SIZE = (20, 20)
COIN_SIZE = (15, 15)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
WALL_BLUE = pygame.Color(0, 0, 128)


class Map:
    """
    creates a map object
    """
    cherry_cord1 = [2, 4]
    cherry_cord2 = [4, 16]
    cherry_cord3 = [15, 2]
    cherry_cord4 = [16, 16]
    cherry_location = [cherry_cord1, cherry_cord2, cherry_cord3, cherry_cord4]
    map_array = np.array(
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
         [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
         [0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0],
         [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
         [0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0],
         [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
         [0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0],
         [0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
         [0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
         [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
         [0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
         [0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
         [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    )
    coins = np.zeros((20, 20), dtype=pygame.Rect)

    def __init__(self, game):
        """
        use the game to draw on its screen
        load the images
        :param game: a game window
        """
        self.window = game

    def spawn_cherry_rects(self, CHERRY_IMAGE):
        cherry_rects = []
        for cherry_cord in self.cherry_location:
            current_location = (
                cherry_cord[0] * TILE_SIZE[0] + 15, cherry_cord[1] * TILE_SIZE[1] + 15)
            rect = CHERRY_IMAGE.get_rect(center=current_location)
            cherry_rects.append(rect)
        return cherry_rects

    def draw_cherry(self, cherrys, CHERRY_IMAGE):
        for cherry_cord in cherrys:
            self.window.blit(CHERRY_IMAGE, cherry_cord)

    def draw_map(self):
        for y, rows in enumerate(self.map_array):
            for x in range(len(rows)):
                current = self.map_array[y][x]
                current_rect = (x * TILE_SIZE[0] + 15, y * TILE_SIZE[1] + 15)
                surface = pygame.Surface(TILE_SIZE)
                rect = surface.get_rect(center=current_rect)
                # creating the surface
                if current == 1:
                    pygame.draw.rect(surface, BLACK, surface.get_rect())
                    self.window.blit(surface, rect)
                elif current == 0:
                    pygame.draw.rect(surface, WALL_BLUE, surface.get_rect())
                    self.window.blit(surface, rect)
