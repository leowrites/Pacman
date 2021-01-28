from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.grid import Grid
from Players.ghost import Ghost

UNIT_SIZE = 30


class Inky(Ghost):
    """
    inky follows the player exactly where they are
    """
    def __init__(self, location, image, aggression, game_window, mode):
        super().__init__(location, image, aggression, game_window, mode)
        self.name = 'Inky'
        self.init_location = [11, 9]