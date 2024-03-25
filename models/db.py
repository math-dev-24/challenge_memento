from tinydb import TinyDB, Query


class DB:
    def __init__(self):
        self.instance = TinyDB('../db.json')
        self.block_table = self.instance.table('block')
        self.game_table = self.instance.table('game')

    def get_game(self, game_id: int):
        game = Query()
        return self.game_table.search(game.id == game_id)

    def get_block(self, game_id: int):
        game = Query()
        return self.block_table.search(game.id == game_id)
