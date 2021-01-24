import pygame
from Map.map import Map
from Players.pacman import Pacman
from Players.ghost import Ghost
import utility

"""
write a pacman game so it is both playable by a human and can train A.I.
author: Leo
started: Jan 15
"""

WHITE = pygame.Color(255, 255, 255)
WALL_COLOR = pygame.Color(0, 0, 128)
YELLOW = pygame.Color(255, 255, 0)


class Game:
    # initiate screen
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Pacman By Leo")
    pygame.display.set_mode((600, 650))

    # surface
    surface = pygame.display.get_surface()

    # load stuff
    PACMAN_IMAGES = utility.load_images_pacman()
    INKY_IMAGE = utility.load_images_ghost()
    COIN_IMAGE = utility.load_images_coin()
    GAME_FONT = utility.load_font()

    # new objects
    game_map = Map(surface)
    pacman = Pacman(game_map.game_map, surface, PACMAN_IMAGES)
    inky = Ghost(11, 9, INKY_IMAGE, 0, surface)
    pacman.spawn()
    coins, total_coins = game_map.spawn_coins(COIN_IMAGE)

    # game variables
    grid = utility.generate_grid(game_map.game_map)

    # game constants
    ANIMATION_PERIOD = pygame.USEREVENT
    pygame.time.set_timer(ANIMATION_PERIOD, 100)
    CHECK_PATH_INTERVAL = pygame.USEREVENT + 1
    pygame.time.set_timer(CHECK_PATH_INTERVAL, 5000)

    # find path evrey 5 seconds

    def __init__(self):
        self.running = True

        while self.running:
            self.event_handler()
            self.update()
            self.draw()

    def update(self):
        # movement
        xy_ahead_a, xy_ahead_b = self.pacman.get_pixel_ahead()
        color_ahead_a = self.surface.get_at(xy_ahead_a)
        color_ahead_b = self.surface.get_at(xy_ahead_b)
        # if both color are channel, then moving is true, else its false
        if color_ahead_a == WALL_COLOR or color_ahead_b == WALL_COLOR:
            self.pacman.moving = False
        if self.pacman.moving:
            self.pacman.move()

        pacman_cord = self.return_pacman_x_y()
        self.inky.move(self.grid, pacman_cord)
        self.coins = self.pacman.eat_coin(self.coins)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == self.ANIMATION_PERIOD:
                if self.pacman.direction == "right":
                    if self.pacman.current_image == 1:
                        self.pacman.current_image = 2
                    else:
                        self.pacman.current_image = 1
                if self.pacman.direction == "left":
                    if self.pacman.current_image == 3:
                        self.pacman.current_image = 4
                    else:
                        self.pacman.current_image = 3
                if self.pacman.direction == "down":
                    if self.pacman.current_image == 5:
                        self.pacman.current_image = 6
                    else:
                        self.pacman.current_image = 5
                if self.pacman.direction == "up":
                    if self.pacman.current_image == 7:
                        self.pacman.current_image = 8
                    else:
                        self.pacman.current_image = 7

            if event.type == self.CHECK_PATH_INTERVAL:
                pacman_cord = self.return_pacman_x_y()
                self.inky.find_path(self.grid, pacman_cord)
            key_input = pygame.key.get_pressed()
            if key_input[pygame.K_LEFT]:
                self.pacman.moving = True
                self.pacman.RIGHT = False
                self.pacman.LEFT = True
                self.pacman.UP = False
                self.pacman.DOWN = False
                self.pacman.direction = "left"
            elif key_input[pygame.K_RIGHT]:
                self.pacman.moving = True
                self.pacman.RIGHT = True
                self.pacman.LEFT = False
                self.pacman.UP = False
                self.pacman.DOWN = False
                self.pacman.direction = "right"
            elif key_input[pygame.K_UP]:
                self.pacman.moving = True
                self.pacman.RIGHT = False
                self.pacman.LEFT = False
                self.pacman.UP = True
                self.pacman.DOWN = False
                self.pacman.direction = "up"
            elif key_input[pygame.K_DOWN]:
                self.pacman.moving = True
                self.pacman.RIGHT = False
                self.pacman.LEFT = False
                self.pacman.UP = False
                self.pacman.DOWN = True
                self.pacman.direction = "down"

    def draw(self):
        bottom_plane = pygame.Surface((600, 50))
        self.surface.blit(bottom_plane,
                          pygame.draw.rect(bottom_plane, WALL_COLOR, bottom_plane.get_rect(center=(300, 625))))
        self.game_map.draw_map()
        self.game_map.draw_coins(self.coins, self.COIN_IMAGE)
        self.pacman.draw()
        self.inky.draw()
        self.display_score()
        pygame.display.update()

    def display_score(self):
        score_surface = self.GAME_FONT.render("Score:{}".format(self.pacman.score), False, WHITE)
        rect = score_surface.get_rect(center=(200, 625))
        self.surface.blit(score_surface, rect)

        author_surface = self.GAME_FONT.render("Pacman By Leo!", False, YELLOW)
        rect1 = author_surface.get_rect(center=(400, 625))
        self.surface.blit(author_surface, rect1)

    def return_pacman_x_y(self):
        x = round((self.pacman.rect.x - 15) / 30)
        if x == 0:
            x = 1
        y = round((self.pacman.rect.y - 15) / 30)
        if y == 0:
            y = 1
        return x, y
