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
    kind = 'towncenters'

    def build_villager(self, player):
        villager_number = len(player.units[Villager.kind])
        new_villager = Villager(villager_number, self.build_position)
        player.units[Villager.kind].append(new_villager)
        player.resources -= Villager.cost


    def num_villagers_can_build_in_turn(self, player):
        key = {'Stone Age':2, 'Bronze Age':4, 'Iron Age':6}
        return key[player.age]


class House(Building):
    cost = Resources({'wood':100})
    size = (2, 2)
    letter_abbreviation = 'H'
    kind = 'houses'

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
    kind = 'blacksmiths'

class Library(Building):
    cost = Resources({'wood':200, 'gold':100})
    size = (3, 3)
    letter_abbreviation = 'L'
    kind = 'libraries'

# Maybe implement this building last
class Market(Building):
    cost = Resources({'wood':150, 'gold':20})
    size = (3, 3)
    letter_abbreviation = 'M'
    kind = 'markets'

if __name__ == '__main__':
    from game_map import Position
    t = TownCenter(1, Position(50,50))
    print(t.cost)
    print(t.number)
    print(t.position)
