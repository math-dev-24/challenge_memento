import yaml
import uuid
from game import Game
from models.db import DbModel
from models.GameModel import GameModel
from models.blockModel import BlockModel

with open("config.yaml", "r", encoding='utf-8') as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)

# game = Game(CONFIG)
# game.init_game()

db = DbModel()

game_id = str(uuid.uuid4())
new_game = GameModel(game_id)
bl1 = BlockModel('A', True, game_id)
bl2 = BlockModel('C', False, game_id)
bl3 = BlockModel('B', True, game_id)

# db.instance.table('game').insert(new_game.get_json())
# db.instance.table('block').insert(bl1.get_json())
# db.instance.table('block').insert(bl2.get_json())
# db.instance.table('block').insert(bl3.get_json())

print(db.get_all_game())
print(db.get_block('c46f8783-9017-48ba-b399-aaadccdf0d4b'))

