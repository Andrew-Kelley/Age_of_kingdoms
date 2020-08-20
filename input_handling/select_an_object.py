from units import Unit, Villager
from units import unit_kinds, unit_kinds_singular, unit_singular_to_plural
from buildings.bldng_class import Building, buildings

# For building names that really are two words, I would like to be able to
# handle a space between those words:
building_first_words = {'town', 'lumber', 'stone', 'mining', 'wood',
                        'archery', 'siege'}


class SelectedObject:
    def consists_of_villagers(self):
        if not isinstance(self, SelectedUnits):
            return False

        return all(isinstance(u, Villager) for u in self.units)


class SelectedUnits(SelectedObject):
    __units = []

    def add_unit(self, unit):
        if not isinstance(unit, Unit):
            return
        self.__units.append(unit)

    @property
    def units(self):
        for u in self.__units:
            yield u

    @property
    def num_units_selected(self):
        return len(self.__units)

    @property
    def non_empty(self):
        return self.num_units_selected > 0


class SelectedBuilding(SelectedObject):
    __building = None

    def __init__(self, building):
        if not isinstance(building, Building):
            return
        self.__building = building

    @property
    def building(self):
        return self.__building


def selected_obj_to_ls_of_units(player, selected_obj):
    """selected_obj must be of the type that the fn select_something returns"""
    if selected_obj is None or len(selected_obj) < 2:
        return []

    ls_of_units = []
    if selected_obj[0] == 'unit':
        # Then selected_obj == ['unit', unit.kind, starting_num, ending_num]
        # The following four lines of code should be unnecessary. I believe it
        # is redundant, assuming that the fn select_something works properly.
        if len(selected_obj) != 4 or selected_obj[1] not in unit_kinds:
            return []
        if not all(type(i) is int for i in selected_obj[2:]):
            return []

        unit_kind = selected_obj[1]
        n1 = selected_obj[2]
        n2 = selected_obj[3]
        for unit in player.units[unit_kind][n1:n2 + 1]:
            if unit.is_alive:
                ls_of_units.append(unit)
        return ls_of_units

    # TODO: implement the rest of this function (when the selected object is
    # an army or a group)
    # I first need to implement the Group and Army classes.
    if selected_obj[0] == 'group':
        return []

    if selected_obj[0] == 'army':
        return []

    return []


def selected_obj_to_actual_building(player, selected_obj):
    """In order to not return None, selected_obj must be in the following format:
    ['building', building.kind, building_num]"""
    if len(selected_obj) != 3:
        return
    if selected_obj[0] != 'building':
        return
    kind = selected_obj[1]
    if kind not in buildings:
        return

    building_num = selected_obj[2]
    if not 1 <= building_num < len(player.buildings[kind]):
        print('There is no {} with number {}'.format(kind, building_num))
        return

    return player.buildings[kind][building_num]


def selected_obj_consists_of_villagers(selected_obj):
    if not selected_obj:
        print('You must first select some villager(s) before giving a command to ',
              'collect a resource or build a building.')
        return False

    if not type(selected_obj) is list or len(selected_obj) < 2:
        print('Error: selected_obj is not proper')
        return False

    negative_message = 'Only villagers can collect resources and build buildings. '
    negative_message += 'Your selected object was not a group of villagers.'

    if not selected_obj[0] in ('unit', 'group'):
        print(negative_message)
        return False

    if selected_obj[0] == 'group':
        if not len(selected_obj) == 2:
            return False
        num = selected_obj[1]
        if not type(num) is int or num < 0:
            print('The group selected is not proper.')
            return False

    if selected_obj[0] == 'unit':
        if not selected_obj[1] == 'villagers':
            print(negative_message)
            return False
        if not len(selected_obj) == 4:
            print("Developer message: Error: selected_obj[0] == 'unit', but",
                  "len(selected_obj) is not 4.")
            return False
        num1, num2 = selected_obj[2:4]
        if not type(num1) is int or not type(num2) is int or \
                num1 > num2 or num1 < 1 or num2 < 1:
            print("The selected object's numbers were not proper.")
            return False

    return True


