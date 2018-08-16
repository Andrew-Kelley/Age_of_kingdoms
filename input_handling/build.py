from units import unit_kinds_singular, unit_kinds, unit_singular_to_plural
from input_handling.select_an_object import selected_obj_to_actual_building

unit_kinds_singular = set(unit_kinds_singular)
unit_kinds = set(unit_kinds)
units_plural = unit_kinds


# For building names that really are two words, I would like to be able to handle a space between those
# words, but as of now, the code doesn't use the following set:
building_first_words = {'town', 'lumber', 'stone', 'mining', 'wood', 'archery', 'siege'}

def build_something(player, inpt_as_ls, selected_obj=None, selected_town_num=1):
    """In order to not return [], selected_obj must either be
    (a) a villager, or villagers, or group of villagers OR
    (b) a building (which builds units)"""
    # selected_town_num will be used when building walls.
    if len(inpt_as_ls) < 2:
        return []
    if not selected_obj or not type(selected_obj) is list:
        print('Command rejected:')
        print('You must first select an object before building something.')
        print('For building a building, you must first select which villagers to build it.')
        print('To build units, you must first select which building to build them from.')
        return []
    if len(selected_obj) < 2:
        return []

    if selected_obj[0] == 'building':
        return build_unit(player, inpt_as_ls, selected_obj, selected_town_num)

    elif selected_obj[0] == 'unit':
        if selected_obj[1] == 'villagers':
            return build_building(player, inpt_as_ls, selected_obj, selected_town_num)
        else:
            print('In order to build a building, the selected object needs to be some villager(s)',
                  "--possibly a 'group' of villagers.")
            return []
    elif selected_obj[0] == 'group':
        return build_building(player, inpt_as_ls, selected_obj, selected_town_num)
    else:
        return []


# The following is intended to only be used by the function build_something
def build_unit(player, inpt_as_ls, selected_obj, selected_town_num=1):
    """Returns a list.

    In order to not return [],
    (a) The building which builds the unit(s) must be selected as selected_obj, and
    (b) inpt_as_ls must be of the following type:
    ['build', <unit type>], (which builds 1 of the given unit type) or
    ['build', 'num', <unit type>]

    If not returning [], this function returns a list of the following format:
    ['build unit', <building>, <unit type>, num_to_be_built], where
    num_to_be_built >= 1"""
    if not selected_obj or not type(selected_obj) is list:
        return []
    if len(selected_obj) < 2:
        return []

    building = selected_obj_to_actual_building(player, selected_obj)
    if not building:
        return []

    unit_type = inpt_as_ls[-1]
    if unit_type not in unit_kinds and unit_type not in unit_kinds_singular:
        print('The last part of your command (which type of unit to be built) was not understood.')
        return []
    if unit_type in unit_kinds_singular:
        unit_type = unit_singular_to_plural[unit_type]

    if len(inpt_as_ls) == 3:
        try:
            num_to_be_built = int(inpt_as_ls[1])
            if num_to_be_built < 1:
                print('Your command must specify a positive number of units to be built.')
                return []
        except ValueError:
            print('The second part of your command (how many units to be built) was not understood.')
            return []
    else:
        num_to_be_built = 1

    return ['build unit', building, unit_type, num_to_be_built]


# The following is intended to only be used by the function build_something
def build_building(player, inpt_as_ls, selected_obj=None, selected_town_num=1):
    return ['build building']


def set_default_build_position(player, inpt_as_ls, selected_obj=None, selected_town_num=1):
    """selected_obj (if not None) must be in the following format:
    ['building', building.kind, building_num]"""
    # I need to decide on the format of the output
    return ['set build position']
