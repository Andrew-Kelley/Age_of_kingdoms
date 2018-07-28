# Age of Kingdoms - A text-based, turn-based strategy game inspired by Age of Empires.
# Started July 21, 2018.

from input_handling import *
from buildings.bldng_class import Building
from buildings.other_bldngs import  TownCenter, House, Blacksmith, Library, Market
from buildings.military_bldngs import Barracks, ArcheryRange, Stable, SiegeWorks
from buildings.defense_bldngs import Tower, Castle

from units import Villager, Pikeman, Swordsman, Archer, Knight, BatteringRam, Catapult, Trebuchet, Merchant

from resources import Resources

from game_map import game_map, Position, print_map

units_ls = [Villager, Pikeman, Swordsman, Archer, Knight, BatteringRam, Catapult, Trebuchet, Merchant]
buildings_ls = [TownCenter, House, Blacksmith, Library, Market, Barracks, ArcheryRange,
                Stable, SiegeWorks, Tower, Castle]
resource_ls = ['food', 'wood', 'stone', 'gold', 'bronze', 'iron']

class Player:
    def __init__(self, number, position, is_human):
        """Players are numbered beginning with 1.

        position is where to place a player's beginning TownCenter."""
        global game_map
        self.number = number
        self.is_human = is_human
        self.resources = Resources({'food':300, 'wood':300, 'stone':200, 'gold':0, 'bronze':0, 'iron':0})

        # For each player, House number 1 (i.e. the first house that player builds) will be in
        # self.buildings['houses'][1]. Since no building is numbered 0, each list needs a place-holder. But
        # since I DO have the space, self.buildings[building_kind][0] will be the number of buildings of that
        # kind that have been destroyed.
        self.buildings = dict((building.kind, [0]) for building in buildings_ls)
        self.units = dict((unit.kind, [0]) for unit in units_ls)

        Building.build(TownCenter, self, position, game_map)
        self.buildings[TownCenter.kind].append(TownCenter(1, position))

        # Each player begins with 3 villagers
        for i, delta in enumerate([(-2, -2), (2,-2), (2, 2)], start=1):
            new_position = position + Position(*delta)
            self.units[Villager.kind].append(Villager(i, new_position))

    @property
    def population_cap(self):
        # Recall that self.buildings[TownCenter.kind][0] is the number of TownCenters that have been destroyed.
        num_town_centers = len(self.buildings[TownCenter.kind]) - self.buildings[TownCenter.kind][0] - 1
        num_houses = len(self.buildings[House.kind]) - self.buildings[House.kind][0] - 1
        return 20 * num_town_centers + 10 * num_houses

    @property
    def population(self):
        pop = 0
        for unit in units_ls:
            # Recall that self.units[unit.kind][0] is the number of that unit kind that have been killed.
            pop += len(self.units[unit.kind]) - self.units[unit.kind][0] - 1
        return pop


p1 = Player(1, Position(80, 80), is_human=True)
for villager in p1.units['villagers'][1:]:
    print(villager.number, villager.position)


print(p1.buildings)
print(p1.units)
print(p1.resources)
print(p1.population_cap)
print(p1.population)

# Testing TownCenter methods can_build_villager and build_villager:
t = TownCenter(2, Position(50, 50))
print(t.can_build_villager(p1))

for j in range(4, 12):
    if t.can_build_villager(p1):
        t.build_villager(p1)
        print(p1.resources)
    print(p1.population)

print(p1.population)
print('ok folks')


print_map(game_map)

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

