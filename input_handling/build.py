from units import unit_kinds_singular, unit_kinds, unit_singular_to_plural
from game_map import Position, game_map
from input_handling.select_an_object import selected_obj_to_actual_building
from input_handling.select_an_object import selected_obj_consists_of_villagers
from input_handling.select_an_object import selected_obj_to_ls_of_units
from input_handling.print import str_to_int
from buildings.bldng_class import stone_age_buildings, bronze_age_buildings, buildings
from buildings.other_bldngs import building_kind_to_class

unit_kinds_singular = set(unit_kinds_singular)
unit_kinds = set(unit_kinds)
units_plural = unit_kinds


# For building names that really are two words, I would like to be able to handle a space between those
# words:
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

    elif selected_obj[0] in ('unit', 'group'):
        if not selected_obj_consists_of_villagers(selected_obj):
            return []
        else:
            return build_building(player, inpt_as_ls, selected_obj, selected_town_num)
    else:
        print('The selected object was neither a building nor a group of villagers.',
              'Command rejected.')
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
def build_building(player, inpt_as_ls, selected_obj, selected_town_num=1):
    """In order to not return [],  inpt_as_ls must be of the following format:
     ['build', <building name>, 'num1', 'num2']. Also, the player must first have advanced
     to the appropriate age for the building they wish to build.

     Returns [] or the following:
     ['build building', ls_of_villagers, building_class, position]"""
    if len(inpt_as_ls) != 4:
        print('Your command to build a building was not understood since it did not have 4',
              'parts/words.')
        return []

    ls_of_villagers = selected_obj_to_ls_of_units(player, selected_obj)
    if len(ls_of_villagers) < 1:
        print('No villagers were selected that could build the building.')
        return []

    building_kind = inpt_as_ls[1]
    if building_kind not in buildings:
        if building_kind in building_first_words:
            if inpt_as_ls[1] + inpt_as_ls[2] in buildings:
                building_kind = inpt_as_ls[1] + inpt_as_ls[2]
            else:
                print('The building kind you want to build was not understood.')
                return []
        else:
            print('The building kind you want to build was not understood.')
            return []

    if player.age == 'Stone Age':
        if building_kind not in stone_age_buildings:
            print('That building cannot be built in the Stone Age.')
            return []
    elif player.age == 'Bronze Age':
        if building_kind not in stone_age_buildings.union(bronze_age_buildings):
            print('That building can only be built in the Iron Age.')
            return []

    if building_kind == 'wallfortification':
        return build_wall_fortification(player, inpt_as_ls)

    if building_kind in ('woodwall', 'stonewall'):
        return build_wall(player, inpt_as_ls)

    if building_kind not in building_kind_to_class:
        # This should never happen because I already checked that building_kind is in buildings
        print('The building you want to build was not understood.')
        return []

    building_class = building_kind_to_class[building_kind]

    i = str_to_int(inpt_as_ls[2])
    j = str_to_int(inpt_as_ls[3])
    if i is None or j is None:
        return []

    position = Position(i, j)
    if not building_class.can_build_on_map(position, game_map):
        print('Command rejected. Try a different position.')
        return []

    return ['build building', ls_of_villagers, building_class, position]


def build_wall(player, inpt_as_ls):
    """Returns a list"""
    print('Sorry this game is not yet finished. You cannot yet build walls.')
    return []


def build_wall_fortification(player, inpt_as_ls):
    """Returns a list"""
    print('You must first build a wall before building a wallfortification.',
          'But unfortunatelly, this game is not finished, and you cannot build walls either.')
    return []


def set_default_build_position(player, inpt_as_ls, selected_obj=None, selected_town_num=1):
    """selected_obj (if not None) must be in the following format:
    ['building', building.kind, building_num]"""
    # I need to decide on the format of the output
    return ['set build position']
