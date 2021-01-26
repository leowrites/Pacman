from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.grid import Grid
from pygame import Color

UNIT_SIZE = 30
WALL_COLOR = Color(0, 0, 128)


class Ghost:
    def __init__(self, location, image, aggression, game_window, mode):
        self.location = location
        self.image = image
        self.aggression = aggression
        self.game_window = game_window
        self.mode = mode
        self.moving = True
        self.surface = image
        self.velocity_x = self.velocity_y = 1
        self.game_window = game_window
        self.direction = 'right'
        self.spawn_location = (self.location[0] * UNIT_SIZE + 15, self.location[1] * UNIT_SIZE + 15)
        self.rect = self.surface.get_rect(center=self.spawn_location)
        self.path = []
        self.name = ''
        self.aim = []

    def mode_select(self, pacman_state):
        if pacman_state == 'super':
            self.mode = 'hide'
        else:
            self.mode = 'chase'

    def draw(self):
        self.game_window.blit(self.surface, self.rect)

    def find_path(self, grid, final):
        x = self.location[0]
        y = self.location[1]
        start = grid.node(x, y)
        end = grid.node(final[0], final[1])
        finder = AStarFinder()
        self.path, runs = finder.find_path(start, end, grid)
        print(str(self.path) + self.name)
        Grid.cleanup(grid)

    def move(self, grid, final):
        # follows the path by multiplying next cord into pixels
        try:
            if not self.path:
                self.find_path(grid, final)
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

            self.location[0] = round((self.rect.x - 15) / 30)
            self.location[1] = round((self.rect.y - 15) / 30)
        except IndexError:
            print("{}: no path found! Cord:{}".format(self.name, final))
