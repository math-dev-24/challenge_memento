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
        self.gameModel = None
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
        q_level = len(self.config['level'])
        while True:
            print("\n")
            cprint('Niveaux disponibles :', attrs=[Format.UNDERLINE, Format.BOLD, Color.MAGENTA])
            for index, grid in enumerate(self.config['level']):
                Message.msg(f"Niveau {index + 1} : {grid} x {grid}")
            Message.question("Quelle niveau ?")
            choice = Message.input()
            if choice.isdigit():
                level = int(choice)
                if 1 <= level <= q_level:
                    self.grid_size = self.config['level'][level - 1]
                    self.y_list = self.generate_alphabet(self.grid_size)
                    print('\n' * 20)
                    Message.question("Partie initialisée !")
                    Message.info(f"Nom de la partie : {self.name}")
                    Message.info(f"Niveau {level} : {self.grid_size} x {self.grid_size}")
                    self.init_grid()
                    break
                else:
                    print('\n' * 20)
                    Message.warning(f"Le niveau doit être compris entre 1 et {q_level}")
            else:
                print('\n' * 20)
                Message.warning('Le niveau doit être un nombre entier positif !')

    def init_grid(self):
        q_emoji = int((self.grid_size * self.grid_size) / 2)
        random.shuffle(self.config['recto'])
        emojis = self.config['recto'][:q_emoji]
        list_emojis = [{'available': 2, 'content': emoji} for emoji in emojis]

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                available_emojis = [emoji_item for emoji_item in list_emojis if emoji_item['available'] > 0]
                emoji_item = random.choice(available_emojis)
                current_emoji = emoji_item['content']
                emoji_item['available'] -= 1
                block = BlockModel(current_emoji, False, self.game_id, x + 1, self.y_list[y])
                self.blocks.append(block)
        self.print_grid()

    def print_grid(self):
        print(f"   {' | '.join(self.y_list)}")
        for x in range(self.grid_size):
            block_line = [block for block in self.blocks if block.x == (x + 1)]
            line = []
            for block in block_line:
                content = block.content if block.is_visible else self.config['verso']
                line.append(content)
            print(f'{x + 1} {"| ".join(line)}')
        self.question_coordinate()

    def question_coordinate(self):
        while True:
            print('\n')
            Message.question("Donnez deux positions !")
            Message.info("Exemple : A2,B5")
            coordinate = Message.input().split(",")
            if len(coordinate) != 2:
                text = "trop" if len(coordinate) > 2 else "pas assez"
                Message.warning(f"Il y a {text} de coordonnées !")
            else:
                # Vérification coordonnées existantes ?
                check_1 = self.check_coordinate(coordinate[0])
                check_2 = self.check_coordinate(coordinate[1])
                if check_1['valid'] and check_2['valid']:
                    # Vérification Block n'est pas déjà découvert ?
                    block_1 = self.get_block(check_1['y'], check_1['x'])
                    block_2 = self.get_block(check_2['y'], check_2['x'])
                    if block_1 and block_2:
                        if not block_1.is_visible and not block_2.is_visible:
                            if block_1.content == block_2.content:
                                for block in self.blocks:
                                    if block.content == block_1.content:
                                        block.is_visible = True
                                if self.check_win():
                                    Message.win("Vous avez gagné !")
                                    print("\n" * 2)
                                    self.reset_game()
                                else:
                                    self.print_grid()
                                break
                            else:
                                Message.info("Non identique")
                                self.print_grid()
                                break
                        else:
                            Message.warning("Bloque déjà découvert !")

                    else:
                        Message.warning("Coordonnées invalides")
                else:
                    Message.warning("Coordonnées invalides")

    def check_coordinate(self, coordinate: str):
        coordinate = coordinate.strip()
        y = coordinate[0].upper()
        x = coordinate[1:].strip()

        y_in_list = any(y in letter for letter in self.y_list)
        x_is_valid = x.isdigit() and 0 < int(x) <= self.grid_size
        is_valid = y_in_list and x_is_valid

        return {
            "valid": is_valid,
            "y": y,
            "x": x
        }

    def get_block(self, y: str, x: str) -> BlockModel:
        block_item = None
        for block in self.blocks:
            if block.x == int(x) and block.y == y:
                block_item = block
        return block_item

    @staticmethod
    def generate_alphabet(n: int):
        alphabet = string.ascii_uppercase
        return [alphabet[i % 26] for i in range(n)]

    def check_win(self):
        win = False
        rest_block = [block for block in self.blocks if not block.is_visible]
        quantity_rest = len(rest_block)
        return  quantity_rest == 0

    def reset_game(self):
        self.name = ""
        self.game_id = str(uuid.uuid4())
        self.blocks = []
        self.y_list = []
        self.init()

    def get_game_model(self):
        return GameModel(self.game_id, self.name, self.grid_size)
