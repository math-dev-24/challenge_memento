from models.db import DbModel


class BlockModel(DbModel):
    def __init__(self, content: str, state: bool, game_id: str):
        super().__init__()
        self.content: str = content
        self.state: bool = state
        self.game_id: str = game_id

    def __str__(self):
        return f"Block(content='{self.content}', state='{self.state}')"

    def get_game_with_block(self):
        super().get_game(self.game_id)

    def get_content(self):
        return self.content

    def get_state(self):
        return self.state

    def get_json(self):
        return {
            'content': self.content,
            'state': self.state,
            'game_id': self.game_id
        }
