#Here are some tests for the Building class (and subclasses)

from game_map import Position, game_map
from buildings.bldng_class import Building
from buildings.other_bldngs import TownCenter, House


# t = TownCenter(1, (80, 80))
Building.build(TownCenter, 1, Position(80,80), game_map)


for tpl in ((4,4), (2,4), (99,0), (100, 0), (90,96), (90, 97), (10, 0), (10, -1)):
    position = Position(*tpl)
    yes_or_no = Building.can_build_on_map(TownCenter, position, game_map)
    print(position, yes_or_no)
    print()

for tpl in ((82, 80), (81,80), (76,80), (77, 80), (80,84), (80,83)):
    position = Position(*tpl)
    yes_or_no = Building.can_build_on_map(House, position, game_map)
    print(position, yes_or_no)
    print()


print(game_map)