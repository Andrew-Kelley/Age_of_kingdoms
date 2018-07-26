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


class House(Building):
    size = (2, 2)
    letter_abbreviation = 'H'

class Blacksmith(Building):
    size = (3, 3)
    letter_abbreviation = 'X'

class Library(Building):
    size = (3, 3)
    letter_abbreviation = 'L'

# Maybe implement this building last
class Market(Building):
    size = (3, 3)
    letter_abbreviation = 'M'

if __name__ == '__main__':
    t = TownCenter(1)
    print(t.cost)
    print(t.number)
