from tinydb import TinyDB, Query
import os


class DbModel(object):
    def __init__(self):
        self.db_path = os.path.join("./db.json")
        self.instance = TinyDB(self.db_path)

    def get_game(self, id_game: str):
        return self.instance.table('game').search(Query().id == id_game)

    def get_block(self, id_game: str):
        return self.instance.table('block').search(Query().game_id == id_game)

    def get_all_game(self):
        return self.instance.table('game').all()
