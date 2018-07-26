# Age of Kingdoms - A text-based, turn-based strategy game inspired by Age of Empires.
# Started July 21, 2018.

from input_handling import *
from buildings.bldng_class import Building
from buildings.other_bldngs import  TownCenter, House, Blacksmith, Library, Market
from buildings.defense_bldngs import Tower, Castle
from units import Villager

class Position:
    """The i and j coordinates of a position on the map"""
    def __init__(self, i, j):
        self.value = (i, j)

    def __add__(self, other):
        i = self.value[0] + other.value[0]
        j = self.value[1] + other.value[1]
        return Position(i, j)

    def __repr__(self):
        return str(self.value)


class Player:
    def __init__(self, number, is_human):
        """Players are numbered beginning with 1."""
        self.number = number
        self.is_human = is_human



game_map  = [[' '] * 100 for i in range(100)]
for i in range(60, 66):
    for j in range(75, 85):
        game_map[i][j] = 'w'

#TODO: In the docstring for the Building class, specify that position is the south-west corner of the building

#TODO: Add a file as a place to put my tests for buildings. Maybe name it bldng_tests
# t = TownCenter(1, (80, 80))
Building.build(TownCenter, 1, Position(80,80), game_map)
# build(TownCenter, 1, (80,80))

for tpl in ((4,4), (2,4), (99,0), (100, 0), (90,96), (90, 97), (10, 0), (10, -1)):
    position = Position(*tpl)
    yes_or_no = Building.can_build(TownCenter, position, game_map)
    print(position, yes_or_no)
    print()

for tpl in ((82, 80), (81,80), (76,80), (77, 80), (80,84), (80,83)):
    position = Position(*tpl)
    yes_or_no = Building.can_build(House, position, game_map)
    print(position, yes_or_no)
    print()

for ls in game_map:
    print(''.join(ls))



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

# NOTE:
print('For testing purposes, the following code only works for 1 human player and 0 computer players.')
num_human_players = n1 # I'm renaming them to make possible error messages more informative
num_computer_players = n2
# assert num_human_players == 1
# assert num_computer_players == 0

turn_number = 0
while True:
    turn_number += 1
    if turn_number > 100: # This should eventually be changed to 1000
        print('The limit of {} turns has been reached. Game over.'.format(turn_number - 1))
        break

    for player in players[1:]:
        print("It is now Player number {}'s turn".format(player.number))
        if player.is_human:
            print('Yay, you are human')







