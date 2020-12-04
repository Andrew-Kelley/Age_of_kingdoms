from resources import Wood, Stone, Food, Gold, Bronze, Iron
from map_etc.game_map import GameMap
from map_etc.position import Position

# Eventually, I should create a function or class that makes a random map
game_map = GameMap([[' '] * 100 for i in range(100)])
for i in range(60, 66):
    for j in range(75, 85):
        game_map[i][j] = Wood(Position(j, i))

# Eh, I feel like adding more wood:
for i in range(66, 72):
    for j in range(80, 90):
        game_map[i][j] = Wood(Position(j, i))

# Filling the bottom left corner with wood:
for i in range(30):
    for j in range(30 - i):
        game_map[i][j] = Wood(Position(j, i))

# Filling the top left corner with wood:
for i in range(80, 100):
    for j in range(i - 80):
        game_map[i][j] = Wood(Position(j, i))

# Filling the bottom right corner with wood:
for i in range(30):
    for j in range(70 + i, 100):
        game_map[i][j] = Wood(Position(j, i))

# Filling the top right corner with wood:
for i in range(80, 100):
    for j in range(179 - i, 100):
        game_map[i][j] = Wood(Position(j, i))

# Fill the middle with stone:
for i in range(40, 60):
    for j in range(40, 60):
        game_map[i][j] = Stone(Position(j, i))

# Put gold around the corners of the large stone deposit:
for i_offset, j_offset in ((-15, -15), (-15, 10), (10, -15), (10, 10)):
    for i in range(50 + i_offset, 50 + i_offset + 5):
        for j in range(50 + j_offset, 50 + j_offset + 5):
            game_map[i][j] = Gold(Position(j, i))

# Adding Food:
for i_start, j_start in ((80, 80), (80, 20), (20, 80), (20, 20)):
    for i in range(i_start, i_start + 4):
        for j in range(j_start - 7, j_start - 4):
            game_map[i][j] = Food(Position(j, i))


for i_start, j_start in ((85, 70), (85, 10), (5, 70), (15, 25)):
    for i in range(i_start, i_start + 2):
        for j in range(j_start, j_start + 2):
            game_map[i][j] = Bronze(Position(j, i))

for i in range(90, 92):
    game_map[i][87] = Gold(Position(87, i))

for i in range(94, 97):
    for j in range(77, 79):
        game_map[i][j] = Stone(Position(j, i))

for i in range(78, 79):
    for j in range(85, 87):
        game_map[i][j] = Stone(Position(j, i))

# The following can be printed, even though it is in the far right column of the map:
game_map[50][99] = Iron(Position(99, 50))

# Adding some Iron at the top of the map (which now can be printed):
for i in range(97, 100):
    for j in range(60, 61):
        game_map[i][j] = Iron(Position(j, i))



if __name__ == '__main__':
    for tpl in ((60, 75), (62, 78), (64, 84), (50, 50)):
        position = Position(*tpl)
        print(position, game_map(position))

    # print(game_map)
    # print('-------------------------------------------------------------------')
    # game_map.print_centered_at(Position(50, 60))
    # print('-------------------------------------------------------------------')
    # game_map.print_centered_at(Position(90, 50))
    # print_map(game_map)
    # The following code was run for various values of distance and Position(i, j):
    # When it was run, the code within the function everything_within_given_distance_on
    # was uncommented so that the map was modified.
    # for i in everything_within_given_distance_on(game_map, 20, Position(5, 92)):
    #     pass
    # print_map(game_map)

    # pos1 = Position(5, 6)
    # vec1 = Vector(2, -1)
    # print(pos1 - vec1)
    # print(vec1.magnitude)


    if len(game_map) == 100 and len(game_map[0]) == 100:
        for tpl in ((-1, 5), (100, 20), (90, 100), (120, 200)):
            position = Position(*tpl)
            assert not position.is_on_the_map(game_map)

