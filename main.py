from Game.game import run
import os

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.feedforward.txt')
    run(config_path)
