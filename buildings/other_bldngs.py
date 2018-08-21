from buildings.bldng_class import Building, buildings
from units import Villager
from resources import Resources, Food, Wood, Stone, Gold, Bronze
from research_classes import BronzeAge, IronAge

from buildings.defense_bldngs import WoodWall, StoneWall, WallFortification, Tower, Castle
from buildings.military_bldngs import Barracks, ArcheryRange, Stable, SiegeWorks
from buildings.resource_bldngs import Farm, LumberCamp, StoneQuarry, MiningCamp

from command_handling import insert_move_later_command, insert_collect_resource_later_command
from command_handling import insert_collect_resource_now_command

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
    # time_to_build = ?

    def __init__(self, number, position):
        Building.__init__(self, number, position)
        # The following can be altered by the player and is used for the default initial action
        # of a newly built villager.
        self.initial_resource_to_collect = None

    def strings_ls_of_things_which_can_be_researched(self, player):
        research_ls = []
        # Maybe have a 'wheelbarrow', which makes all villagers more efficient at anything they do
        # 'wheelbarrow' could be researched in the bronze age

        if player.age == 'stone age':
            research_ls.append('bronze age')
        elif player.age == 'bronze age':
            research_ls.append('iron age')
        return research_ls

    def units_which_can_be_built(self, player):
        return ['villagers']

    def build_unit(self, player, unit_type='villagers'):
        if unit_type != 'villagers':
            print('Error! A TownCenter can only build Villagers.')
            return
        villager_number = len(player.units[Villager.kind])
        delta = self.build_position - self.position

        if delta.magnitude > 6:
            delta1, delta2 = delta.beginning_plus_the_rest(distance_in_one_turn=6)
            build_position = self.position + delta1
            new_villager = Villager(villager_number, build_position)
            command = ['move', [new_villager], delta2]
            insert_move_later_command(player, command)
        else:
            new_villager = Villager(villager_number, self.build_position)
        if self.initial_resource_to_collect:
            command = ['collect resource', self.initial_resource_to_collect, [new_villager]]
            if delta.magnitude <= 6:
                insert_collect_resource_now_command(player, command)
            else:
                insert_collect_resource_later_command(player, command)

        player.units[Villager.kind].append(new_villager)
        player.resources -= Villager.cost

    def num_villagers_can_build_in_turn(self, player):
        key = {'stone age': 1, 'bronze age': 2, 'iron age': 3}
        return key[player.age]


class House(Building):
    cost = Resources({Wood: 100})
    size = (2, 2)
    letter_abbreviation = 'H'
    kind = 'house'
    time_to_build = 30


class Blacksmith(Building):
    # Can only be built once the Bronze Age is reached.
    # The following can be researched here:
    # -bronze tipped spears (benefits Pikeman) - shouldn't be too expensive
    # -bronze armor (benefits Pikeman and is necessary to build Swordsman)
    # -bronze shields (is necessary to build Swordsman)
    # -bronze axes (benefits Villagers which are chopping wood)
    # -bronze picks (benefits Villagers which are mining stone, gold, bronze, or iron)
    #       specifically, it makes player.collecting_capacity[stone or gold or bronze] = 8
    #                 and it makes player.collecting_capacity[iron] = 6
    cost = Resources({Wood: 150, Stone: 25})
    size = (3, 3)
    letter_abbreviation = 'X'
    kind = 'blacksmith'
    # time_to_build = ?


class Library(Building):
    cost = Resources({Wood: 200, Gold: 100})
    size = (3, 3)
    letter_abbreviation = 'L'
    kind = 'library'
    # time_to_build = ?

# Maybe implement this building last
class Market(Building):
    cost = Resources({Wood: 150, Gold: 20})
    size = (3, 3)
    letter_abbreviation = 'M'
    kind = 'market'
    # time_to_build = ?


building_kind_to_class =  {'house':House, 'lumbercamp':LumberCamp, 'stonequarry':StoneQuarry,
                           'miningcamp':MiningCamp, 'woodwall':WoodWall, 'barracks':Barracks,
                           'farm':Farm, 'stonewall':StoneWall, 'wallfortification':WallFortification,
                           'tower':Tower, 'archeryrange':ArcheryRange, 'siegeworks':SiegeWorks,
                           'blacksmith':Blacksmith, 'market':Market, 'towncenter':TownCenter,
                           'castle':Castle, 'stable':Stable, 'library':Library}


if __name__ == '__main__':
    from game_map import Position

    t = TownCenter(1, Position(50, 50))
    print(t.cost)
    print(t.number)
    print(t.position)