def formatted_input_to_SelectedUnits_obj(formatted_input, player):
    """Returns None or an instance of SelectedUnits

    formatted_input should be of the following form:
    ['unit', unit_kind, [(start1, stop1), (start2, stop2),...]]
    where startN <= stopN for N = 1, 2, 3, ...

    The intention of what units represented by formatted_input is all the
    units of type unit_kind of player with numbers any any of the ranges
    start1 to stop1 (inclusive), start2 to stop2, etc.
    """
    if not type(formatted_input) is list:
        return
    if len(formatted_input) != 3:
        return
    unit_kind = formatted_input[1]
    if unit_kind not in unit_kinds:
        return
    ranges = formatted_input[2]
    if not type(ranges) is list or len(ranges) == 0:
        return
    for rng in ranges:
        if len(rng) != 2 or rng[0] > rng[1]:
            return

    selected_units = SelectedUnits()

    for rng in ranges:
        start = rng[0]
        stop = rng[1]
        for unit in player.units[unit_kind][start:stop + 1]:
            if unit.is_alive:
                selected_units.add_unit(unit)
        return selected_units






def extract_selected_obj(inpt_as_ls, player):
    """The return format is the same as the fn select_something"""
    if len(inpt_as_ls) < 3:
        return []

    kind = inpt_as_ls[1]
    not_units = kind not in unit_kinds_singular and \
                kind not in unit_kinds and kind not in {'group', 'army'}
    not_building = kind not in buildings
    not_town = kind != 'town'
    if not_units and not_building and not_town:
        if kind in building_first_words:
            kind = inpt_as_ls[1] + inpt_as_ls[2]
            if kind in buildings:
                new_inpt_as_ls = [inpt_as_ls[0]]
                new_inpt_as_ls.append(kind)
                new_inpt_as_ls.extend(inpt_as_ls[3:])
                inpt_as_ls = new_inpt_as_ls
                if len(inpt_as_ls) == 2:
                    inpt_as_ls.append('1')
            else:
                print("The second word in your command could not be understood.")
                return []
        else:
            print("The second word in your command could not be understood.")
            return []

    if kind in unit_kinds:
        # inpt_as_ls[2] should be of the form 'num1-num2'
        num_range = inpt_as_ls[2].split('-')
        try:
            num_range = [int(i) for i in num_range]
        except ValueError:
            print('The third part of your command could not be understood.', end=' ')
            print("A number range (such as 1-4) was expected.")
            return []

        # In case num_range is a list of a single number...
        a = num_range[0]
        b = num_range[-1]
        if a < 1 or b < a:
            print('No units were selected. Try a different number range.')
            return []

        if not unit_exists(kind, a, player):
            return []

        selected_obj = ['unit', kind, a, b]
        return selected_obj
    else:
        # Now, inpt_as_ls[2] should be of the form 'num'
        try:
            num = int(inpt_as_ls[2])
        except ValueError:
            return []

    if num < 1:
        print('No unit selected since units are numbered beginning with 1.')
        return []

    if kind in unit_kinds_singular:
        kind = unit_singular_to_plural[kind]
        if not unit_exists(kind, num, player):
            return []
        selected_obj = ['unit', kind, num, num]
    elif kind in {'group', 'army'}:
        selected_obj = [kind, num]
    elif kind in buildings:
        selected_obj = ['building', kind, num]
    elif kind == 'town':
        selected_obj = ['town', num]
    else:
        # Due to the second conditional statement in this function, this code
        # should never be reached.
        selected_obj = []

    return selected_obj


def unit_exists(unit_kind, unit_number, player):
    if unit_kind not in player.units:
        return False

    if unit_number >= len(player.units[unit_kind]):
        print('There is no unit with that/those number(s).')
        return False

    if unit_number < 1:
        return False

    return True


def is_a_selected_obj(ls):
    """Returns True if ls is a non-empty list of the format of
    what select_something returns"""
    if type(ls) != list:
        return False
    if len(ls) < 2 or len(ls) > 4:
        return False
    if ls[0] not in ('unit', 'army', 'group', 'building', 'town'):
        return False

    if ls[0] == 'unit':
        if len(ls) != 4:
            return False
        if ls[1] not in unit_kinds:
            return False
        if not type(ls[2]) is int or not type(ls[3]) is int:
            return False
        if not 1 <= ls[2] <= ls[3]:
            return False
        return True

    if ls[0] in ('army', 'group',  'town'):
        if len(ls) != 2:
            return False
        return type(ls[1]) is int and 1 <= ls[1]

    if ls[0] == 'building':
        if len(ls) != 3:
            return False
        if ls[1] not in buildings:
            return False
        return type(ls[2]) is int and 1 <= ls[2]


