#Here are some tests for the Building class (and subclasses)

from player import Player
from game_map import Position, game_map
from buildings.bldng_class import Building
from buildings.other_bldngs import TownCenter, House


position = Position(80, 80)
player = Player(1, position, True)
towncenter = TownCenter(1, position, player)
towncenter.build_on_map(Position(80, 80), game_map)


for tpl in ((4,4), (2,4), (99,0), (100, 0), (90,96), (90, 97), (10, 0), (10, -1)):
    position = Position(*tpl)
    yes_or_no = towncenter.can_build_on_map(position, game_map)
    print(position, yes_or_no)
    print()

for tpl in ((82, 80), (81,80), (76,80), (77, 80), (80,84), (80,83)):
    position = Position(*tpl)
    house = House(1, position, player)
    yes_or_no = house.can_build_on_map(position, game_map)
    print(position, yes_or_no)
    print()


print(game_map)