from term_printer import Color, Format, cprint
from core.Print import Message
from models.GameModel import GameModel
from models.blockModel import BlockModel
from models.db import DbModel
import uuid


class Game:
    def __init__(self, config):
        self.config = config
        self.level: int = 0
        self.history = []
        self.db = DbModel()
        self.name = ""

    def init(self):
        Message.title(" Jeu de pair ")
        is_n_ok = True
        while is_n_ok:
            print("\n")
            Message.question("Que souhaitez vous faire ?")
            Message.msg("1. Reprendre une partie sauvegardé")
            Message.msg("2. Nouvelle partie")
            value = input("> ")
            try:
                number = int(value)
                if 3 > number > 0:
                    is_n_ok = False
                    if number == 1:
                        game = self.db.get_all_game()
                        if len(game) > 0:
                            print(self.db.get_all_game())
                        else:
                            Message.info("Aucun jeu disponible")
                            is_n_ok = True
                    elif number == 2:
                        self.name = input('Nom de la partie  > ').strip()
                        self.init_game()
                    else:
                        Message.warning(f"Numéros {number} n'est pas 1 ou 2")
            except:
                Message.warning("Doit être un nombre !")

    def init_game(self):
        choice_level: bool = False
        q_level: int = len(self.config['level'])
        while not choice_level:
            cprint('Niveaux disponibles :', attrs=[Format.UNDERLINE, Format.BOLD, Color.MAGENTA])
            for index, grid in enumerate(self.config['level']):
                Message.msg(f"Niveau {index + 1} : {grid} x {grid}")
            choice = input(f"> ")
            try:
                self.level = int(choice)
                if q_level >= self.level > 0:
                    choice_level = True
                    Message.ok(f"Partie : nom -> {self.name} et niveau {self.level}")
                else:
                    print('\n' * 20)
                    Message.warning(f"Le niveau doit être compris entre 1 et {q_level}")
            except:
                print('\n' * 20)
                Message.warning('le niveau doit être un nombre !')
