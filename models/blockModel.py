from db import DB


class BlockModel(DB):
    def __init__(self, content: str, state: bool, game_id: int):
        super().__init__()
        self.content: str = content
        self.state: bool = state
        self.game_id: int = game_id

    def __repr__(self):
        return f"Block(content='{self.content}', state='{self.state}'"

    def __str__(self):
        return f"Block(content='{self.content}', state='{self.state}'"

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
