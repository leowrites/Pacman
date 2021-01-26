import pygame
from Map.map import Map
from Players.pacman import Pacman
from Players.inky import Inky
from Players.pinky import Pinky
from Players.blinky import Blinky
from Players.clyde import Clyde
import utility
import queue
from threading import Thread

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
    GHOST_IMAGES = utility.load_images_ghost()
    CHERRY_IMAGE = utility.load_images_cherry()
    COIN_IMAGE = utility.load_images_coin()
    GAME_FONT = utility.load_font()
    GAME_OVER_FONT = utility.load_game_over_font()

    # new objects
    game_map = Map(surface)
    coins, total_coins = game_map.spawn_coins(COIN_IMAGE)
    pacman = Pacman(game_map.game_map, surface, PACMAN_IMAGES)
    inky = Inky([11, 9], GHOST_IMAGES['inky'], 0, surface, 'chasing')
    pinky = Pinky([10, 9], GHOST_IMAGES['pinky'], 0, surface, 'chasing')
    blinky = Blinky([9, 9], GHOST_IMAGES['blinky'], 0, surface, 'chasing')
    clyde = Clyde([8, 9], GHOST_IMAGES['clyde'], 0, surface, 'chasing')
    ghost_rects = [inky.rect, pinky.rect, clyde.rect, blinky.rect]
    cherry_rects = game_map.spawn_cherry_rects(CHERRY_IMAGE)

    # game variables
    grid = utility.generate_grid(game_map.game_map)
    queue = queue.Queue()

    # game constants
    count_down = Thread(target=utility.count_down, arg=(queue))
    ANIMATION_PERIOD = pygame.USEREVENT
    pygame.time.set_timer(ANIMATION_PERIOD, 100)
    CHECK_PATH_INTERVAL = pygame.USEREVENT + 1
    pygame.time.set_timer(CHECK_PATH_INTERVAL, 1000)

    def __init__(self):
        self.running = True

        while self.running:
            self.event_handler()
            self.update()
            self.draw()

    def update(self):
        if self.pacman.alive:

            # pacman movement
            self.pacman.movement_restrictions()
            if self.pacman.moving:
                self.pacman.move()
            self.coins = self.pacman.eat_coin(self.coins)
            self.cherry_rects = self.pacman.eat_cherry(self.cherry_rects)
            self.pacman.is_alive(self.ghost_rects)

            # ghost movement
            pacman_cord = self.return_pacman_x_y()
            # clyde
            self.clyde.move(self.grid, pacman_cord)
            # blinky
            self.blinky.move(self.grid, pacman_cord)
            # inky
            self.inky.move(self.grid, pacman_cord)
            # pinky
            if not self.pinky.aim:
                self.pinky.look_ahead(self.game_map.game_map, pacman_cord)
            self.pinky.move(self.grid, self.pinky.aim)
            self.pinky.clear_aim()

            if self.pacman.mode == 'eat ghost':
                if not self.count_down.is_alive():
                    self.count_down.start()
                    value = self.queue.get()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            key_input = pygame.key.get_pressed()
            if self.pacman.alive:
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
                    self.pinky.look_ahead(self.game_map.game_map, pacman_cord)

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
            if key_input[pygame.K_SPACE]:
                if not self.pacman.alive:
                    self.reset()

    def draw(self):

        if self.pacman.alive:
            bottom_plane = pygame.Surface((600, 50))
            self.surface.blit(bottom_plane,
                              pygame.draw.rect(bottom_plane, WALL_COLOR, bottom_plane.get_rect(center=(300, 625))))
            self.game_map.draw_map()
            self.game_map.draw_coins(self.coins, self.COIN_IMAGE)
            self.game_map.draw_cherry(self.cherry_rects, self.CHERRY_IMAGE)

            self.pacman.draw()
            self.inky.draw()
            self.pinky.draw()
            self.blinky.draw()
            self.clyde.draw()
            self.display_score()
            pygame.display.update()

        else:
            self.surface.fill((0, 0, 0))
            self.display_game_over()
            pygame.display.update()

    def display_game_over(self):
        logo = self.GAME_OVER_FONT.render('PACMAN BY LEO', False, YELLOW)
        logo_rect = logo.get_rect(center=(300, 250))
        self.surface.blit(logo, logo_rect)
        surface = self.GAME_OVER_FONT.render("GAME OVER!", False, WHITE)
        rect = surface.get_rect(center=(300, 300))
        self.surface.blit(surface, rect)
        surface1 = self.GAME_FONT.render("PRESS SPACE TO PLAY AGAIN", False, WHITE)
        rect1 = surface1.get_rect(center=(300, 350))
        self.surface.blit(surface1, rect1)

    def display_score(self):
        score_surface = self.GAME_FONT.render("Score:{}".format(self.pacman.score), False, WHITE)
        rect = score_surface.get_rect(center=(100, 625))
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

    def reset(self):
        self.pacman = Pacman(self.game_map.game_map, self.surface, self.PACMAN_IMAGES)
        self.inky = Inky([11, 9], self.GHOST_IMAGES['inky'], 0, self.surface, 'chasing')
        self.pinky = Pinky([10, 9], self.GHOST_IMAGES['pinky'], 0, self.surface, 'chasing')
        self.coins, self.total_coins = self.game_map.spawn_coins(self.COIN_IMAGE)
        self.ghost_rects = [self.inky.rect, self.pinky.rect]
