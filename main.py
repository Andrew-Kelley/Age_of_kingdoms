# Age of Kingdoms - A text-based, turn-based strategy game inspired by Age of Empires.
# Started July 21, 2018.

from input_handling import *
from buildings.bldng_class import Building
from buildings.other_bldngs import  TownCenter, House, Blacksmith, Library, Market
from buildings.military_bldngs import Barracks, ArcheryRange, Stable, SiegeWorks
from buildings.defense_bldngs import Tower, Castle
from units import Villager, Pikeman, Swordsman, Archer, Knight, BatteringRam, Catapult, Trebuchet, Merchant

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


game_map  = [[' '] * 100 for i in range(100)]
for i in range(60, 66):
    for j in range(75, 85):
        game_map[i][j] = 'w'

# Eh, I feel like adding more wood:
for i in range(66, 72):
    for j in range(80, 90):
        game_map[i][j] = 'w'

units_ls = [Villager, Pikeman, Swordsman, Archer, Knight, BatteringRam, Catapult, Trebuchet, Merchant]
buildings_ls = [TownCenter, House, Blacksmith, Library, Market, Barracks, ArcheryRange,
                Stable, SiegeWorks, Tower, Castle]
resource_ls = ['food', 'wood', 'stone', 'gold', 'bronze', 'iron']

class Player:
    def __init__(self, number, position, is_human):
        """Players are numbered beginning with 1.

        position is where to place a players beginning TownCenter."""
        global game_map
        self.number = number
        self.is_human = is_human
        self.resources = {'food':300, 'wood':300, 'stone':200, 'gold':0, 'bronze':0, 'iron':0}

        # For each player, House number 1 (i.e. the first house that player builds) will be in
        # self.buildings['houses'][1]. Since no building is numbered 0, each list needs a place-holder
        self.buildings = dict((building.kind, [None]) for building in buildings_ls)
        self.units = dict((unit.kind, [None]) for unit in units_ls)

        Building.build(TownCenter, self, position, game_map)
        self.buildings[TownCenter.kind].append(TownCenter(1, position))

        # Each player begins with 3 villagers
        for i, delta in enumerate([(-2, -2), (2,-2), (2, 2)], start=1):
            new_position = position + Position(*delta)
            self.units[Villager.kind].append(Villager(i, new_position))

    def print_resources(self):
        global resource_ls
        for resource in resource_ls:
            print('{}: {}  '.format(resource,self.resources[resource]),end=' ')
        print()


p1 = Player(1, Position(80, 80), is_human=True)
for villager in p1.units['villagers'][1:]:
    print(villager.number, villager.position)


print(p1.buildings)
print(p1.units)
p1.print_resources()


#TODO: In the docstring for the Building class, specify that position is the south-west corner of the building

#TODO: Add a file as a place to put my tests for buildings. Maybe name it bldng_tests
# t = TownCenter(1, (80, 80))
# Building.build(TownCenter, 1, Position(80,80), game_map)
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

def initial_position_of_player(player_number, game_map):
    """returns the initial position of the player's TownCenter"""
    assert player_number >= 1
    # TODO: write this function properly. For now, it works if player_number <= 4
    length = len(game_map)
    small = length // 5
    large = length - small
    # Placing the players clockwise around the map...
    if player_number == 1:
        return Position(large, large)
    if player_number == 2:
        return Position(large, small)
    if player_number == 3:
        return Position(small, small)
    if player_number == 4:
        return Position(small, large)


print("Starting a game of Age of Kingdoms...")
# n1 = input_number_of_players(human=True)
# n2 = input_number_of_players(human=False)
# Note: for testing purposes, I'll start off with only 1 human player (and no computer players).
n1 = 1
n2 = 0
print("""Ok folks, starting a game with {} human player(s) and {} computer player(s).""".format(n1, n2))


players = [None]
for i in range(1, n1+1):
    players.append(Player(number=i, position=initial_position_of_player(i, game_map), is_human=True))
for i in range(n1+1, n1 + n2 + 1):
    players.append(Player(number=i, position=initial_position_of_player(i, game_map), is_human=False))

for player in players[1:]:
    print("Is player number {} human? {}".format(player.number, player.is_human))


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







