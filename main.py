import yaml
from game import Game

# Récupération de la configuration
with open("config.yaml", "r", encoding='utf-8') as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

# Instance du jeu
game = Game(CONFIG)

# Initialisation du jeu
game.init()