def select_something(player, inpt_as_ls, selected_obj=None):
    """The point of this function is to return an output selected_obj
    returns [] or a list in one of the following formats:

    ['unit', unit.kind, starting_num, ending_num],  1 <= where starting_num <= ending_num
    or
    ['army', army_num], where 1 <= army_num
    or
    ['group', group_num], where 1 <= group_num
    or
    ['building', building.kind, building_num], where 1 <= building_num
    or
    ['town', town_num], where 1 <= town_num

    Note: The arguments player, selected_obj, and selected_town_num are not used.
    """
    if len(inpt_as_ls) > 2:
        # Then the player has specified the building or unit number(s)
        return extract_selected_obj(inpt_as_ls, player)
    elif len(inpt_as_ls) < 2:
        return []
    else:
        # Current Usage: In this case, there is an implied '1' as the building
        # or unit number. Alternate usage (not used): It would make sense that
        # ['select', 'barracks'] is selecting the only barracks in the town
        # with the given selected_town_num.
        inpt_as_ls.append('1')
        return extract_selected_obj(inpt_as_ls, player)


if __name__ == '__main__':
    from player import Player
    from game_map import Position
    from buildings.other_bldngs import TownCenter
    from units import Villager


    p1 = Player(1, Position(80, 80), is_human=True)
    towncenter = selected_obj_to_actual_building(p1, ['building', 'towncenter', 1])
    assert isinstance(towncenter, TownCenter)
    print(towncenter)

    selected_obj = select_something(p1, ['select', 'towncenter'])
    # print(selected_obj)
    towncenter = selected_obj_to_actual_building(p1, selected_obj)
    assert isinstance(towncenter, TownCenter)
    print(towncenter)

    selected_obj = select_something(p1, ['select', 'towncenter', 1])
    # print(selected_obj)
    towncenter = selected_obj_to_actual_building(p1, selected_obj)
    assert isinstance(towncenter, TownCenter)
    print(towncenter)

    for num in range(2, 5):
        selected_obj = select_something(p1, ['select', 'towncenter', num])
        # print(selected_obj)
        towncenter = selected_obj_to_actual_building(p1, selected_obj)
        assert towncenter is None
        # print(towncenter)


    s_obj = select_something(p1, ['select', 'villager'])
    assert selected_obj_consists_of_villagers(s_obj)
    villager_ls = selected_obj_to_ls_of_units(p1, s_obj)
    for v in villager_ls:
        print(v)
        assert isinstance(v, Villager)

    s_obj = select_something(p1, ['select', 'villager', '2'])
    assert selected_obj_consists_of_villagers(s_obj)
    villager_ls = selected_obj_to_ls_of_units(p1, s_obj)
    for v in villager_ls:
        print(v)
        assert isinstance(v, Villager)

    s_obj = select_something(p1, ['select', 'villager', '3'])
    assert selected_obj_consists_of_villagers(s_obj)
    villager_ls = selected_obj_to_ls_of_units(p1, s_obj)
    for v in villager_ls:
        print(v)
        assert isinstance(v, Villager)


    assert not select_something(p1, ['select', 'building'])
    assert not select_something(p1, ['select', 'blah'])
    assert not select_something(p1, ['select', 'villagar'])

    # the following two lines don't print anything
    assert not select_something(p1, ['select', 'towncenter', 'n'])
    assert not select_something(p1, ['select'])

    assert not select_something(p1, ['select', 'villager', '4'])
    assert not select_something(p1, ['select', 'villagers', '10-20'])
    assert not select_something(p1, ['select', 'pikeman', '40'])

    # the following line doesn't print anything
    assert selected_obj_to_actual_building(p1, ['building', 'blah', 1]) is None

    assert selected_obj_to_actual_building(p1, ['building', 'barracks', 1]) is None

    # The above code prints the following:
    # Towncenter 1 at position (80, 80)
    # Towncenter 1 at position (80, 80)
    # Towncenter 1 at position (80, 80)
    # There is no towncenter with number 2
    # There is no towncenter with number 3
    # There is no towncenter with number 4
    # Villager 1 at position (78, 78) doing nothing
    # Villager 2 at position (82, 78) doing nothing
    # Villager 3 at position (82, 82) doing nothing
    # The second word in your command could not be understood.
    # The second word in your command could not be understood.
    # The second word in your command could not be understood.
    # There is no unit with that/those number(s).
    # There is no unit with that/those number(s).
    # There is no unit with that/those number(s).
    # There is no barracks with number 1
