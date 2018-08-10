from buildings.bldng_class import Building
from units import Villager
from resources import Resources

class TownCenter(Building):
    """Every player begins with one TownCenter.
    More can be built in the Iron Age."""
    cost = Resources({'wood':300, 'stone':200})
    size = (4, 4)
    letter_abbreviation = 'T'
    # hit_points = ?
    # construction_time = ?
    population_support = 20
    garrison_capacity = 50
    defensible = True
    kind = 'towncenter'

    def units_which_can_be_built(self, player):
        return ['villagers']

    def build_unit(self, player, unit_type='villagers'):
        if unit_type != 'villagers':
            print('Error! A TownCenter can only build Villagers.')
            return
        villager_number = len(player.units[Villager.kind])
        new_villager = Villager(villager_number, self.build_position)
        player.units[Villager.kind].append(new_villager)
        player.resources -= Villager.cost


    def num_villagers_can_build_in_turn(self, player):
        key = {'Stone Age':1, 'Bronze Age':2, 'Iron Age':3}
        return key[player.age]


class House(Building):
    cost = Resources({'wood':100})
    size = (2, 2)
    letter_abbreviation = 'H'
    kind = 'house'

class Blacksmith(Building):
    # Can only be built once the Bronze Age is reached.
    # The following can be researched here:
    # -bronze tipped spears (benefits Pikeman) - shouldn't be too expensive
    # -bronze armor (benefits Pikeman and is necessary to build Swordsman)
    # -bronze shields (is necessary to build Swordsman)
    # -bronze axes (benefits Villagers which are chopping wood)
    # -bronze picks (benefits Villagers which are mining gold or bronze)
    cost = Resources({'wood':150, 'stone':25})
    size = (3, 3)
    letter_abbreviation = 'X'
    kind = 'blacksmith'

class Library(Building):
    cost = Resources({'wood':200, 'gold':100})
    size = (3, 3)
    letter_abbreviation = 'L'
    kind = 'library'

# Maybe implement this building last
class Market(Building):
    cost = Resources({'wood':150, 'gold':20})
    size = (3, 3)
    letter_abbreviation = 'M'
    kind = 'market'

if __name__ == '__main__':
    from game_map import Position
    t = TownCenter(1, Position(50,50))
    print(t.cost)
    print(t.number)
    print(t.position)
