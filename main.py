import yaml
from game import Game

with open("config.yaml", "r", encoding='utf-8') as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)

game = Game(CONFIG)

game.init_game()


