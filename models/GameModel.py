from models.db import DbModel


class GameModel(DbModel):
    def __init__(self, game_id: str):
        super().__init__()
        self.id: str = game_id

    def __str__(self):
        return f"GameModel('id': '{self.id}')"

    def get_json(self):
        return {
            'id': self.id
        }