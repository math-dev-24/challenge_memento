from tinydb import TinyDB, Query
import os


class DbModel:
    def __init__(self):
        self.db_path = os.path.join("./db.json")
        self.instance = TinyDB(self.db_path)

    def get_game(self, id_game: str):
        return self.instance.table('game').search(Query().id == id_game)

    def get_block(self, id_game: str):
        return self.instance.table('block').search(Query().game_id == id_game)

    def get_all_game(self):
        return self.instance.table('game').all()

    def register_game(self, game):
        self.instance.table('game').insert(game.get_json())

    def register_block(self, block):
        self.instance.table('block').insert(block.get_json())

    def update_block(self, block):
        self.instance.table('block').update(
            {'is_visible': block.is_visible},
            (Query().x == block.x) & (Query().y == block.y) & (Query().game_id == block.game_id)
        )

    def delete_game(self, game_id: str):
        self.instance.table('block').remove(Query().game_id == game_id)
        self.instance.table('game').remove(Query().id == game_id)