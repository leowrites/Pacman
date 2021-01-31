import pickle

import neat
import pygame

import utility
from Map.map import Map
from Players.blinky import Blinky
from Players.clyde import Clyde
from Players.inky import Inky
from Players.pacman import Pacman
from Players.pinky import Pinky

"""
Training an A.N.N using neuroevolution of augmenting topologies for the Pacman game
author: Leo
started: Jan 15
"""

# game.py is the highest level file and has access to all other files
# initiate screen
pygame.init()
pygame.font.init()
pygame.display.set_caption("Pacman By Leo")
pygame.display.set_mode((600, 600))

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

# game variables
change_image = True
change_path = True
DRAW_RADAR = False
gen = 0

# game constants
ANIMATION_PERIOD = pygame.USEREVENT
pygame.time.set_timer(ANIMATION_PERIOD, 100)
CHECK_PATH_INTERVAL = pygame.USEREVENT + 1
pygame.time.set_timer(CHECK_PATH_INTERVAL, 1000)
WHITE = pygame.Color(255, 255, 255)
WALL_COLOR = pygame.Color(0, 0, 128)
YELLOW = pygame.Color(255, 255, 0)


def event_handler(pacmans, DRAW_RADAR):
    """
    do specific things at each event intervals
    :param pacmans: a list of pacmans to be affected
    :return: nothing
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == ANIMATION_PERIOD:
            for pacman in pacmans:
                pacman.pacman_image_selector()

        # toggle radar
    key_input = pygame.key.get_pressed()
    if key_input[pygame.K_SPACE]:
        if not DRAW_RADAR:
            DRAW_RADAR = True
        else:
            DRAW_RADAR = False
    return DRAW_RADAR


def eval_genome(genomes, config):
    """
    a generation
    :param genomes:
    :param config:
    :return: nothing
    """
    global change_image
    global change_path
    global gen
    global DRAW_RADAR

    # new objects for each iteration
    running = True
    gen += 1
    nets = []
    ge = []
    pacmans = []
    ghost_rect = []
    ghost_dead = []

    # map
    game_map = Map(surface)
    grid = utility.generate_grid(game_map.map_array)

    # cherry
    cherry_rects = game_map.spawn_cherry_rects(CHERRY_IMAGE)

    # ghosts
    inky = Inky([9, 11], GHOST_IMAGES['inky'], 0, surface, 'chase')
    pinky = Pinky([10, 11], GHOST_IMAGES['pinky'], 0, surface, 'chase')
    blinky = Blinky([9, 12], GHOST_IMAGES['blinky'], 0, surface, 'chase')
    clyde = Clyde([10, 12], GHOST_IMAGES['clyde'], 0, surface, 'chase')
    ghosts = [inky, pinky, blinky, clyde]

    for ghost in ghosts:
        ghost_rect.append(ghost.rect)

    # creating brains
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        pacmans.append(Pacman(game_map.map_array,
                              surface, PACMAN_IMAGES))
        genome.fitness = 0
        ge.append(genome)

    for x, pacman in enumerate(pacmans):
        pacmans[x].spawn_coins(COIN_IMAGE)

    while running and len(pacmans) > 0:

        utility.draw( game_map, cherry_rects, ghosts, ghost_dead, CHERRY_IMAGE)

        # process individuals
        # consider moving it to individual pacmans
        for x, pacman in enumerate(pacmans):

            direction = ['right', 'left', 'up', 'down']
            pacman.radars.clear()
            for d in direction:
                pacman.radar(d, surface)

            pacman.distance_to_ghost(ghosts, grid)
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

            cherry_rects = pacman.eat_cherry(cherry_rects)
            ghosts, ghost_dead = pacman.is_alive(ghosts)

            pacman.eat_coin()
            ge[x].fitness = pacman.get_fitness()

            if ghost_dead is not None:
                ghost_dead.append(ghost_dead)
            pacman.draw(COIN_IMAGE)

        for x, pacman in enumerate(pacmans):
            pacman.movement_restrictions()
            if not pacman.alive:
                pacmans.pop(x)
                ge.pop(x)
                nets.pop(x)

        if DRAW_RADAR:
            for pacman in pacmans:
                pacman.draw_radar()
                break

        for pacman in pacmans:
            if pacman.mode == 'eat ghost':
                inky.surface, blinky.surface, clyde.surface, pinky.surface = utility.mode_eat_ghost(pacmans, ghosts,
                                                                                                    SCARED_IMAGE,
                                                                                                    GHOST_IMAGES)
                break

        for ghost in ghosts:
            if ghost.mode == 'chase':
                utility.mode_ghost_chase(inky, blinky, clyde, pinky, pacmans, grid, game_map.map_array)
                break
            if ghost.mode == 'hide':
                utility.mode_ghost_hide(ghosts, pacmans, grid)
                break

        if len(pacmans) == 0:
            break

        utility.respawn_ghost(grid, ghost_dead, ghosts, pacmans)
        DRAW_RADAR = event_handler(pacmans, DRAW_RADAR)
        pygame.display.update()


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_file)
    population = neat.Checkpointer.restore_checkpoint('neat-checkpoint-{}'.format(input("Which generation do y"
                                                                                        "ou want to simulate? ")))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.Checkpointer(5))

    winner = population.run(eval_genome, 500)
    win = population.best_genome
    pickle.dump(winner, open('winner_pop.pkl', 'wb'))
    pickle.dump(win, open('winner.pkl', 'wb'))
