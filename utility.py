import pygame
from pathfinding.core.grid import Grid
from random import randint

pygame.font.init()
SECONDS = 10
COUNTDOWN = SECONDS * 60

change_image = True
change_path = True


def load_images_pacman():
    PACMAN_RIGHT_OPEN = pygame.transform.smoothscale(pygame.image.load("assets/pacman_right_open.png"), (20, 20))
    PACMAN_RIGHT_CLOSED = pygame.transform.smoothscale(pygame.image.load("assets/pacman_right_closed.png"), (20, 20))
    PACMAN_LEFT_OPEN = pygame.transform.smoothscale(pygame.image.load("assets/pacman_left_open.png"), (20, 20))
    PACMAN_LEFT_CLOSED = pygame.transform.smoothscale(pygame.image.load("assets/pacman_left_closed.png"), (20, 20))
    PACMAN_DOWN_CLOSED = pygame.transform.smoothscale(pygame.image.load("assets/pacman_down_close.png"), (20, 20))
    PACMAN_DOWN_OPEN = pygame.transform.smoothscale(pygame.image.load("assets/pacman_down_open.png"), (20, 20))
    PACMAN_UP_OPEN = pygame.transform.smoothscale(pygame.image.load("assets/pacman_up_open.png"), (20, 20))
    PACMAN_UP_CLOSED = pygame.transform.smoothscale(pygame.image.load("assets/pacman_up_closed.png"), (20, 20))
    PACMAN_IMAGES = {
        1: PACMAN_RIGHT_OPEN,
        2: PACMAN_RIGHT_CLOSED,
        3: PACMAN_LEFT_OPEN,
        4: PACMAN_LEFT_CLOSED,
        5: PACMAN_DOWN_OPEN,
        6: PACMAN_DOWN_CLOSED,
        7: PACMAN_UP_OPEN,
        8: PACMAN_UP_CLOSED
    }
    return PACMAN_IMAGES


def load_images_ghost():
    INKY = pygame.transform.smoothscale(pygame.image.load("assets/inky.png"), (20, 20))
    PINKY = pygame.transform.smoothscale(pygame.image.load("assets/pinky.png"), (20, 20))
    BLINKY = pygame.transform.smoothscale(pygame.image.load("assets/blinky.png"), (20, 20))
    CLYDE = pygame.transform.smoothscale(pygame.image.load("assets/clyde.png"), (20, 20))
    IMAGES = {
        'inky': INKY,
        'pinky': PINKY,
        'blinky': BLINKY,
        'clyde': CLYDE
    }
    return IMAGES


def load_scared_ghosts():
    SCARED = pygame.transform.smoothscale(pygame.image.load("assets/scared.png"), (20, 20))
    return SCARED


def load_images_coin():
    COIN_IMAGE = pygame.transform.scale(pygame.image.load("assets/coin.png"), (7, 7))
    return COIN_IMAGE


def load_images_cherry():
    CHERRY_IMAGE = pygame.transform.scale(pygame.image.load('assets/cherry.png'), (30, 30))
    return CHERRY_IMAGE


def load_font():
    game_font = pygame.font.Font("assets/font.ttf", 20)
    return game_font


def load_game_over_font():
    game_over_font = pygame.font.Font("assets/font.ttf", 50)
    return game_over_font


def generate_grid(game_map):
    map_list = list(game_map)
    grid = Grid(matrix=map_list)
    return grid


def count_down():
    """
    because the game updates 60 times a second, function
    should subtract 1 from COUNTDOWN 60 times a second to acheive countdown
    :return: state of the pacman
    """
    global COUNTDOWN
    COUNTDOWN -= 1
    if COUNTDOWN == 0:
        # resets the clock
        COUNTDOWN = SECONDS * 60
        return 'normal'
    return 'eat ghost'


def generate_random_loc(game_map):
    x = randint(1, 18)
    y = randint(1, 18)
    cord = [x, y]
    if game_map[y][x] != 1:
        return generate_random_loc(game_map)
    else:
        return cord


def draw(game_map, cherry_rects, ghosts, ghosts_dead, CHERRY_IMAGE):
    game_map.draw_map()
    game_map.draw_cherry(cherry_rects, CHERRY_IMAGE)
    for ghost in ghosts:
        ghost.draw()
    draw_dead_ghost(ghosts_dead)


def draw_dead_ghost(ghost_dead):
    if ghost_dead:
        for ghost in ghost_dead:
            ghost.draw()


def respawn_ghost(grid, ghost_dead, ghosts, pacmans):
    if ghost_dead:
        for dead_ghost in ghost_dead:
            respawn_complete = dead_ghost.respawn_timer()
            if respawn_complete:
                pacman_cord = return_pacman_x_y(pacmans)
                dead_ghost.find_path(grid, pacman_cord)
                ghosts.append(dead_ghost)
                ghost_dead.remove(dead_ghost)


def return_pacman_x_y(pacmans):
    for pacman in pacmans:
        x = round((pacman.rect.x - 15) / 30)
        if x == 0:
            x = 1
        y = round((pacman.rect.y - 15) / 30)
        if y == 0:
            y = 1
        return x, y


def mode_eat_ghost(pacmans, ghosts, SCARED_IMAGE, GHOST_IMAGES):
    global change_image
    global change_path

    for pacman in pacmans:
        if change_image:
            inky_surface, blinky_surface, clyde_surface, pinky_surface = change_ghost_image(ghosts, 'scared',
                                                                                            SCARED_IMAGE, GHOST_IMAGES)
            for ghost in ghosts:
                ghost.mode = 'hide'
            change_image = False
            return inky_surface, blinky_surface, clyde_surface, pinky_surface
        if count_down() == 'normal':
            pacman.mode = 'normal'
            inky_surface, blinky_surface, clyde_surface, pinky_surface = change_ghost_image(ghosts, 'normal',
                                                                                            SCARED_IMAGE, GHOST_IMAGES)
            for ghost in ghosts:
                ghost.mode = 'chase'
            change_image = True
            change_path = True
            return inky_surface, blinky_surface, clyde_surface, pinky_surface


def mode_ghost_chase(inky, clyde, blinky, pinky, pacmans, grid, game_map):
    pacman_cord = return_pacman_x_y(pacmans)
    inky.move(grid, pacman_cord)
    clyde_aim = generate_random_loc(game_map)
    clyde.move(grid, clyde_aim)
    blinky_aim = generate_random_loc(game_map)
    blinky.move(grid, blinky_aim)
    if not pinky.aim:
        pinky.look_ahead(game_map, pacman_cord)
    pinky.move(grid, pinky.aim)
    pinky.clear_aim()


def mode_ghost_hide(ghosts, pacmans, grid):
    global change_path
    pacman_cord = return_pacman_x_y(pacmans)
    corner = [[1, 1], [18, 1], [1, 18], [18, 18]]
    if change_path:
        for x, ghost in enumerate(ghosts):
            ghosts[x].find_path(grid, corner[x])
            change_path = False
    for ghost in ghosts:
        ghost.move(grid, pacman_cord)


def change_ghost_image(ghosts, state, SCARED_IMAGE, GHOST_IMAGES):
    if state == 'scared':
        for ghost in ghosts:
            ghost.surface = SCARED_IMAGE
    if state == 'normal':
        inky_surface = GHOST_IMAGES['inky']
        blinky_surface = GHOST_IMAGES['blinky']
        pinky_surface = GHOST_IMAGES['pinky']
        clyde_surface = GHOST_IMAGES['clyde']
        return inky_surface, blinky_surface, pinky_surface, clyde_surface
