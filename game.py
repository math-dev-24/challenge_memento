from term_printer import Color, Format, cprint
from core.Print import Message
from models.GameModel import GameModel
from models.blockModel import BlockModel
from models.db import DbModel
import uuid
import string
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
        self.y_list = []

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
                    self.y_list = self.generate_alphabet(self.grid_size)
                    print('\n' * 20)
                    Message.info(f"Partie initialisé !")
                    Message.info(f"Nom : {self.name}")
                    Message.info(f"niveau {level} : {self.grid_size} x {self.grid_size}")
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
        emojis = self.config['recto'][:q_emoji]
        list_emojis = [{'available': 2, 'content': emoji} for emoji in emojis]

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                list_emojis = [emoji_item for emoji_item in list_emojis if emoji_item['available'] > 0]
                emoji_number = int(round(random.random() * (len(list_emojis) - 1), 0))
                current_emoji = list_emojis[emoji_number]['content']
                list_emojis[emoji_number]['available'] -= 1
                block = BlockModel(current_emoji, False, self.game_id, x + 1, self.y_list[y])
                self.blocks.append(block)
        self.print_grid()

    def print_grid(self):
        print(f"   {' | '.join(self.y_list)}")
        for x in range(self.grid_size):
            block_line = [block for block in self.blocks if block.x == (x+1)]
            line = []
            for block in block_line:
                content = block.content if block.is_visible else self.config['verso']
                line.append(content)
            print(f'{x + 1} {"| ".join(line)}')
        self.question_coor()

    def question_coor(self):
        is_n_ok = True
        while is_n_ok:
            print('\n')
            Message.question("Donnez deux positions !")
            Message.info("Exemple : A2,B5")
            coordinate = Message.input().split(",")
            is_n_ok = not len(coordinate) == 2
            if is_n_ok:
                Message.warning("Positions invalides !")
            else:
                Message.msg("vérification des coordonées")

    @staticmethod
    def generate_alphabet(n: int):
        alphabet = string.ascii_uppercase
        return [alphabet[i % 26] for i in range(n)]

    def get_game_model(self):
        return GameModel(self.game_id, self.name, self.grid_size)
