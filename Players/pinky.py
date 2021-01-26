from Players.ghost import Ghost
import random


class Pinky(Ghost):
    """
    Pinky is fast but looks at 3 tiles ahead of the pacman
    """

    def __init__(self, location, image, aggression, game_window, mode):
        super().__init__(location, image, aggression, game_window, mode)
        self.name = 'Pinky'

    def look_ahead(self, game_map, pacman_location):
        a = [pacman_location[0] + 3, pacman_location[1]]
        b = [pacman_location[0] - 3, pacman_location[1]]
        c = [pacman_location[0], pacman_location[1] + 3]
        d = [pacman_location[0], pacman_location[1] - 3]
        cord = [a, b, c, d]

        for possible in cord:
            if 0 < possible[0] < 19 and 0 < possible[1] < 19:
                if game_map[possible[1], possible[0]] == 1:
                    self.aim = possible
                    break
        if not self.aim:
            self.aim = pacman_location

    def clear_aim(self):
        if self.location == self.aim:
            self.aim = []
