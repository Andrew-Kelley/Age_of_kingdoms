from buildings.bldng_class import Building
from buildings.other_bldngs import TownCenter, House, Blacksmith, Library, Market
from buildings.military_bldngs import Barracks, ArcheryRange, Stable, SiegeWorks
from buildings.defense_bldngs import Tower, Castle

from units import Unit, Villager, Pikeman, Swordsman, Archer, Knight
from units import BatteringRam, Catapult, Trebuchet, Merchant

from resources import Resources

from game_map import game_map, Position, print_map

from copy import deepcopy

units_ls = [Villager, Pikeman, Swordsman, Archer, Knight, BatteringRam, Catapult, Trebuchet, Merchant]
buildings_ls = [TownCenter, House, Blacksmith, Library, Market, Barracks, ArcheryRange,
                Stable, SiegeWorks, Tower, Castle]


class Player:
    def __init__(self, number, position, is_human):
        """Players are numbered beginning with 1.

        position is where to place a player's beginning TownCenter."""
        global game_map
        self.number = number
        self.is_human = is_human
        self.resources = Resources({'food':300, 'wood':300, 'stone':200, 'gold':0, 'bronze':0, 'iron':0})
        self.age = 'Stone Age'
        # self.commands contains the commands entered by the player:
        commands_dict = {'move':dict(), 'build unit':dict()}  # This will need to be lengthened.
        self.commands = {'now':commands_dict, 'later':deepcopy(commands_dict)}
        # 'now' means at the end of the turn, when all players' commands are run.
        # 'later' means at some later turn.

        # For each player, House number 1 (i.e. the first house that player builds) will be in
        # self.buildings['houses'][1]. Since no building is numbered 0, each list needs a place-holder.
        # But since I DO have the space, self.buildings[building_kind][0] will be the number of
        # buildings of that kind that have been destroyed.
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
        total_cap = 300
        # Recall that self.buildings[TownCenter.kind][0] is the number of TownCenters that have
        # been destroyed.
        num_town_centers = len(self.buildings[TownCenter.kind]) - self.buildings[TownCenter.kind][0] - 1
        num_houses = len(self.buildings[House.kind]) - self.buildings[House.kind][0] - 1
        return min(20 * num_town_centers + 10 * num_houses, total_cap)

    @property
    def population(self):
        pop = 0
        for unit in units_ls:
            # Recall that self.units[unit.kind][0] is the number of that unit kind that have been killed.
            pop += len(self.units[unit.kind]) - self.units[unit.kind][0] - 1
        return pop

    def can_build(self, thing, number=1):
        """If thing is a Unit, number is how many of that Unit that is desired to be built PLUS the number
        of other units already OK'd to be built during the next turn."""
        if issubclass(thing, Unit) or isinstance(thing, Unit):
            if self.population > self.population_cap - number:
                return False
        if not self.resources >= thing.cost:
            return False
        return True


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


if __name__ == '__main__':
    from input_handling import input_next_command


    p1 = Player(1, Position(80, 80), is_human=True)
    for villager in p1.units['villagers'][1:]:
        print(villager.number, villager.position)

    inpt = input_next_command(p1)

    print(p1.buildings)
    print(p1.units)
    print(p1.resources)
    print(p1.population_cap)
    print(p1.population)
    t = p1.buildings[TownCenter.kind][1]

    for j in range(4, 22):
        if p1.can_build(Villager):
            t.build_villager(p1)

    print(p1.population)
    print(p1.resources)
    print('ok')
    print_map(game_map)