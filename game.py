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
        self.blocks = {}
        self.gameModel = None
        self.grid_size: int = 0
        self.y_list = []
        self.save = False

    def init(self):
        print('\n')
        Message.title(" Jeu de pair ")
        is_n_ok = True
        while is_n_ok:
            print("\n")
            Message.question("Que souhaitez vous faire ?")
            Message.msg("1 - Reprendre une partie sauvegardée")
            Message.msg("2 - Nouvelle partie")
            Message.msg("3 - Quitter")
            value = Message.input()

            if value.isdigit():
                number = int(value)
                if 4 > number > 0:
                    is_n_ok = False
                    if number == 1:
                        games = self.db.get_all_game()
                        if games:
                            game_save = len(games)
                            Message.info("Partie(s) sauvegardée(s) :")
                            for index, game in enumerate(games):
                                print(
                                    f"{index + 1} - Nom de la partie : {game['name']}, Grille : {game['grid_size']} x {game['grid_size']}.")
                            while True:
                                Message.question("Choix de la partie à reprendre :")
                                choice_game = Message.input()
                                if choice_game.isdigit() and 0 < int(choice_game) <= game_save:
                                    game_select = games[int(choice_game) - 1]
                                    self.game_id = game_select['id']
                                    self.name = game_select['name']
                                    self.grid_size = int(game_select['grid_size'])
                                    self.y_list = self.generate_alphabet(self.grid_size)
                                    self.save = True
                                    blocks = self.db.get_block(self.game_id)
                                    for block in blocks:
                                        block_key = f"{block['x']}-{block['y']}"
                                        self.blocks[block_key] = BlockModel(block['content'], block['is_visible'],
                                                                            block['game_id'], block['x'], block['y'])
                                    self.game()
                                else:
                                    Message.warning("Invalide !")
                        else:
                            Message.info("Aucune(s) sauvegarde(s) disponible(s)")
                            is_n_ok = True
                    elif number == 2:
                        Message.question("Nom de la partie ?")
                        self.name = Message.input().strip()
                        self.init_game()
                    else:
                        Message.info("Fermeture du jeu")
                        Message.info("Bonne journée !")
                        exit()
                else:
                    Message.warning(f"Votre choix : {number}, n'est pas 1 ou 2 ou 3")
            else:
                Message.warning("Doit être un nombre !")

    def init_game(self):
        q_level = len(self.config['level'])
        while True:
            print("\n")
            cprint('Niveaux disponibles :', attrs=[Format.UNDERLINE, Format.BOLD, Color.MAGENTA])
            for index, grid in enumerate(self.config['level']):
                Message.msg(f"Niveau {index + 1} : {grid} x {grid}")
            Message.question("Votre niveau ?")
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
        emojis = self.config['recto'][:q_emoji] * 2
        random.shuffle(emojis)
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                emoji = emojis.pop()
                block_key = f"{x + 1}-{self.y_list[y]}"
                self.blocks[block_key] = BlockModel(emoji, False, self.game_id, x + 1, self.y_list[y])
        self.game()

    def game(self):
        # print grid
        self.print_grid()
        item_1 = self.question_coordinate()
        item_2 = self.question_coordinate()
        block_1 = item_1['block']
        block_2 = item_2['block']
        value_1 = item_1['value']
        value_2 = item_2['value']
        if block_2.content != block_1.content:
            self.hide_bloc(value_1['y'], value_1['x'])
            self.hide_bloc(value_2['y'], value_2['x'])
        if self.check_win():
            Message.win("Bravo ! Tu as gagné !")
            self.reset_game()
        self.game()

    def print_grid(self):
        print(f"   {'  '.join(self.y_list)}")
        for x in range(1, self.grid_size + 1):
            line = []
            for y in self.y_list:
                block_key = f"{x}-{y}"
                block = self.blocks.get(block_key)
                content = block.content if block and block.is_visible else self.config['verso']
                line.append(content)
            print(f'{x}|{" ".join(line)}')

    def question_coordinate(self):
        while True:
            print('\n')
            Message.question("Entrée une position !")
            Message.info("Pour sauvegarder et reprendre plus tard : save")
            response = Message.input()
            if response.strip() == "save":
                self.go_save_game()

            value = self.check_coordinate(response)
            if not value['valid']:
                Message.warning("Coordonnée non valide")
            else:
                block = self.get_block(value['y'], value['x'])
                if not block.is_visible:
                    self.show_bloc(value['y'], value['x'])
                    self.print_grid()
                    return {
                        'block': block,
                        "value": value,
                    }
                Message.info("Block déjà visible")

    def check_coordinate(self, coordinate: str):
        coordinate = coordinate.strip()
        y = coordinate[0].upper()
        x = coordinate[1:].strip()

        y_in_list = any(y in letter for letter in self.y_list)
        x_is_valid = x.isdigit() and 0 < int(x) <= self.grid_size

        is_valid = y_in_list and x_is_valid

        return {
            "coordinate": coordinate,
            "valid": is_valid,
            "y": y,
            "x": x,
        }

    def get_block(self, y: str, x: str) -> BlockModel:
        return self.blocks.get(f"{x}-{y}")

    def show_bloc(self, y: str, x: str):
        block = self.blocks.get(f"{x}-{y}")
        if block:
            block.is_visible = True

    def hide_bloc(self, y: str, x: str):
        block = self.blocks.get(f"{x}-{y}")
        if block:
            block.is_visible = False

    @staticmethod
    def generate_alphabet(n: int):
        alphabet = string.ascii_uppercase
        return [alphabet[i % 26] for i in range(n)]

    def check_win(self):
        invisible_blocks_count = sum(1 for block in self.blocks.values() if not block.is_visible)
        return invisible_blocks_count == 0

    def reset_game(self):
        if self.save:
            self.db.delete_game(self.game_id)
        self.name = ""
        self.game_id = str(uuid.uuid4())
        self.blocks.clear()
        self.y_list = []
        self.save = False
        self.init()

    def get_game_model(self):
        return GameModel(self.game_id, self.name, self.grid_size)

    def go_save_game(self):
        if not self.save:
            self.get_game_model().register()
            for block in self.blocks.values():
                block.register()
        for block in self.blocks.values():
            block.update()
        Message.info("Partie sauvegardée !")
        exit()
