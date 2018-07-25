from buildings.bldng_class import Building

class TownCenter(Building):
    """Every player begins with one TownCenter.
    More can be built in the Iron Age."""
    cost = {'wood':300, 'stone':200}
    size = (4,4)
    # hit_points = ?
    # construction_time = ?
    population_support = 20
    garrison_capacity = 50
    defensible = True


class House(Building):
    pass

class Blacksmith(Building):
    pass

class Library(Building):
    pass

# Maybe implement this building last
class Market(Building):
    pass

if __name__ == '__main__':
    t = TownCenter(1)
    print(t.cost)
    print(t.number)
