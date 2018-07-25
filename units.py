

class Unit:
    """e.g. villager, swordsman, knight, catapult"""
    def __init__(self, number, position):
        """For each player, the first of each unit is numbered 1.
        Further units built (of the same type) are consecutively numbered.

        The position attribute is where on the map the unit starts."""
        self.number = number
        self.position = position


class Villager(Unit):
    pass

class Pikeman(Unit):
    pass

class Swordsman(Unit):
    pass

class Archer(Unit):
    pass

class Knight(Unit):
    pass

class BatteringRam(Unit):
    pass

class Catapult(Unit):
    pass

class Trebuchet(Unit):
    pass

class Merchant(Unit):
    pass