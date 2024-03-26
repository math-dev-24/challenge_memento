from term_printer import Color, Format, cprint
from core.Print import Message
from models.GameModel import GameModel
from models.blockModel import BlockModel
from models.db import DbModel
import uuid
import random


class Game:
    def __init__(self, config):
        self.name = ""
        self.config = config
        self.db = DbModel()
        self.game_id: str = str(uuid.uuid4())
        self.blocks = []
        self.gameModel = ""
        self.grid_size: int = 0

    def init(self):
        Message.title(" Jeu de pair ")
        is_n_ok = True
        while is_n_ok:
            print("\n")
            Message.question("Que souhaitez vous faire ?")
            Message.msg("1 - Reprendre une partie sauvegardé")
            Message.msg("2 - Nouvelle partie")
            value = Message.input()

            if value.isdigit():
                number = int(value)
                if 3 > number > 0:
                    is_n_ok = False
                    if number == 1:
                        game = self.db.get_all_game()
                        if len(game) > 0:
                            print(self.db.get_all_game())
                        else:
                            Message.info("Aucune(s) sauvegarde(s) disponible(s)")
                            is_n_ok = True
                    elif number == 2:
                        Message.question("Nom de la partie ?")
                        self.name = Message.input().strip()
                        self.init_game()
                else:
                    Message.warning(f"Choix {number}, n'est pas 1 ou 2")
            else:
                Message.warning("Doit être un nombre !")

    def init_game(self):
        choice_level: bool = False
        q_level: int = len(self.config['level'])
        while not choice_level:
            print("\n")
            cprint('Niveaux disponibles :', attrs=[Format.UNDERLINE, Format.BOLD, Color.MAGENTA])
            for index, grid in enumerate(self.config['level']):
                Message.msg(f"Niveau {index + 1} : {grid} x {grid}")
            choice = Message.input()

            if choice.isdigit():
                level = int(choice)
                if q_level >= level > 0:
                    choice_level = True
                    self.grid_size = self.config['level'][level - 1]
                    Message.ok(f"Partie : nom -> {self.name} et niveau {level} : {self.grid_size} x {self.grid_size}")
                    self.init_grid()

                else:
                    print('\n' * 20)
                    Message.warning(f"Le niveau doit être compris entre 1 et {q_level}")
            else:
                print('\n' * 20)
                Message.warning('le niveau doit être un nombre !')

    def init_grid(self):
        q_emoji = int((self.grid_size * self.grid_size) / 2)
        random.shuffle(self.config['recto'])
        emoji = self.config['recto'][:q_emoji]

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                block = BlockModel('X', False, self.game_id, x + 1, y + 1)
                self.blocks.append(block)
        print(q_emoji)
        print(emoji)

    def print_grid(self):
        print(f"{self.grid_size} x {self.grid_size}")

    def get_game_model(self):
        return GameModel(self.game_id, self.name, self.grid_size)
