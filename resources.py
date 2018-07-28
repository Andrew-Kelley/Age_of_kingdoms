from copy import copy

resource_ls = ['food', 'wood', 'stone', 'gold', 'bronze', 'iron']

# The purpose of having this class is to enable subtraction of the dictionaries whenever resources are being
# used. Also, printing is now standardized.
class Resources(dict):
    def __sub__(self, other):
        """Intended use: self is a player's resources, and other is the cost of
        something (i.e. cost of researching something or of building a unit or
        a building.)"""
        updated_resources = copy(self)
        for resource in other:
            updated_resources[resource] -= other[resource]
        return updated_resources

    def __repr__(self):
        global resource_ls
        ls_of_what_to_print = []
        for resource in resource_ls:
            if resource not in self: # This is so that resource costs can also be printed. Costs never include
                continue             # all possible resources.
            ls_of_what_to_print.append('{}: {}   '.format(resource,self[resource]))
        return ''.join(ls_of_what_to_print)

    def __ge__(self, other):
        """self must include every resource that other includes"""
        return all(self[resource] >= other[resource] for resource in other)




if __name__ == '__main__':
    from units import Villager, Pikeman

    my_resources = Resources({'food':300, 'wood':300, 'stone':200, 'gold':0, 'bronze':0, 'iron':0})
    some_cost = Resources({'food':300, 'wood':300, 'stone':200})

    assert my_resources >= some_cost
    assert my_resources >= Villager.cost
    assert my_resources >= Pikeman.cost

    print(my_resources)
    Villager.cost = Resources(Villager.cost)
    Pikeman.cost = Resources(Pikeman.cost)
    my_resources -= Villager.cost
    print(my_resources)
    my_resources -= Villager.cost
    print(my_resources)
    my_resources -= Pikeman.cost
    print(my_resources)


