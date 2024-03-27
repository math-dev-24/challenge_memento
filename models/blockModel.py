from models.db import DbModel


class BlockModel(DbModel):
    def __init__(self, content: str, is_visible: bool, game_id: str, x: int, y: int):
        super().__init__()
        self.game_id: str = game_id
        self.x: int = x
        self.y: int = y
        self.content: str = content
        self.is_visible: bool = is_visible

    def __str__(self):
        return f"Block(content='{self.content}', is_visible='{self.is_visible}', x='{self.x}', y='{self.y}')"

    def get_game_with_block(self):
        super().get_game(self.game_id)

    def get_content(self):
        return self.content

    def get_state(self):
        return self.is_visible

    def get_json(self):
        return {
            'game_id': self.game_id,
            'content': self.content,
            'is_visible': self.is_visible,
            'x': self.x,
            'y': self.y
        }

    def register(self):
        super().register_block(self)

    def update(self):
        super().update_block(self)
