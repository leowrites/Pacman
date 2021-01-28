import pygame
from Map.map import Map
from Players.pacman import Pacman
from Players.inky import Inky
from Players.pinky import Pinky
from Players.blinky import Blinky
from Players.clyde import Clyde
import utility

"""
write a pacman game so it is both playable by a human and can train A.I.
author: Leo
started: Jan 15
"""

WHITE = pygame.Color(255, 255, 255)
WALL_COLOR = pygame.Color(0, 0, 128)
YELLOW = pygame.Color(255, 255, 0)

change_image = True
change_path = True


class Game:
    # initiate screen
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Pacman By Leo")
    pygame.display.set_mode((600, 650))

    # surface
    surface = pygame.display.get_surface()

    # load stuff
    SCARED_IMAGE = utility.load_scared_ghosts()
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
    inky = Inky([9, 11], GHOST_IMAGES['inky'], 0, surface, 'chase')
    pinky = Pinky([10, 11], GHOST_IMAGES['pinky'], 0, surface, 'chase')
    blinky = Blinky([9, 12], GHOST_IMAGES['blinky'], 0, surface, 'chase')
    clyde = Clyde([10, 12], GHOST_IMAGES['clyde'], 0, surface, 'chase')
    ghost_rects = [inky.rect, pinky.rect, clyde.rect, blinky.rect]
    cherry_rects = game_map.spawn_cherry_rects(CHERRY_IMAGE)
    ghosts = [inky, pinky, blinky, clyde]
    ghost_dead = []

    # game variables
    grid = utility.generate_grid(game_map.game_map)
    level = 0
    winning = False

    # game constants
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
        global change_image
        global change_path

        if self.pacman.alive:

            # pacman movement
            self.pacman.movement_restrictions()
            if self.pacman.moving:
                self.pacman.move()
            self.coins, self.total_coins = self.pacman.eat_coin(self.coins, self.total_coins)
            self.cherry_rects = self.pacman.eat_cherry(self.cherry_rects)
            self.ghosts, ghost_dead = self.pacman.is_alive(self.ghosts)
            if ghost_dead is not None:
                self.ghost_dead.append(ghost_dead)
            if self.pacman.mode == 'eat ghost':
                self.mode_eat_ghost()

            # ghost movement
            for ghost in self.ghosts:
                if ghost.mode == 'chase':
                    self.mode_ghost_chase()
                    break
                if ghost.mode == 'hide':
                    self.mode_ghost_hide()
                    break

            if self.total_coins == 14:
                self.winning = True
                self.level += 1
                self.reset(self.level)

            self.respawn_ghost()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            key_input = pygame.key.get_pressed()

            if self.pacman.alive:
                if event.type == self.ANIMATION_PERIOD:
                    self.pacman_image_selector()

                self.pacman_movements(key_input)

            if key_input[pygame.K_SPACE]:
                if not self.pacman.alive:
                    self.reset(0)

    def draw(self):

        if self.pacman.alive:
            bottom_plane = pygame.Surface((600, 50))
            self.surface.blit(bottom_plane,
                              pygame.draw.rect(bottom_plane, WALL_COLOR, bottom_plane.get_rect(center=(300, 625))))
            self.game_map.draw_map()
            self.game_map.draw_coins(self.coins, self.COIN_IMAGE)
            self.game_map.draw_cherry(self.cherry_rects, self.CHERRY_IMAGE)

            self.pacman.draw()
            for ghost in self.ghosts:
                ghost.draw()
            self.draw_dead_ghost()

            self.display_score()

            pygame.display.update()

        else:
            self.surface.fill((0, 0, 0))
            self.display_game_over()
            pygame.display.update()

    def mode_eat_ghost(self):
        global change_image
        global change_path
        if change_image:
            self.change_ghost_image('scared')
            for ghost in self.ghosts:
                ghost.mode = 'hide'
            change_image = False
        self.pacman.mode = utility.count_down()
        if self.pacman.mode == 'normal':
            self.change_ghost_image('normal')
            for ghost in self.ghosts:
                ghost.mode = 'chase'
            change_image = True
            change_path = True

    def mode_ghost_chase(self):
        pacman_cord = self.return_pacman_x_y()
        self.inky.move(self.grid, pacman_cord)
        clyde_aim = utility.generate_random_loc(self.game_map.game_map)
        self.clyde.move(self.grid, clyde_aim)
        blinky_aim = utility.generate_random_loc(self.game_map.game_map)
        self.blinky.move(self.grid, blinky_aim)
        if not self.pinky.aim:
            self.pinky.look_ahead(self.game_map.game_map, pacman_cord)
        self.pinky.move(self.grid, self.pinky.aim)
        self.pinky.clear_aim()

    def mode_ghost_hide(self):
        pacman_cord = self.return_pacman_x_y()
        global change_path
        corner = [[1, 1], [18, 1], [1, 18], [18, 18]]
        if change_path:
            for x, ghost in enumerate(self.ghosts):
                self.ghosts[x].find_path(self.grid, corner[x])
                change_path = False
        for ghost in self.ghosts:
            ghost.move(self.grid, pacman_cord)

    def change_ghost_image(self, state):
        if state == 'scared':
            self.inky.surface = self.blinky.surface = self.pinky.surface = self.clyde.surface = self.SCARED_IMAGE
        if state == 'normal':
            self.inky.surface = self.GHOST_IMAGES['inky']
            self.blinky.surface = self.GHOST_IMAGES['blinky']
            self.pinky.surface = self.GHOST_IMAGES['pinky']
            self.clyde.surface = self.GHOST_IMAGES['clyde']

    def respawn_ghost(self):
        for dead_ghost in self.ghost_dead:
            respawn_complete = dead_ghost.respawn_timer()
            if respawn_complete:
                pacman_cord = self.return_pacman_x_y()
                dead_ghost.find_path(self.grid, pacman_cord)
                self.ghosts.append(dead_ghost)
                self.ghost_dead.remove(dead_ghost)

    def return_pacman_x_y(self):
        x = round((self.pacman.rect.x - 15) / 30)
        if x == 0:
            x = 1
        y = round((self.pacman.rect.y - 15) / 30)
        if y == 0:
            y = 1
        return x, y

    def draw_dead_ghost(self):
        if self.ghost_dead:
            for ghost in self.ghost_dead:
                ghost.draw()

    def pacman_image_selector(self):
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

    def pacman_movements(self, key_input):

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

    def reset(self, level):
        self.pacman = Pacman(self.game_map.game_map, self.surface, self.PACMAN_IMAGES)
        self.inky = Inky([9, 11], self.GHOST_IMAGES['inky'], level, self.surface, 'chase')
        self.pinky = Pinky([10, 11], self.GHOST_IMAGES['pinky'], level, self.surface, 'chase')
        self.blinky = Blinky([9, 12], self.GHOST_IMAGES['blinky'], level, self.surface, 'chase')
        self.clyde = Clyde([10, 12], self.GHOST_IMAGES['clyde'], level, self.surface, 'chase')
        self.coins, self.total_coins = self.game_map.spawn_coins(self.COIN_IMAGE)
        self.ghosts = [self.inky, self.pinky, self.blinky, self.clyde]
        self.ghost_rects = [self.inky.rect, self.pinky.rect, self.blinky.rect, self.clyde.rect]
        self.cherry_rects = self.game_map.spawn_cherry_rects(self.CHERRY_IMAGE)

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
