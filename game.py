from term_printer import Color, Format, cprint
from models.GameModel import GameModel
from models.blockModel import BlockModel
import uuid


class Game:
    def __init__(self, config):
        self.config = config
        self.level: int = 0
        self.history = []

    @staticmethod
    def msg_warning(text: str):
        cprint(f'🚨 - {text}', attrs=[Color.BRIGHT_RED])

    @staticmethod
    def msg_ok(text: str):
        cprint(f'✅️ - {text} ', attrs=[Color.BRIGHT_GREEN])

    @staticmethod
    def msg_info(text: str):
        cprint(f'ℹ️ - {text} ', attrs=[Color.BRIGHT_BLUE])

    def init_game(self):
        choice_level: bool = False
        q_level: int = len(self.config['level'])
        cprint(" Jeu de pair ", attrs=[Format.BOLD, Color.BG_MAGENTA])
        while not choice_level:
            cprint('Niveaux disponibles :', attrs=[Format.UNDERLINE, Format.BOLD, Color.MAGENTA])
            for index, grid in enumerate(self.config['level']):
                cprint(f"Niveau {index + 1} : {grid} x {grid}", attrs=[Color.BRIGHT_GREEN])
            choice = input(f"Choix du niveau > ")
            try:
                self.level = int(choice)
                if q_level >= self.level > 0:
                    choice_level = True
                    # test msg
                    self.msg_ok("C'est partie !")
                    self.msg_info("Pour information")
                else:
                    print('\n' * 20)
                    self.msg_warning(f"Le niveau doit être compris entre 1 et {q_level}")
            except:
                print('\n' * 20)
                self.msg_warning('le niveau doit être un nombre !')

    def create_snap(self):
        game_id = str(uuid.uuid4())
        game = GameModel(game_id)
        # générer le nombre de bloc nécessaire
        # prendre en compte position X et Y ?
        self.history.append(game_id)

    def print_grid(self):

        print("Generate grid")
