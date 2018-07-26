# Age of Kingdoms - A text-based, turn-based strategy game inspired by Age of Empires.
# Started July 21, 2018.

from input_handling import *

class Player:
    def __init__(self, number, is_human):
        """Players are numbered beginning with 1."""
        self.number = number
        self.is_human = is_human

turn_number = 0

game_map  = [[' '] * 100 for i in range(100)]
for i in range(60, 66):
    for j in range(75, 85):
        game_map[i][j] = 'w'

# for ls in game_map:
#     print(''.join(ls))



print("Starting a game of Age of Kingdoms...")
n1 = input_number_of_players(human=True)
n2 = input_number_of_players(human=False)

print("""Ok folks, starting a game with {} human player(s) and {} computer player(s).""".format(n1, n2))

players = [None]
for i in range(1, n1+1):
    players.append(Player(number=i,is_human=True))
for i in range(n1+1, n1 + n2 + 1):
    players.append(Player(number=i,is_human=False))

for player in players[1:]:
    print("Is player number {} human? {}".format(player.number, player.is_human))

while True:
    turn_number += 1
    if turn_number > 1000:
        break







