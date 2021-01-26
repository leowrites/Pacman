from Players.ghost import Ghost


class Blinky(Ghost):
    def __init__(self, location, image, aggression, game_window, mode):
        super().__init__(location, image, aggression, game_window, mode)
        self.name = 'blinky'
