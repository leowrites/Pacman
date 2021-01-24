import pygame
from pathfinding.core.grid import Grid

pygame.font.init()


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
    return INKY


def load_images_coin():
    COIN_IMAGE = pygame.transform.scale(pygame.image.load("assets/coin.png"), (15, 15))
    return COIN_IMAGE


def load_font():
    game_font = pygame.font.Font("assets/font.ttf", 20)
    return game_font


def generate_grid(game_map):
    map_list = list(game_map)
    grid = Grid(matrix=map_list)
    return grid
