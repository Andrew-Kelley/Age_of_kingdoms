from units import unit_kinds, unit_kinds_singular, unit_singular_to_plural
from buildings.bldng_class import buildings


def selected_obj_to_ls_of_units(player, selected_obj):
    """selected_obj must be of the type that the fn select_something returns"""
    if selected_obj is None or len(selected_obj) < 2:
        return []

    ls_of_units = []
    if selected_obj[0] == 'unit':
        # Then selected_obj == ['unit', unit.kind, starting_num, ending_num]
        # The following four lines of code should be unnecessary. I believe it is redundant, assuming
        # that the fn select_something works properly.
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

    # TODO: implement the rest of this function (when the selected object is an army or a group)
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
        if not type(num1) is int or not type(num2) is int or num1 > num2 or num1 < 1 or num2 < 1:
            print("The selected object's numbers were not proper.")
            return False

    return True


def extract_selected_obj(inpt_as_ls):
    """The return format is the same as the fn select_something"""
    if len(inpt_as_ls) < 3:
        return []

    kind = inpt_as_ls[1]
    not_units = kind not in unit_kinds_singular and kind not in unit_kinds and kind not in {'group', 'army'}
    not_building = kind not in buildings
    not_town = kind != 'town'
    if not_units and not_building and not_town:
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
        return []

    if kind in unit_kinds_singular:
        kind = unit_singular_to_plural[kind]
        selected_obj = ['unit', kind, num, num]
    elif kind in {'group', 'army'}:
        selected_obj = [kind, num]
    elif kind in buildings:
        selected_obj = ['building', kind, num]
    elif kind == 'town':
        selected_obj = ['town', num]
    else:
        # Due to the second conditional statement in this function, this code should never be reached.
        selected_obj = []

    return selected_obj


def is_a_selected_obj(ls):
    """Returns True if ls is a non-empty list of the format of what select_something returns"""
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


def select_something(player, inpt_as_ls, selected_obj=None, selected_town_num=1):
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
        return extract_selected_obj(inpt_as_ls)
    elif len(inpt_as_ls) < 2:
        return []
    else:
        # Current Usage: In this case, there is an implied '1' as the building or unit number.
        # Alternate usage (not used): It would make sense that ['select', 'barracks'] is
        # selecting the only barracks in the town with the given selected_town_num.
        inpt_as_ls.append('1')
        return extract_selected_obj(inpt_as_ls)


if __name__ == '__main__':
    from player import Player
    from game_map import Position

    p1 = Player(1, Position(80, 80), is_human=True)
    print(selected_obj_to_actual_building(p1, ['building', 'towncenter', 1]))
    assert selected_obj_to_actual_building(p1, ['building', 'blah', 1]) == None
    assert selected_obj_to_actual_building(p1, ['building', 'barracks', 1]) == None