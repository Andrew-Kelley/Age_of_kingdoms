from resources import Resources, Wood, Food, Stone, Gold, Bronze, Iron
from map_etc.make_map import game_map
from map_etc.iterate_around import everything_within_given_distance_on
from map_etc.iterate_around import within_given_distance
from buildings.resource_bldngs import Farm, LumberCamp, StoneQuarry, MiningCamp
from random import choice
from copy import copy

unit_kind_to_singular = {'villagers': 'villager',
                         'pikemen': 'pikeman',
                         'swordsmen': 'swordsman',
                         'archers': 'archer',
                         'knights': 'knight',
                         'batteringrams': 'batteringram',
                         'catapults': 'catapult',
                         'trebuchets': 'trebuchet',
                         'units': 'unit',
                         'merchants': 'merchant'}

unit_kinds_singular = ['villager', 'pikeman', 'swordsman',
                       'archer', 'knight', 'batteringram',
                       'catapult', 'trebuchet', 'merchant']


class Unit:
    """e.g. villager, swordsman, knight, catapult"""
    kind = 'units'
    # The following should never be accessed. It will always be
    # overridden by the subclasses.
    cost = Resources({Food: 1000, Wood: 1000, Gold: 1000})

    def __init__(self, position, player):
        """For each player, the first of each unit is numbered 1.
        Further units built (of the same type) are consecutively numbered.

        The position attribute is where on the map the unit starts."""
        number = len(player.units[self.kind])
        self.number = number
        self.position = position
        self.is_alive = True
        self.current_action = 'doing nothing'
        player.messages += 'New unit: {}\n'.format(self)
        player.units[self.kind].append(self)

    def __str__(self):
        kind_singular = unit_kind_to_singular[self.kind].capitalize()
        # The following three lines exist only to make the return statement shorter.
        num = self.number
        position = self.position
        current_action = self.current_action
        return '{} {} at position ' \
               '{} {}'.format(kind_singular, num, position, current_action)

    def can_move(self, delta, game_map):
        """Returns bool.

        Right now, every unit can move the same distance, but that may change.
        delta must be of type Vector"""
        if delta.magnitude > 15:
            # Then delta is too big
            return False
        # Next, check if the proposed movement moves the unit outside the map
        new_position = self.position + delta
        if not new_position.is_on_the_map(game_map):
            return False

        # TODO eventually: add a check to keep the unit from moving across enemy walls
        return True

    def move_by(self, delta):
        """delta must of of type Vector (or Position)"""
        self.position += delta

    def compare_to(self, other):
        there_is_an_error = False
        if self.number != other.number:
            print("Error: their numbers don't match:")
            print("Numbers: ", self.number, other.number)
            there_is_an_error = True

        delta = self.position - other.position
        error_margin = 5  # Somewhat arbitrary
        # Recall that when villagers collect resources, which resource
        # they go to next uses randomness. When military units attack,
        # I might also use randomness to which unit they choose to attack.
        if delta.magnitude > error_margin:
            print("Possible error: their positions are different:")
            print("positions: ", self.position, other.position)
            there_is_an_error = True
        if self.is_alive != other.is_alive:
            print("Error: one is dead and the other alive.")
            there_is_an_error = True
        if self.current_action != other.current_action:
            print("Error: their actions don't match.")
            print(self.current_action, other.current_action)
            there_is_an_error = True
        if there_is_an_error:
            print(self)
            print(other)
        return there_is_an_error


# Should I inherit from SelectedUnits?
# But being an army doesn't mean it is selected, so I don't think so.
class Army:
    """A collection of some units for military purposes."""
    # Needs to implement the method units (which is all units in this army)
    # and that method, called units, needs to be a property
    pass


# Should Group inherit from Army? Or should Group be more general than its
# docstring states and then have Army inherit from Group?
class Group:
    """A collection of villagers."""
    # Needs to implement the method units (which is all units in this army)
    # and that method, called units, needs to be a property
    pass


