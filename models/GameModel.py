from models.db import DbModel


class GameModel(DbModel):
    def __init__(self, game_id: str, name: str, grid_size: int):
        super().__init__()
        self.id: str = game_id
        self.name: str = name
        self.grid_size: int = grid_size

    def __str__(self):
        return f"GameModel('id': '{self.id}','name': '{self.name}','grid_size': '{self.grid_size}')"

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'grid_size': self.grid_size
        }