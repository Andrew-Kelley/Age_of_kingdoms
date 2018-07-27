from buildings.bldng_class import Building

class TownCenter(Building):
    """Every player begins with one TownCenter.
    More can be built in the Iron Age."""
    cost = {'wood':300, 'stone':200}
    size = (4, 4)
    letter_abbreviation = 'T'
    # hit_points = ?
    # construction_time = ?
    population_support = 20
    garrison_capacity = 50
    defensible = True
    kind = 'towncenters'


class House(Building):
    cost = {'wood':100}
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
    cost = {'wood':150, 'stone':25}
    size = (3, 3)
    letter_abbreviation = 'X'
    kind = 'blacksmiths'

class Library(Building):
    cost = {'wood':200, 'gold':100}
    size = (3, 3)
    letter_abbreviation = 'L'
    kind = 'libraries'

# Maybe implement this building last
class Market(Building):
    cost = {'wood':150, 'gold':20}
    size = (3, 3)
    letter_abbreviation = 'M'
    kind = 'markets'

if __name__ == '__main__':
    from game_map import Position
    t = TownCenter(1, Position(50,50))
    print(t.cost)
    print(t.number)
    print(t.position)
