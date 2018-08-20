from buildings.bldng_class import Building, buildings
from units import Villager
from resources import Resources, Wood, Stone, Gold

from buildings.defense_bldngs import WoodWall, StoneWall, WallFortification, Tower, Castle
from buildings.military_bldngs import Barracks, ArcheryRange, Stable, SiegeWorks
from buildings.resource_bldngs import Farm, LumberCamp, StoneQuarry, MiningCamp


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

    def units_which_can_be_built(self, player):
        return ['villagers']

    def things_which_can_be_researched(self, player):
        research_ls = []
        # Maybe have a 'wheelbarrow', which makes all villagers more efficient at anything they do
        # 'wheelbarrow' could be researched in the bronze age

        # Note: the following is capitalized correctly, despite the inconsistency.
        # The reason why everything in research_ls must be lower case is that the user's input
        # is always converted to lower case.
        if player.age == 'Stone Age':
            research_ls.append('bronze age')
        elif player.age == 'Bronze Age':
            research_ls.append('iron age')
        return research_ls

    def build_unit(self, player, unit_type='villagers'):
        if unit_type != 'villagers':
            print('Error! A TownCenter can only build Villagers.')
            return
        villager_number = len(player.units[Villager.kind])
        new_villager = Villager(villager_number, self.build_position)
        player.units[Villager.kind].append(new_villager)
        player.resources -= Villager.cost

    def num_villagers_can_build_in_turn(self, player):
        key = {'Stone Age': 1, 'Bronze Age': 2, 'Iron Age': 3}
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
