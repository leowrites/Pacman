import pygame
from Map.map import Map
from Players.pacman import Pacman
from Players.inky import Inky
from Players.pinky import Pinky
from Players.blinky import Blinky
from Players.clyde import Clyde
import utility
import neat
import pickle

"""
write a pacman game so it is both playable by a human and can train A.I.
author: Leo
started: Jan 15
"""

WHITE = pygame.Color(255, 255, 255)
WALL_COLOR = pygame.Color(0, 0, 128)
YELLOW = pygame.Color(255, 255, 0)
gen = 0

change_image = True
change_path = True


def pacman_image_selector(pacmans):
    for pacman in pacmans:
        if pacman.direction == "right":
            if pacman.current_image == 1:
                pacman.current_image = 2
            else:
                pacman.current_image = 1
        if pacman.direction == "left":
            if pacman.current_image == 3:
                pacman.current_image = 4
            else:
                pacman.current_image = 3
        if pacman.direction == "down":
            if pacman.current_image == 5:
                pacman.current_image = 6
            else:
                pacman.current_image = 5
        if pacman.direction == "up":
            if pacman.current_image == 7:
                pacman.current_image = 8
            else:
                pacman.current_image = 7


def return_pacman_x_y(pacmans):
    for pacman in pacmans:
        x = round((pacman.rect.x - 15) / 30)
        if x == 0:
            x = 1
        y = round((pacman.rect.y - 15) / 30)
        if y == 0:
            y = 1
        return x, y


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

    # game variables

    # game constants
    ANIMATION_PERIOD = pygame.USEREVENT
    pygame.time.set_timer(ANIMATION_PERIOD, 100)
    CHECK_PATH_INTERVAL = pygame.USEREVENT + 1
    pygame.time.set_timer(CHECK_PATH_INTERVAL, 1000)

    def __init__(self):
        self.game_map = None
        self.running = True
        self.inky = None
        self.pinky = None
        self.blinky = None
        self.clyde = None
        self.game_map = None
        self.ghost_rects = self.cherry_rects = self.ghosts = self.ghost_dead = None
        self.grid = None

    def eval_genome(self, genomes, config):
        global change_image
        global change_path
        global gen

        gen += 1
        nets = []
        ge = []
        pacmans = []

        self.game_map = Map(self.surface)
        self.ghost_dead = []
        self.inky = Inky([9, 11], self.GHOST_IMAGES['inky'],
                         0, self.surface, 'chase')
        self.pinky = Pinky(
            [10, 11], self.GHOST_IMAGES['pinky'], 0, self.surface, 'chase')
        self.blinky = Blinky(
            [9, 12], self.GHOST_IMAGES['blinky'], 0, self.surface, 'chase')
        self.clyde = Clyde(
            [10, 12], self.GHOST_IMAGES['clyde'], 0, self.surface, 'chase')
        self.ghost_rects = [self.inky.rect, self.pinky.rect,
                            self.clyde.rect, self.blinky.rect]
        self.cherry_rects = self.game_map.spawn_cherry_rects(self.CHERRY_IMAGE)
        self.ghosts = [self.inky, self.pinky, self.blinky, self.clyde]
        self.grid = utility.generate_grid(self.game_map.game_map)

        for genome_id, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            pacmans.append(Pacman(self.game_map.game_map,
                                  self.surface, self.PACMAN_IMAGES))
            genome.fitness = 0
            ge.append(genome)

        for x, pacman in enumerate(pacmans):
            pacmans[x].spawn_coins(self.COIN_IMAGE)

        while self.running and len(pacmans) > 0:

            self.draw()

            for x, pacman in enumerate(pacmans):

                direction = ['right', 'left', 'up', 'down']
                pacman.radars.clear()
                for d in direction:
                    pacman.radar(d, self.surface)

                pacman.distance_to_ghost(self.ghosts, self.grid)
                output = nets[x].activate((pacman.get_data()))
                if pacman.moving:
                    if output[0] > 0:
                        ge[x].fitness = pacman.move('right')
                    elif output[1] > 0:
                        ge[x].fitness = pacman.move('left')
                    elif output[2] > 0:
                        ge[x].fitness = pacman.move('up')
                    elif output[3] > 0:
                        ge[x].fitness = pacman.move('down')
                    else:
                        pacman.alive = False

                self.cherry_rects = pacman.eat_cherry(self.cherry_rects)
                self.ghosts, ghost_dead = pacman.is_alive(self.ghosts)

                pacman.eat_coin()
                ge[x].fitness = pacman.get_fitness()

                if ghost_dead is not None:
                    ghost_dead.append(ghost_dead)
                pacman.draw(self.COIN_IMAGE)
            for x, pacman in enumerate(pacmans):
                pacman.movement_restrictions()
                if not pacman.alive:
                    pacmans.pop(x)
                    ge.pop(x)
                    nets.pop(x)

            if len(pacmans) == 0:
                break

            for pacman in pacmans:
                if pacman.mode == 'eat ghost':
                    self.mode_eat_ghost(pacmans)
                    break

            for ghost in self.ghosts:
                if ghost.mode == 'chase':
                    self.mode_ghost_chase(pacmans)
                    break
                if ghost.mode == 'hide':
                    self.mode_ghost_hide(pacmans)
                    break

            self.respawn_ghost(pacmans)
            self.event_handler(pacmans)
            self.display_generation()
            pygame.display.update()

    def event_handler(self, pacmans):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == self.ANIMATION_PERIOD:
                pacman_image_selector(pacmans)

    def draw(self):
        bottom_plane = pygame.Surface((600, 50))
        self.surface.blit(bottom_plane,
                          pygame.draw.rect(bottom_plane, WALL_COLOR, bottom_plane.get_rect(center=(300, 625))))
        self.game_map.draw_map()
        self.game_map.draw_cherry(self.cherry_rects, self.CHERRY_IMAGE)
        for ghost in self.ghosts:
            ghost.draw()
        self.draw_dead_ghost()

    def mode_eat_ghost(self, pacmans):
        global change_image
        global change_path
        for pacman in pacmans:
            if change_image:
                self.change_ghost_image('scared')
                for ghost in self.ghosts:
                    ghost.mode = 'hide'
                change_image = False
            if utility.count_down() == 'normal':
                pacman.mode = 'normal'
                self.change_ghost_image('normal')
                for ghost in self.ghosts:
                    ghost.mode = 'chase'
                change_image = True
                change_path = True

    def mode_ghost_chase(self, pacmans):
        pacman_cord = return_pacman_x_y(pacmans)
        self.inky.move(self.grid, pacman_cord)
        clyde_aim = utility.generate_random_loc(self.game_map.game_map)
        self.clyde.move(self.grid, clyde_aim)
        blinky_aim = utility.generate_random_loc(self.game_map.game_map)
        self.blinky.move(self.grid, blinky_aim)
        if not self.pinky.aim:
            self.pinky.look_ahead(self.game_map.game_map, pacman_cord)
        self.pinky.move(self.grid, self.pinky.aim)
        self.pinky.clear_aim()

    def mode_ghost_hide(self, pacmans):
        global change_path
        pacman_cord = return_pacman_x_y(pacmans)
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

    def display_generation(self):
        generation_surface = self.GAME_FONT.render(
            "Generation:{}".format(gen), False, (255, 255, 255))
        generation_surface_rect = generation_surface.get_rect(
            center=(100, 620))
        self.surface.blit(generation_surface, generation_surface_rect)

    def respawn_ghost(self, pacmans):
        for dead_ghost in self.ghost_dead:
            respawn_complete = dead_ghost.respawn_timer()
            if respawn_complete:
                pacman_cord = return_pacman_x_y(pacmans)
                dead_ghost.find_path(self.grid, pacman_cord)
                self.ghosts.append(dead_ghost)
                self.ghost_dead.remove(dead_ghost)

    def draw_dead_ghost(self):
        if self.ghost_dead:
            for ghost in self.ghost_dead:
                ghost.draw()


game1 = Game()


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_file)
    # population = neat.Population(config)
    population = neat.Checkpointer.restore_checkpoint('neat-checkpoint-{}'.format(input("Which generation do you want "
                                                                                        "to simulate? ")))
    stats = neat.StatisticsReporter()
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.Checkpointer(5))

    winner = population.run(game1.eval_genome, 500)
    win = population.best_genome
    pickle.dump(winner, open('winner_pop.pkl', 'wb'))
    pickle.dump(win, open('winner.pkl', 'wb'))
