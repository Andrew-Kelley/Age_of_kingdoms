from buildings.bldng_class import Building, buildings
from units import Villager
from resources import Resources, Food, Wood, Stone, Gold, Bronze, Iron
from research_classes import BronzeAge, IronAge, blacksmith_bronze_age_research
from research_classes import bronze_to_iron_research_str

from buildings.defense_bldngs import WoodWall, StoneWall, WallFortification, Tower, Castle
from buildings.military_bldngs import Barracks, ArcheryRange, Stable, SiegeWorks
from buildings.resource_bldngs import Farm, LumberCamp, StoneQuarry, MiningCamp

from command_handling.insert_commands import insert_move_later_command
from command_handling.insert_commands import insert_collect_resource_later_command
from command_handling.insert_commands import insert_collect_resource_now_command
from command_handling.commands import MoveCmd

class TownCenter(Building):
    """Every player begins with one TownCenter.
    More can be built in the Iron Age."""
    cost = Resources({Wood: 300, Stone: 200})
    size = (4, 4)
    letter_abbreviation = 'T'
    # hit_points = ?
    population_support = 20
    garrison_capacity = 50
    defensible = True
    kind = 'towncenter'
    time_to_build = 160

    def __init__(self, number, position, player):
        Building.__init__(self, number, position, player)
        # The following can be altered by the player and is used for the
        # default initial action of a newly built villager.
        self.initial_resource_to_collect = None

    def things_which_can_be_researched(self):
        research_ls = []
        # Maybe have a 'wheelbarrow', which makes all villagers more efficient
        # at anything they do 'wheelbarrow' could be researched in the bronze age

        player = self.player
        if player.age == 'stone age':
            research_ls.append('bronze age')
        elif player.age == 'bronze age':
            research_ls.append('iron age')
        return research_ls

    def units_which_can_be_built(self):
        return ['villagers']

    def build_unit(self, unit_type='villagers'):
        player = self.player
        if unit_type != 'villagers':
            print('Error! A TownCenter can only build Villagers.')
            return
        # villager_number = len(player.units[Villager.kind])
        delta = self.build_position - self.position

        if delta.magnitude > 6:
            delta1, delta2 = delta.beginning_plus_the_rest(distance_in_one_turn=6)
            build_position = self.position + delta1
            new_villager = Villager(build_position, player)
            command = MoveCmd()
            command.add_unit_with_delta(new_villager, delta2)
            insert_move_later_command(player, command)
        else:
            new_villager = Villager(self.build_position, player)
        if self.initial_resource_to_collect:
            command = ['collect resource',
                       self.initial_resource_to_collect, [new_villager]]
            if delta.magnitude <= 6:
                insert_collect_resource_now_command(player, command)
            else:
                insert_collect_resource_later_command(player, command)

        # player.units[Villager.kind].append(new_villager)
        player.messages += 'New unit: {}\n'.format(new_villager)
        player.resources -= Villager.cost

    def num_villagers_can_build_in_turn(self, player):
        # At one point, I thought a towncenter should be able to
        # build a different number of villagers in the different ages,
        # but now I'm thinking to keep it at 1. Perhaps some research
        # at the library/university will increase this number.

        # The following two lines is what it used to be:
        # key = {'stone age': 1, 'bronze age': 2, 'iron age': 3}
        # return key[player.age]
        return 1


class House(Building):
    cost = Resources({Wood: 100})
    size = (2, 2)
    letter_abbreviation = 'H'
    kind = 'house'
    time_to_build = 30


class Blacksmith(Building):
    # Can only be built once the Bronze Age is reached.
    cost = Resources({Wood: 150, Stone: 25})
    size = (3, 3)
    letter_abbreviation = 'X'
    kind = 'blacksmith'
    time_to_build = 50

    def things_which_can_be_researched(self):
        player = self.player
        research_ls = []
        for research_obj in blacksmith_bronze_age_research:
            if research_obj.name not in player.things_researched:
                research_ls.append(research_obj.name)

        if player.age == 'iron age':
            for research_obj in blacksmith_bronze_age_research:
                if research_obj.name in bronze_to_iron_research_str:
                    if research_obj.name in player.things_researched:
                        research_obj_str = bronze_to_iron_research_str[research_obj.name]
                        if research_obj_str not in player.things_researched:
                            research_ls.append(research_obj_str)

        return research_ls


class Library(Building):
    cost = Resources({Wood: 200, Gold: 100})
    size = (3, 3)
    letter_abbreviation = 'L'
    kind = 'library'
    time_to_build = 80


class Wonder(Building):
    cost = Resources({Wood: 1500, Stone: 1200, Gold: 1000, Iron: 1000})
    size = (6, 6)
    letter_abbreviation = 'W'
    kind = 'wonder'
    time_to_build = 700

# Maybe implement this building last
class Market(Building):
    cost = Resources({Wood: 150, Gold: 20})
    size = (3, 3)
    letter_abbreviation = 'M'
    kind = 'market'
    time_to_build = 50


building_kind_to_class =  {'house':House, 'lumbercamp':LumberCamp,
                           'stonequarry':StoneQuarry,
                           'miningcamp':MiningCamp, 'woodwall':WoodWall,
                           'barracks':Barracks,
                           'farm':Farm, 'stonewall':StoneWall,
                           'wallfortification':WallFortification,
                           'tower':Tower, 'archeryrange':ArcheryRange,
                           'siegeworks':SiegeWorks,
                           'blacksmith':Blacksmith, 'market':Market,
                           'towncenter':TownCenter,
                           'castle':Castle, 'stable':Stable, 'library':Library,
                           'wonder':Wonder}


if __name__ == '__main__':
    from game_map import Position
    from player import Player

    p1 = Player(1, Position(80, 80), is_human=True)
    t = TownCenter(1, Position(50, 50), p1)
    print(t.cost)
    print(t.number)
    print(t.position)