class Villager(Unit):
    cost = Resources({Food: 50})
    kind = 'villagers'

    def __init__(self, position, player):
        Unit.__init__(self, position, player)
        # The following gives how fast a villager can build a building.
        self.build_amount_per_turn = 10
        self.farm_currently_farming = None

        if 'bronze tipped plow' in player.things_researched:
            self.food_from_farming_per_turn = 12
        else:
            self.food_from_farming_per_turn = 10

    def resource_iter_within_given_distance_of_me(self, distance, resource, player):
        """Returns an iterator of instances of the given resource within
        the stated distance of self which
        are also within 15 spots of an appropriate building.

        resource must be in [Wood, Food, Stone, Bronze, Iron]."""
        if not type(distance) is int or distance < 0:
            return

        buildings_ls = copy(player.buildings['towncenter'][1:])
        resource_to_building = {Wood: LumberCamp, Stone: StoneQuarry, Gold: MiningCamp,
                                Bronze: MiningCamp, Iron: MiningCamp}
        if resource in resource_to_building:
            building = resource_to_building[resource]
            buildings_ls.extend(copy(player.buildings[building.kind][1:]))

        for obj in everything_within_given_distance_on(game_map, distance, self.position):
            if isinstance(obj, resource):
                for building in buildings_ls:
                    if within_given_distance(obj, building, distance=15):
                        yield obj
                        break

    def can_collect_resource_now(self, resource, player):
        """The word 'now' means this turn.

        The villager self must be within 6 spots of a resource instance
        that is also within 15 spots of an appropriate building.

        If the given resource is within 6 spots of the villager,
        then the villager is allowed to instantly move to a nearby
        resource instance and collect
        that resource this turn."""
        for _ in self.resource_iter_within_given_distance_of_me(6, resource, player):
            return True
        return False

    def collect_resource_here(self, resource, player):
        resource_instance = game_map(self.position)
        if not isinstance(resource_instance, resource):
            # This should never happen.
            print('ERROR! The function collect_resource_here was called '
                  'with the argument resource {},'.format(resource),
                  "but the object at the villager's "
                  "position was {}".format(resource_instance))
            return

        amount_to_collect = min(player.collecting_capacity[resource],
                                resource_instance.amount_left)
        resource_instance.amount_left -= amount_to_collect
        player.resources[resource] += amount_to_collect
        if resource_instance.amount_left <= 0:
            # Then delete resource_instance on the map
            x, y = self.position.value
            game_map.bldngs_n_rsrcs[y][x] = ' '

    def collect_resource(self, resource, player):
        ls = list(self.resource_iter_within_given_distance_of_me(0, resource, player))
        if len(ls) > 0:
            self.collect_resource_here(resource, player)
            return

        for distance in (1, 2, 4, 6):
            ls = list(self.resource_iter_within_given_distance_of_me(distance,
                                                                     resource, player))
            if len(ls) > 0:
                resource_instance = choice(ls)
                delta = resource_instance.position - self.position
                self.move_by(delta)
                self.collect_resource_here(resource, player)
                return

    def farm(self, the_farm, player):
        if not isinstance(the_farm, Farm):
            # This check should be completely unnecessary.
            player.messages += 'Error! {} '.format(self)
            player.messages += 'is trying to farm something that is not a farm.\n'
            return
        if the_farm != self.farm_currently_farming:
            player.messages += 'Error! {} '.format(self)
            player.messages += 'is trying to farm is different\n'
            player.messages += 'from the farm he is listed as currently farming.'
            return
        if self not in the_farm.current_farmers:
            # This should never happen.
            player.messages += 'Error! {} '.format(self)
            player.messages += 'was commanded to farm from a farm the he was\n'
            player.messages += 'not listed as a farmer.'
            return
        player.resources[Food] += self.food_from_farming_per_turn


# Unless pikemen are significantly weaker than Swordsman, I think that the cost
# difference between Pikeman and Swordsman will result in many more
# Pikeman being built at the beginning of the game.
# I think that this is OK.
# I intend Pikeman to only be somewhat weaker than Swordsman
class Pikeman(Unit):
    """A man with a spear and a shield"""
    cost = Resources({Food: 40, Wood: 20})
    kind = 'pikemen'


