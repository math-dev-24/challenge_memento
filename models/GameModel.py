from models.db import DbModel


class GameModel(DbModel):
    def __init__(self, game_id: str, name: str):
        super().__init__()
        self.id: str = game_id
        self.name: str = name

    def __str__(self):
        return f"GameModel('id': '{self.id}')"

    def get_json(self):
        return {
            'id': self.id
        }