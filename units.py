

class Unit:
    """e.g. villager, swordsman, knight, catapult"""
    def __init__(self, number, position):
        """For each player, the first of each unit is numbered 1.
        Further units built (of the same type) are consecutively numbered.

        The position attribute is where on the map the unit starts."""
        self.number = number
        self.position = position


class Villager(Unit):
    kind = 'villagers'

class Pikeman(Unit):
    kind = 'pikemen'

class Swordsman(Unit):
    kind = 'swordsmen'

class Archer(Unit):
    kind = 'archers'

class Knight(Unit):
    kind = 'knights'

class BatteringRam(Unit):
    kind = 'batteringrams'

class Catapult(Unit):
    kind = 'catapults'

class Trebuchet(Unit):
    kind = 'trebuchets'

class Merchant(Unit):
    kind = 'merchants'
