import pygame
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.grid import Grid
import numpy as np

UNIT_SIZE = 30
WALL_COLOR = pygame.Color(0, 0, 128)
TILE_SIZE = (30, 30)


class Pacman:
    # static variables for all pacman
    cur_location_on_grid = [10, 14]
    # this is for showing the pacman
    velocity_x = 1
    velocity_y = 1
    direction = "up"
    is_super = False

    def __init__(self, game_map, game_window, image):
        self.RIGHT = True
        self.LEFT = False
        self.UP = False
        self.DOWN = False

        self.moving = True
        self.alive = True

        self.radars = []
        self.distance = []
        self.score = 0
        self.winning = False
        self.distance_traveled = 0
        self.game_map = game_map
        self.image = image
        self.current_image = 1
        self.mode = 'normal'
        self.coins = np.zeros((20, 20), dtype=pygame.Rect)
        self.total_coins = 0
        self.rect = self.image[1].get_rect(
            center=(self.cur_location_on_grid[0] * UNIT_SIZE + 15, self.cur_location_on_grid[1] * UNIT_SIZE + 15))

        # this is used to locate the pacman on the grid
        self.game_window = game_window

    def spawn_coins(self, COIN_IMAGE):
        self.total_coins = np.sum(1 - self.game_map)
        for y, rows in enumerate(self.game_map):
            for x in range(len(rows)):
                # coin cannot spawn inside jail?
                current = self.game_map[y][x]
                current_location = (
                    x * TILE_SIZE[0] + 15, y * TILE_SIZE[1] + 15)
                if current == 1:
                    self.coins[y][x] = COIN_IMAGE.get_rect(
                        center=current_location)

    def draw_coins(self, coins, COIN_IMAGE):
        for y, rows in enumerate(coins):
            for x in range(len(rows)):
                current = coins[y][x]
                current_location = (
                    x * TILE_SIZE[0] + 15, y * TILE_SIZE[1] + 15)
                rect = COIN_IMAGE.get_rect(center=current_location)
                # creating the surface
                if current != 0:
                    self.game_window.blit(COIN_IMAGE, rect)

    def move(self, direction, fitness):
        # need to map the pacman's location to the cell on a map
        # we can use a for loop to detect if the pacman collides with a block that has a value 1
        self.direction = direction
        if self.moving:
            if direction == 'right':
                self.rect.x += self.velocity_x
            elif direction == 'left':
                self.rect.x -= self.velocity_x
            elif direction == 'up':
                self.rect.y -= self.velocity_y
            elif direction == 'down':
                self.rect.y += self.velocity_y
            fitness += 0.05
            return fitness
        return fitness

    def eat_cherry(self, cherry_rects):
        """
        eat a cherry and become super
        :param cherry_rects: cherry rectangles
        :return: new cherry rectangles
        """
        for cherry_rect in cherry_rects:
            if pygame.rect.Rect.colliderect(self.rect, cherry_rect):
                self.mode = 'eat ghost'
                self.score += 500
                cherry_rects.remove(cherry_rect)
        return cherry_rects

    def radar(self, direction, pixel):

        length = 0
        x = int(self.rect.centerx)
        y = int(self.rect.centery)

        if direction == 'right':
            while not pixel.get_at((x, y)) == (0, 0, 128) and length < 150:
                length += 1
                x = int(self.rect.centerx + length)
            distance = abs(x - self.rect.centerx)
            self.radars.append([(x, y), distance])
        if direction == 'left':
            while not pixel.get_at((x, y)) == (0, 0, 128) and length < 150:
                length += 1
                x = int(self.rect.centerx - length)
            distance = abs(self.rect.centerx - x)
            self.radars.append([(x, y), distance])
        if direction == 'up':
            while not pixel.get_at((x, y)) == (0, 0, 128) and length < 150:
                length += 1
                y = int(self.rect.centery - length)
            distance = abs(self.rect.centery - y)
            self.radars.append([(x, y), distance])
        if direction == 'down':
            while not pixel.get_at((x, y)) == (0, 0, 128) and length < 150:
                length += 1
                y = int(self.rect.centery + length)
            distance = abs(y - self.rect.centery)
            self.radars.append([(x, y), distance])

    def get_data(self):
        radars = self.radars
        ret = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i, r in enumerate(radars):
            ret[i] = int(r[1])
        for x in range(4):
            ret[4+x] = self.distance[x]
        return ret

    def get_pixel_ahead(self, ahead=1):
        xy_ahead_a = []
        xy_ahead_b = []
        if self.direction == "right":
            xy_ahead_a = (self.rect.topright[0] + ahead, self.rect.topright[1])
            xy_ahead_b = (
                self.rect.bottomright[0] + ahead, self.rect.bottomright[1])
        if self.direction == "left":
            xy_ahead_a = (self.rect.topleft[0] - ahead, self.rect.topleft[1])
            xy_ahead_b = (
                self.rect.bottomleft[0] - ahead, self.rect.bottomleft[1])
        if self.direction == "up":
            xy_ahead_a = (self.rect.topright[0], self.rect.topright[1] - ahead)
            xy_ahead_b = (self.rect.topleft[0], self.rect.topleft[1] - ahead)
        if self.direction == "down":
            xy_ahead_a = (
                self.rect.bottomright[0], self.rect.bottomright[1] + ahead)
            xy_ahead_b = (
                self.rect.bottomleft[0], self.rect.bottomleft[1] + ahead)
        return xy_ahead_a, xy_ahead_b

    def movement_restrictions(self):
        xy_ahead_a, xy_ahead_b = self.get_pixel_ahead()
        color_ahead_a = self.game_window.get_at(xy_ahead_a)
        color_ahead_b = self.game_window.get_at(xy_ahead_b)
        # if both color are channel, then moving is true, else its false
        if color_ahead_a == WALL_COLOR or color_ahead_b == WALL_COLOR:
            self.moving = False
            self.alive = False
        return color_ahead_b, color_ahead_b

    def eat_coin(self):
        # if collides, return true and remove the coin
        for y, rows in enumerate(self.coins):
            for x in range(len(rows)):
                this_coin = self.coins[y][x]
                if this_coin != 0:
                    if pygame.Rect.colliderect(self.rect, this_coin):
                        self.coins[y][x] = 0
                        self.total_coins -= 1
                        self.score += 100
                        return True
        return False

    def win(self):
        if self.total_coins == 14:
            self.winning = True

    def is_alive(self, ghosts):
        """
        :param ghost_rect: a list of ghost rectangles to be looped through to check if collides with pacman
        :return: nothing
        """
        for ghost in ghosts:
            if pygame.rect.Rect.colliderect(self.rect, ghost.rect):
                if self.mode == 'eat ghost':
                    self.score += 2000
                    ghosts.remove(ghost)
                    return ghosts, ghost
                else:
                    self.alive = False
                    return ghosts, None
        return ghosts, None

    def draw_radar(self):
        for r in self.radars:
            pos, dest = r
            pygame.draw.line(self.game_window, (0, 255, 0), (self.rect.centerx, self.rect.centery), pos, 1)

    def draw(self, COIN_IMAGE):
        self.game_window.blit(self.image[self.current_image], self.rect)
        self.draw_coins(self.coins, COIN_IMAGE)

    def distance_to_ghost(self, ghosts, grid):
        self.distance.clear()
        if ghosts is not None:
            for ghost in ghosts:
                d = self.find_path(grid, ghost.get_location())
                self.distance.append(d)

    def find_path(self, grid, final):
        x = round((self.rect.centerx - 15) / 30)
        y = round((self.rect.centery - 15) / 30)
        start = grid.node(x, y)
        end = grid.node(final[0], final[1])
        finder = AStarFinder()
        path, runs = finder.find_path(start, end, grid)
        Grid.cleanup(grid)
        return len(path)
