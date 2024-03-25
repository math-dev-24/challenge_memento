from term_printer import Color, Format, cprint
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

    @staticmethod
    def msg_warning(text: str):
        cprint(f'🚨 - {text}', attrs=[Color.BRIGHT_RED])

    @staticmethod
    def msg_ok(text: str):
        cprint(f'✅️ - {text} ', attrs=[Color.BRIGHT_GREEN])

    @staticmethod
    def msg_info(text: str):
        cprint(f'ℹ️ - {text} ', attrs=[Color.BRIGHT_BLUE])

    def init(self):
        cprint(" Jeu de pair ", attrs=[Format.BOLD, Color.BG_MAGENTA])
        is_n_ok = True
        while is_n_ok:
            print("\n")
            self.msg_info("Que souhaitez vous faire ?")
            cprint("1. Reprendre une partie sauvegardé", attrs=[Format.BOLD, Color.CYAN])
            cprint("2. Nouvelle partie", attrs=[Format.BOLD, Color.MAGENTA])
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
                            self.msg_info("Aucun jeu disponible")
                            is_n_ok = True
                    elif number == 2:
                        self.init_game()
                    else:
                        self.msg_info(f"Numéros {number} n'est pas 1 ou 2")
            except:
                self.msg_warning("Doit être un nombre !")

    def init_game(self):
        choice_level: bool = False
        q_level: int = len(self.config['level'])
        while not choice_level:
            cprint('Niveaux disponibles :', attrs=[Format.UNDERLINE, Format.BOLD, Color.MAGENTA])
            for index, grid in enumerate(self.config['level']):
                cprint(f"Niveau {index + 1} : {grid} x {grid}", attrs=[Color.BRIGHT_GREEN])
            choice = input(f"> ")
            try:
                self.level = int(choice)
                if q_level >= self.level > 0:
                    choice_level = True
                else:
                    print('\n' * 20)
                    self.msg_info(f"Le niveau doit être compris entre 1 et {q_level}")
            except:
                print('\n' * 20)
                self.msg_warning('le niveau doit être un nombre !')
