from buildings.other_bldngs import TownCenter, House, Blacksmith, Library, Market
from buildings.other_bldngs import Wonder
from buildings.military_bldngs import Barracks, ArcheryRange, Stable, SiegeWorks
from buildings.defense_bldngs import Tower, Castle
from buildings.resource_bldngs import Farm, LumberCamp, StoneQuarry, MiningCamp

from units import Unit, Villager, Pikeman, Swordsman, Archer, Knight
from units import BatteringRam, Catapult, Trebuchet, Merchant

from colors import Color

from resources import Resources, Food, Wood, Stone, Gold, Bronze, Iron

from game_map import game_map, Position

from copy import deepcopy

units_ls = [Villager, Pikeman, Swordsman, Archer, Knight,
            BatteringRam, Catapult, Trebuchet, Merchant]
buildings_ls = [TownCenter, House, Blacksmith, Library, Market,
                Barracks, ArcheryRange, Stable, SiegeWorks, Tower,
                Castle, Farm, LumberCamp, StoneQuarry, MiningCamp,
                Wonder]

# Eventually, maybe I ought to let the players choose their colors.

colors = ['', Color.DARK_BLUE, Color.GREEN, Color.MAGENTA,
          Color.RED, Color.LIGHT_BLUE]

class Player:
    def __init__(self, number, position, is_human):
        """Players are numbered beginning with 1.

        position is where to place a player's beginning TownCenter."""
        self.number = number
        self.color = colors[self.number % len(colors)]
        self.is_human = is_human
        self.resources = Resources({Food: 300, Wood: 300, Stone: 200,
                                    Gold: 0, Bronze: 0, Iron: 0})
        self.age = 'stone age'

        # The following is how much of a given resource a single villager
        # can collect in one turn.
        self.collecting_capacity = {Wood: 8, Food: 10, Stone: 6,
                                    Gold: 6, Bronze: 6, Iron: 2}

        # self.commands contains the commands entered by the player:
        commands_dict = {'move': dict(), 'build unit': dict(),
                         'build building': dict(),
                         'collect resource': dict(),
                         'farm': dict(), 'research': dict()}
        # commands_dict will need to be lengthened
        self.commands = {'now': commands_dict, 'later': deepcopy(commands_dict)}
        # 'now' means at the end of the turn, when all players' commands are run.
        # 'later' means at some later turn.

        self._commands_history = []

        # self.messages is for printing messages that are produced
        # while the player's commands are implemented.
        self.messages = ''

        self.things_researched = set()
        self.things_being_currently_researched = set()

        # For each player, House number 1 (i.e. the first house that
        # player builds) will be at self.buildings['houses'][1]. Since
        # no building is numbered 0, each list needs a placeholder.
        # But since I DO have the space, self.buildings[building_kind][0]
        # will be the number of buildings of that kind that have been
        # destroyed.
        self.buildings = dict((building.kind, [0]) for building in buildings_ls)

        # For each each of the player's buildings, the following will
        # contain a key: value pair as follows:
        #  position: building_instance
        self.building_position_pairs = dict()
        self.units = dict((unit.kind, [0]) for unit in units_ls)

        towncenter = TownCenter(1, position, self)
        towncenter.build_on_map(position, game_map)
        self.buildings[TownCenter.kind].append(towncenter)

        # Each player begins with 3 villagers
        for i, delta in enumerate([(-2, -2), (2, -2), (2, 2)], start=1):
            new_position = position + Position(*delta)
            Villager(new_position, self)

    def log_command(self, cmd_as_inpt_string):
        """Temporarily save the command entered by adding it to
        the list that keeps track of all (valid-ish) commands."""
        self._commands_history.append(cmd_as_inpt_string)

    @property
    def population_cap(self):
        total_cap = 300
        # Recall that self.buildings[TownCenter.kind][0] is the number
        # of TownCenters that have been destroyed.
        num_tc_destroyed = self.buildings[TownCenter.kind][0]
        num_town_centers = len(self.buildings[TownCenter.kind]) - num_tc_destroyed - 1
        num_houses_destroyed = self.buildings[House.kind][0]
        num_houses = len(self.buildings[House.kind]) - num_houses_destroyed - 1
        return min(20 * num_town_centers + 10 * num_houses, total_cap)

    @property
    def population(self):
        pop = 0
        for unit in units_ls:
            # Recall that self.units[unit.kind][0] is the number of that unit
            # kind that have been killed.
            num_units_killed = self.units[unit.kind][0]
            pop += len(self.units[unit.kind]) - num_units_killed - 1
        return pop

    def can_build(self, thing, number=1):
        """If thing is a Unit, number is how many of that Unit that is desired
        to be built PLUS the number of other units already OK'd to be built during
        the next turn."""
        if issubclass(thing, Unit) or isinstance(thing, Unit):
            if self.population > self.population_cap - number:
                return False
        if not self.resources >= thing.cost:
            return False
        return True

    def print_and_clear_messages(self):
        if self.messages:
            print(self.messages)
            self.messages = ''

    def compare_to(self, other):
        pass


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
    from input_handling.get_input import input_next_command

    p1 = Player(1, Position(80, 80), is_human=True)
    for villager in p1.units['villagers'][1:]:
        print(villager.number, villager.position)

    # inpt = input_next_command(p1)

    print(p1.buildings)
    print(p1.units)
    print(p1.resources)
    print(p1.population_cap)
    print(p1.population)
    t = p1.buildings[TownCenter.kind][1]

    for j in range(4, 22):
        if p1.can_build(Villager):
            t.build_unit(Villager.kind)

    print(p1.population)
    print(p1.resources)
    print('ok')
    print(game_map)
