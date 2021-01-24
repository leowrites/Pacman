import random
import pygame
import numpy as np

UNIT_SIZE = 30


class Pacman:
    # static variables for all pacman
    cur_location_on_grid = [0, 0]
    # this is for showing the pacman
    velocity_x = 1
    velocity_y = 1
    direction = "right"
    is_super = False

    def __init__(self, game_map, game_window, image):
        self.RIGHT = True
        self.LEFT = False
        self.UP = False
        self.DOWN = False
        self.moving = True
        self.score = 0
        self.game_map = game_map
        self.spawn()
        self.image = image
        self.current_image = 1
        self.alive = True
        self.rect = self.image[1].get_rect(
            center=(self.cur_location_on_grid[0] * UNIT_SIZE + 15, self.cur_location_on_grid[1] * UNIT_SIZE + 15))

        # this is used to locate the pacman on the grid
        self.game_window = game_window

    def move(self):
        # need to map the pacman's location to the cell on a map
        # we can use a for loop to detect if the pacman collides with a block that has a value 1
        if self.RIGHT:
            self.rect.x += self.velocity_x
        elif self.LEFT:
            self.rect.x -= self.velocity_x
        elif self.UP:
            self.rect.y -= self.velocity_y
        elif self.DOWN:
            self.rect.y += self.velocity_y

    def transform_image(self, direction):
        pass

    def check_collision(self, ghost_rect):
        pass

    def get_pixel_ahead(self, ahead=1):
        xy_ahead_a = []
        xy_ahead_b = []
        if self.direction == "right":
            xy_ahead_a = (self.rect.topright[0] + ahead, self.rect.topright[1])
            xy_ahead_b = (self.rect.bottomright[0] + ahead, self.rect.bottomright[1])
        if self.direction == "left":
            xy_ahead_a = (self.rect.topleft[0] - ahead, self.rect.topleft[1])
            xy_ahead_b = (self.rect.bottomleft[0] - ahead, self.rect.bottomleft[1])
        if self.direction == "up":
            xy_ahead_a = (self.rect.topright[0], self.rect.topright[1] - ahead)
            xy_ahead_b = (self.rect.topleft[0], self.rect.topleft[1] - ahead)
        if self.direction == "down":
            xy_ahead_a = (self.rect.bottomright[0], self.rect.bottomright[1] + ahead)
            xy_ahead_b = (self.rect.bottomleft[0], self.rect.bottomleft[1] + ahead)
        return xy_ahead_a, xy_ahead_b

    def spawn(self):
        """
        generates a valid spawn location
        :return:
        """
        self.cur_location_on_grid = [random.randint(0, 19), random.randint(0, 19)]
        while self.game_map[self.cur_location_on_grid[1]][self.cur_location_on_grid[0]] == 0:
            self.spawn()

    def eat_coin(self, coin_rects):
        # if collides, return true and remove the coin
        for y, rows in enumerate(coin_rects):
            for x in range(len(rows)):
                this_coin = coin_rects[y][x]
                if this_coin != 0:
                    if pygame.Rect.colliderect(self.rect, this_coin):
                        coin_rects[y][x] = 0
                        self.score += 100
                        return coin_rects
        return coin_rects

    def is_alive(self, ghost_rect):
        """
        :param ghost_rect: a list of ghost rectangles to be looped through to check if collides with pacman
        :return: nothing
        """
        if pygame.rect.Rect.colliderect(self.rect, ghost_rect):
            self.alive = False

    def draw(self):
        self.game_window.blit(self.image[self.current_image], self.rect)
