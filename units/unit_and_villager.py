from resources import Wood, Food, Stone, Gold, Bronze, Iron
from map_etc.make_map import game_map
from map_etc.iterate_around import everything_within_given_distance_on
from map_etc.iterate_around import within_given_distance
from map_etc.initialize_position import set_unit_position_and_movement

from buildings.resource_bldngs import Farm, LumberCamp, StoneQuarry, MiningCamp

from units.unit_kinds import unit_kind_to_singular
from units.aggression_level import FLEE

from random import choice
from copy import copy


class Unit:
    """e.g. villager, swordsman, knight, catapult"""
    kind = 'units'
    letter_abbreviation = 'u'  # should always be overridden

    def __init__(self, building, player, position=None):
        """For each player, the first of each unit is numbered 1.
        Further units built (of the same type) are consecutively numbered.

        The position attribute is where on the map the unit starts."""
        number = len(player.units[self.kind])
        # self.number might be changeable by a command to be implemented later
        self.number = number
        # self._build_number is never to be changed and is used for testing
        # equality of instances via the method __hash__.
        self._build_number = number
        self.player_number = player.number
        self.is_alive = True
        self.current_action = 'doing nothing'
        if position is not None:
            # This is used for units that a player begins the game with
            self.position = position
        else:
            set_unit_position_and_movement(building, self, player)
        player.messages += 'New unit: {}\n'.format(self)
        player.units[self.kind].append(self)
        self.place_on_map(self.position)

    def __hash__(self):
        return hash((self.kind, self._build_number, self.player_number))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

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

        # The following check is not needed because the insert_move_command function
        # already checks that delta is not too big. Also, I want to be able
        # to use this method in the implement_move_commands function, and I
        # want to intentionally not check for the size of delta.
        # if delta.magnitude > 15:
        #     # Then delta is too big
        #     return False
        # Next, check if the proposed movement moves the unit outside the map
        new_position = self.position + delta
        if not new_position.is_on_the_map(game_map):
            return False

        if game_map.has_building_at(new_position) and not isinstance(self, Villager):
            return False

        if game_map.has_unit_at(new_position):
            player_num = game_map.get_player_num_for_unit_at(new_position)
            if self.player_number != player_num:
                return False
            if isinstance(self, Villager) and game_map.has_villager_at(new_position):
                return True
            return False
        return True

    def move_by(self, delta, game_map):
        """delta must of of type Vector (or Position)"""
        self.remove_from_map()

        new_position = self.position + delta
        self.place_on_map(new_position)

        self.position = new_position

    def place_on_map(self, new_position):
        def print_error_moving_to_message():
            print("Error!! A unit is trying to move to ", self.position)
            print("This is there already: ", at_this_location)
            print("Unit trying to move: ", self)

        x, y = new_position.value
        at_this_location = game_map(new_position, units=True)
        if isinstance(self, Villager):
            if isinstance(at_this_location, set):
                at_this_location.add(self)
            elif at_this_location is None:
                game_map.units[y][x] = {self}
            else:
                print_error_moving_to_message()
                return
        else:
            if at_this_location is None:
                game_map.units[y][x] = self
            else:
                print_error_moving_to_message()
                return

    def remove_from_map(self):
        """This happens any time a unit is moved."""
        def print_error_moving_from_message():
            print("Error! A unit is trying to move from ", self.position)
            print("But the unit wasn't really in game_map.units there.")
            print("This is what was where it 'was' instead: ", at_this_location)
            print("Unit trying to move: ", self)

        at_this_location = game_map(self.position, units=True)
        if isinstance(at_this_location, Unit):
            if at_this_location == self:
                x, y = self.position.value
                game_map.units[y][x] = None
            else:
                print_error_moving_from_message()
        elif isinstance(at_this_location, set):
            if self in at_this_location:
                at_this_location.remove(self)
                if len(at_this_location) == 0:
                    x, y = self.position.value
                    game_map.units[y][x] = None
            else:
                print_error_moving_from_message()

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


class Villager(Unit):
    kind = 'villagers'
    letter_abbreviation = 'v'

    def __init__(self, building, player, position=None):
        Unit.__init__(self, building, player, position)
        self.aggression_lvl = FLEE
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
                self.move_by(delta, game_map)
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


if __name__ == '__main__':
    from map_etc.position import Position, Vector
    from player import Player

    p1 = Player(1, Position(80, 80), is_human=True)
    towncenter = p1.buildings['towncenter'][1]

    print("WARNING!!!! These tests will currently fail and so are commented out.")
    print("New units are now created with one argument being the building")
    print("that builds them.")
    v1 = Villager(towncenter, p1, Position(50, 50))
    print(v1.number, v1.position)
    v1.move_by(Vector(5, 8), game_map)
    print(v1.number, v1.position)

    v2 = Villager(towncenter, p1, Position(5, 5))
    for tpl in ((-5, -5), (7, 8), (-4, 11), (3, 6)):
        delta = Vector(*tpl)
        assert v2.can_move(delta, game_map)
    print(v2.position)

    for tpl in ((-6, -5), (-5, -6)):
        delta = Vector(*tpl)
        assert not v2.can_move(delta, game_map)

    v3 = Villager(towncenter, p1)
    v3.move_by(Vector(10, 5), game_map)
    # print('Now, v3 is at position ', v3.position)
    v3.move_by(Vector(5, 10), game_map)
    assert v3.position.value == (95, 95)

    for tpl in ((4, 4), (4, -10), (2, 3), (4, 0), (0, 4)):
        delta = Vector(*tpl)
        assert v3.can_move(delta, game_map)

    for tpl in ((5, 4), (4, 5), (6, -1), (2, 7)):
        delta = Vector(*tpl)
        assert not v3.can_move(delta, game_map)

    # NOTE: The following four blocks of code may break if I change game_map
    v4 = Villager(towncenter, p1)
    ls = list(v4.resource_iter_within_given_distance_of_me(0, Wood, p1))
    # The following two assertions are broken:
    # assert len(ls) == 1
    # assert isinstance(ls[0], Wood)

    lumber_camp = LumberCamp(1, Position(67, 92), p1)
    lumber_camp.build_on_map(Position(67, 92), game_map)
    p1.buildings[LumberCamp.kind].append(lumber_camp)
    # print(game_map)
    v5 = Villager(towncenter, p1, Position(67, 89))
    # The following is broken:
    # assert v5.can_collect_resource_now(Wood, p1)
    # v5.collect_resource(Wood, p1)
    assert v5.position == Position(67, 89)

    v6 = Villager(towncenter, p1)
    assert not v6.can_collect_resource_now(Wood, p1)
    v6.collect_resource(Wood, p1)
    # The following is broken:
    # assert v6.position == Position(54, 77)
    # assert v6.position == Position(60, 77)

    v7 = Villager(towncenter, p1)
    v7.collect_resource(Wood, p1)
    # The following is broken:
    # assert v7.position in (Position(66, 80), Position(65, 79))

    print(p1.resources)
    position = Position(70, 80)
    v8 = Villager(towncenter, p1)
    # The following is broken:
    # assert v8.can_collect_resource_now(Wood, p1)
    # assert isinstance(game_map(position), Wood)
    # for i in range(30):
    #     v8.collect_resource(Wood, p1)
    # assert game_map(position) == ' '
    print(p1.resources)