class Swordsman(Unit):
    # After reaching the Bronze Age, before being able to train Swordsman,
    # two things must first be researched at the Blacksmith:
    # (a) bronze shields, and (b) bronze swords.
    # The first of these also benefits Pikeman (by upgrading their
    # armor to bronze).
    cost = Resources({Food: 40, Gold: 25, Bronze: 15})
    kind = 'swordsmen'


class ChampionSwordsman(Swordsman):
    # Can only be built after researching level 3 swordsman
    pass


class Archer(Unit):
    cost = Resources({Wood: 40, Gold: 20, Bronze: 10})
    kind = 'archers'


class ChampionArcher(Archer):
    # Can only be built after researching level 3 archers
    pass


class Knight(Unit):
    kind = 'knights'


class ChampionKnight(Knight):
    # Can only be built after researching level 3 knight
    pass


class BatteringRam(Unit):
    kind = 'batteringrams'


class Catapult(Unit):
    kind = 'catapults'


class Trebuchet(Unit):
    kind = 'trebuchets'


class Merchant(Unit):
    kind = 'merchants'


unit_kinds = ['villagers', 'pikemen', 'swordsmen', 'archers', 'knights',
              'batteringrams', 'catapults', 'trebuchets', 'merchants']

# In case I change units or unit_kinds and forget to change the other:
assert len(unit_kinds_singular) == len(unit_kinds)

unit_classes = [Villager, Pikeman, Swordsman, Archer, Knight, BatteringRam,
                Catapult, Trebuchet, Merchant]

assert len(unit_kinds) == len(unit_classes)

unit_kind_to_class = dict((k, c) for k, c in zip(unit_kinds, unit_classes))

unit_singular_to_plural = dict((s, p) for s, p in zip(unit_kinds_singular, unit_kinds))

if __name__ == '__main__':
    from map_etc.position import Position, Vector
    from player import Player

    p1 = Player(1, Position(80, 80), is_human=True)

    v1 = Villager(Position(50, 50), p1)
    print(v1.number, v1.position)
    v1.move_by(Vector(5, 8))
    print(v1.number, v1.position)

    v2 = Villager(Position(5, 5), p1)
    for tpl in ((-5, -5), (7, 8), (-4, 11), (3, 6)):
        delta = Vector(*tpl)
        assert v2.can_move(delta, game_map)
    print(v2.position)

    for tpl in ((-6, -5), (-5, -6), (10, 6), (-2, 20)):
        delta = Vector(*tpl)
        assert not v2.can_move(delta, game_map)

    v3 = Villager(Position(80, 80), p1)
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

    # NOTE: The following four blocks of code may break if I change game_map
    v4 = Villager(Position(70, 85), p1)
    ls = list(v4.resource_iter_within_given_distance_of_me(0, Wood, p1))
    assert len(ls) == 1
    assert isinstance(ls[0], Wood)

    lumber_camp = LumberCamp(1, Position(67, 92), p1)
    lumber_camp.build_on_map(Position(67, 92), game_map)
    p1.buildings[LumberCamp.kind].append(lumber_camp)
    # print(game_map)
    v5 = Villager(Position(67, 90), p1)
    assert v5.can_collect_resource_now(Wood, p1)
    v5.collect_resource(Wood, p1)
    assert v5.position == Position(67, 89)

    v6 = Villager(Position(54, 77), p1)
    assert not v6.can_collect_resource_now(Wood, p1)
    v6.collect_resource(Wood, p1)
    assert v6.position == Position(54, 77)
    # assert v6.position == Position(60, 77)

    v7 = Villager(Position(66, 79), p1)
    v7.collect_resource(Wood, p1)
    assert v7.position in (Position(66, 80), Position(65, 79))

    print(p1.resources)
    position = Position(70, 80)
    v8 = Villager(position, p1)
    assert v8.can_collect_resource_now(Wood, p1)
    assert isinstance(game_map(position), Wood)
    for i in range(30):
        v8.collect_resource(Wood, p1)
    assert game_map(position) == ' '
    print(p1.resources)
