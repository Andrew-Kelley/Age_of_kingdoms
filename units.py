from resources import Resources

class Unit:
    """e.g. villager, swordsman, knight, catapult"""
    def __init__(self, number, position):
        """For each player, the first of each unit is numbered 1.
        Further units built (of the same type) are consecutively numbered.

        The position attribute is where on the map the unit starts."""
        self.number = number
        self.position = position

    def can_move(self, delta, game_map):
        """Returns bool. Right now, every unit can move the same distance, but that may change.

        delta must be of type Vector"""
        if delta.magnitude > 15:
            # Then delta is too big
            return False
        # Next, check if the proposed movement moves the unit outside the map
        new_position = self.position + delta
        if not new_position.is_on_the_map(game_map):
            return False

        #TODO eventually: add a check to keep the unit from moving across enemy walls
        return True

    def move_by(self, delta):
        """delta must of of type Position"""
        self.position += delta

class Army:
    """A collection of some units for military purposes."""
    pass

# Should Group inherit from Army? Or should Group be more general than its docstring states and then have
# Army inherit from Group?
class Group:
    """A collection of villagers."""
    pass

class Villager(Unit):
    cost = Resources({'food':50})
    kind = 'villagers'

# Unless Pikeman are vastly weaker than Swordsman, I think that the cost difference between Pikeman and
# Swordsman will result in many more Pikeman being built at the beginning of the game. I think that this is OK.
# I intend Pikeman to only be somewhat weaker than Swordsman
class Pikeman(Unit):
    """A man with a spear and a shield"""
    cost = Resources({'food':40, 'wood':15})
    kind = 'pikemen'

class Swordsman(Unit):
    # After reaching the Bronze Age, before being able to train Swordsman, three things must first be researched
    # at the Blacksmith: (a) bronze armor, (b) bronze shields, and (b) bronze swords. (The first of these
    # also benefits Pikeman (by upgrading their armor to bronze)
    cost = Resources({'food':40, 'gold':25, 'bronze':30})
    kind = 'swordsmen'

class Archer(Unit):
    cost = Resources({'wood':40, 'gold':25, 'bronze':15})
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


if __name__ == '__main__':
    from game_map import Position, Vector, game_map
    v1 = Villager(1, Position(50, 50))
    print(v1.number, v1.position)
    v1.move_by(Vector(5, 8))
    print(v1.number, v1.position)

    v2 = Villager(2, Position(5, 5))
    for tpl in ((-5, -5), (7, 8), (-4, 11), (3, 6)):
        delta = Vector(*tpl)
        assert v2.can_move(delta, game_map)
    print(v2.position)

    for tpl in ((-6, -5), (-5, -6), (10, 6), (-2, 20)):
        delta = Vector(*tpl)
        assert not v2.can_move(delta, game_map)

    v3 = Villager(3, Position(80, 80))
    v3.move_by(Vector(10, 5))
    # print('Now, v3 is at position ', v3.position)
    v3.move_by(Vector(5, 10))
    assert v3.position.value == (95, 95)

    for tpl in ((4, 4), (4, -10), (2, 3), (4, 0), (0, 4)):
        delta = Vector(*tpl)
        assert v3.can_move(delta, game_map)

    for tpl in ((5, 4), (4, 5), (6, -1), (2, 7)):
        delta = Vector(*tpl)
        assert not v3.can_move(delta, game_map)

