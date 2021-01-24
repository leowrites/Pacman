from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.grid import Grid
import pygame

UNIT_SIZE = 30


class Ghost:
    def __init__(self, x, y, image, aggression, game_window):
        self.game_window = game_window
        self.location = [x, y]
        self.spawn_location = (self.location[0] * UNIT_SIZE + 15, self.location[1] * UNIT_SIZE + 15)
        self.velocity_x = self.velocity_y = 1
        self.surface = image
        self.rect = self.surface.get_rect(center=self.spawn_location)
        self.aggression = aggression
        self.moving = True
        self.direction = 'right'
        self.mode = 'chasing'
        self.path = []

    def move(self, grid, pacman_location):
        # follows the path by multiplying next cord into pixels
        try:
            if not self.path:
                self.find_path(grid, pacman_location)
            next_x = self.path[0][0] * 30 + 15
            next_y = self.path[0][1] * 30 + 15
            if self.rect.centerx == next_x and self.rect.centery == next_y:
                self.path.remove(self.path[0])
            if self.rect.centerx < next_x:
                self.rect.centerx += self.velocity_x
            if self.rect.centerx > next_x:
                self.rect.centerx -= self.velocity_x
            if self.rect.centery > next_y:
                self.rect.centery -= self.velocity_y
            if self.rect.centery < next_y:
                self.rect.centery += self.velocity_y

            self.location[0] = round((self.rect.x-15)/30)
            self.location[1] = round((self.rect.y-15)/30)
        except IndexError:
            print("no path found")

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

    def find_path(self, grid, pacman_location):
        x = self.location[0]
        y = self.location[1]
        start = grid.node(x, y)
        end = grid.node(pacman_location[0], pacman_location[1])
        finder = AStarFinder()
        self.path, runs = finder.find_path(start, end, grid)
        print(self.path)
        print(grid.grid_str(path=self.path, start=start, end=end))
        Grid.cleanup(grid)

    def mode_select(self):
        pass

    def draw(self):
        self.game_window.blit(self.surface, self.rect)
