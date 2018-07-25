# Age of Kingdoms - A text-based, turn-based strategy game inspired by Age of Empires.
# Started July 21, 2018.

class Player:
    pass


game_map  = [[' '] * 100 for i in range(100)]
for i in range(60, 66):
    for j in range(75, 85):
        game_map[i][j] = 'w'

# for ls in game_map:
#     print(''.join(ls))

