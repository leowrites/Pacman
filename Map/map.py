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
    game_map = np.array(
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
         [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
         [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
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

    def spawn_coins(self, COIN_IMAGE):
        """
        spawn the coins
        :return: coins array, total number of coins, coin rectangles stored in a list
        """
        counter = 0
        total_coins = np.sum(1 - self.game_map)
        for y, rows in enumerate(self.game_map):
            for x in range(len(rows)):
                counter += 1
                current = self.game_map[y][x]
                current_location = (x * TILE_SIZE[0] + 15, y * TILE_SIZE[1] + 15)
                if current == 1:
                    self.coins[y][x] = COIN_IMAGE.get_rect(center=current_location)
        return self.coins, total_coins

    def draw_coins(self, coins, COIN_IMAGE):
        for y, rows in enumerate(coins):
            for x in range(len(rows)):
                current = coins[y][x]
                current_location = (x * TILE_SIZE[0] + 15, y * TILE_SIZE[1] + 15)
                rect = COIN_IMAGE.get_rect(center=current_location)
                # creating the surface
                if current != 0:
                    self.window.blit(COIN_IMAGE, rect)

    def draw_map(self):
        for y, rows in enumerate(self.game_map):
            for x in range(len(rows)):
                current = self.game_map[y][x]
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
