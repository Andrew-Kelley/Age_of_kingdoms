# IMPORTANT NOTE: Resources are represented in two different ways.
#
# (a) wood, stone, etc. to be collected by villagers are represented
# by (instances of) their respective classes, which inherit from the
# Resource class.
#
# (b) Also, the amount of resources a player has is represented by a
# modified dictionary (an instance of the class Resources below).
# Also, the cost of building/researching anything in the game is
# also represented as an instance of the Resources class.

from copy import copy


# NOTE: Do not confuse this class with the Resources (plural) class.
class Resource:
    pass


class Wood(Resource):
    """Also called trees."""
    kind = 'wood'
    letter_abbreviation = 'w'

    def __init__(self, position):
        self.position = position
        self.amount_left = 120

    def __str__(self):
        return 'w'


# I might have a couple of types of Food (berry bushes, fruit trees, deer)
# inherit from Food. Also, deer might also inherit from Unit.
class Food(Resource):
    kind = 'food'
    letter_abbreviation = 'f'

    def __init__(self, position):
        self.position = position
        # The following might change for some Food subclasses (to be made later).
        self.amount_left = 150

    def __str__(self):
        return 'f'


class Stone(Resource):
    kind = 'stone'
    letter_abbreviation = 's'

    def __init__(self, position):
        self.position = position
        self.amount_left = 400

    def __str__(self):
        return 's'


class Gold(Resource):
    kind = 'gold'
    letter_abbreviation = 'g'

    def __init__(self, position):
        self.position = position
        self.amount_left = 400

    def __str__(self):
        return 'g'


class Bronze(Resource):
    kind = 'bronze'
    letter_abbreviation = 'b'

    def __init__(self, position):
        self.position = position
        self.amount_left = 400

    def __str__(self):
        return 'b'


class Iron(Resource):
    kind = 'iron'
    letter_abbreviation = 'i'

    def __init__(self, position):
        self.position = position
        self.amount_left = 400

    def __str__(self):
        return 'i'


resource_ls = [Food, Wood, Stone, Gold, Bronze, Iron]
resource_kind_to_class = dict((resource.kind, resource) for resource in resource_ls)


# The purpose of having this class is to enable subtraction of the dictionaries
# whenever resources are being used. Also, printing is now standardized.
class Resources(dict):
    def __sub__(self, other):
        """Intended use: self is a player's resources, and other is the cost of
        something (i.e. cost of researching something or of building a unit or
        a building.)"""
        updated_resources = copy(self)
        for resource in other:
            updated_resources[resource] -= other[resource]
        return updated_resources

    def __mul__(self, n):
        updated_resources = copy(self)
        for resource in self:
            updated_resources[resource] *= n
        return updated_resources

    def __repr__(self):
        global resource_ls
        ls_of_what_to_print = []
        for resource in resource_ls:
            # The following is so that resource costs can also be printed. Costs
            # never include all possible resources.
            if resource not in self:
                continue
            ls_of_what_to_print.append('{}: {}   '.format(resource.kind, self[resource]))
        return ''.join(ls_of_what_to_print)

    def __ge__(self, other):
        """self must include every resource that other includes"""
        return all(self[resource] >= other[resource] for resource in other)


if __name__ == '__main__':
    from units.unit_costs import unit_costs

    my_resources = Resources({Food: 300, Wood: 300, Stone: 200,
                              Gold: 0, Bronze: 0, Iron: 0})
    some_cost = Resources({Food: 300, Wood: 300, Stone: 200})

    print("I think these tests fail because the imported Resources subclasses")
    print("are different in memory than the classes here.")
    assert my_resources >= some_cost
    assert my_resources >= unit_costs['villagers']
    assert my_resources >= unit_costs['pikemen']

    print(my_resources)
    my_resources -= unit_costs['villagers']
    print(my_resources)
    my_resources -= unit_costs['villagers']
    print(my_resources)
    my_resources -= unit_costs['pikemen']
    print(my_resources)
