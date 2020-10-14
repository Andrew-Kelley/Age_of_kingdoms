from units import unit_kinds_singular, unit_kinds, unit_singular_to_plural
from units import Group, Army
from game_map import Position, game_map
from resources import resource_kind_to_class
from input_handling.select_an_object import SelectedObject, SelectedBuilding
from input_handling.select_an_object import SelectedUnits
from input_handling.select_an_object import building_first_words
from input_handling.print import str_to_int
from buildings.bldng_class import stone_age_buildings, bronze_age_buildings, buildings
from buildings.other_bldngs import building_kind_to_class
from command_handling.commands import BuildUnitCmd, BuildBuildingCmd

unit_kinds_singular = set(unit_kinds_singular)
unit_kinds = set(unit_kinds)
units_plural = unit_kinds


def build_something(player, inpt_as_ls, selected_obj=None):
    """In order to not return None, selected_obj must either be
    (a) a villager, or villagers, or group of villagers OR
    (b) a building (which builds units)"""
    if len(inpt_as_ls) < 2:
        return
    if not isinstance(selected_obj, SelectedObject):
        print('Command rejected:')
        print('You must first select an object before building something.')
        print('For building a building, you must first select which villagers '
              'to build it.')
        print('To build units, you must first select which building to build '
              'them from.')
        return


    if isinstance(selected_obj, SelectedBuilding):
        return build_unit(inpt_as_ls, selected_obj)

    elif isinstance(selected_obj, SelectedUnits):
        if not selected_obj.consists_of_villagers:
            return
        else:
            return build_building(player, inpt_as_ls, selected_obj)
    elif isinstance(selected_obj, Army) or isinstance(selected_obj, Group):
        #Todo: implement this
        pass
    else:
        print('The selected object was neither a building nor a group of villagers.',
              'Command rejected.')
        return


# The following is intended to only be used by the function build_something
def build_unit(inpt_as_ls, selected_obj):
    """Returns None or an instance of BuildUnitCmd.

    In order to not return None,
    (a) The building which builds the unit(s) must be selected as selected_obj, and
    (b) inpt_as_ls must be of the following type:
    ['build', <unit type>], (which builds 1 of the given unit type) or
    ['build', 'num', <unit type>]"""
    if not isinstance(selected_obj, SelectedBuilding):
        return

    building = selected_obj.building
    if not building:
        return

    unit_type = inpt_as_ls[-1]
    if unit_type not in unit_kinds and unit_type not in unit_kinds_singular:
        print('The last part of your command (which type of unit to be built) '
              'was not understood.')
        return
    if unit_type in unit_kinds_singular:
        unit_type = unit_singular_to_plural[unit_type]

    if len(inpt_as_ls) == 3:
        try:
            num_to_be_built = int(inpt_as_ls[1])
            if num_to_be_built < 1:
                print('Your command must specify a positive number of units '
                      'to be built.')
                return
        except ValueError:
            print('The second part of your command (how many units to be built) '
                  'was not understood.')
            return
    else:
        num_to_be_built = 1

    return BuildUnitCmd(building, unit_type, num_to_be_built)


# The following is intended to only be used by the function build_something
def build_building(player, inpt_as_ls, selected_obj):
    """In order to not return None,  inpt_as_ls must be of the following format:
     ['build', <building name>, 'num1', 'num2']. Also, the player must first
     have advanced to the appropriate age for the building they wish to build.

     Returns [] or the following:
     ['build building', ls_of_villagers, building_class, position]"""
    if len(inpt_as_ls) < 4:
        print('Your command to build a building was not understood since it had '
              'fewer than 4 parts/words.')
        return

    if inpt_as_ls[0] == 'help build':
        this_is_a_help_build_command = True
    else:
        this_is_a_help_build_command = False

    if not selected_obj.consists_of_villagers:
        print('No villagers were selected that could build the building.')
        return

    if selected_obj.is_empty:
        print('No villagers were selected that could build the building.')
        return

    villagers = selected_obj.units

    building_kind = inpt_as_ls[1]
    if building_kind not in buildings:
        if building_kind in building_first_words:
            if inpt_as_ls[1] + inpt_as_ls[2] in buildings:
                building_kind = inpt_as_ls[1] + inpt_as_ls[2]
            else:
                print('The building kind you want to build was not understood.')
                return
        else:
            print('The building kind you want to build was not understood.')
            return

    if player.age == 'stone age':
        if building_kind not in stone_age_buildings:
            print('That building cannot be built in the Stone Age.')
            return
    elif player.age == 'bronze age':
        if building_kind not in stone_age_buildings.union(bronze_age_buildings):
            print('That building can only be built in the Iron Age.')
            return

    if building_kind == 'wallfortification':
        return build_wall_fortification(player, inpt_as_ls, this_is_a_help_build_command)

    if building_kind in ('woodwall', 'stonewall'):
        return build_wall(player, inpt_as_ls, this_is_a_help_build_command)

    if building_kind not in building_kind_to_class:
        # This should never happen because I already checked that
        # building_kind is in buildings
        print('The building you want to build was not understood.')
        return

    building_class = building_kind_to_class[building_kind]

    i = str_to_int(inpt_as_ls[-2])
    j = str_to_int(inpt_as_ls[-1])
    if i is None or j is None:
        return
    position = Position(i, j)

    if not this_is_a_help_build_command:
        if not building_class.can_build_on_map(building_class, position, game_map):
            print('Command rejected. Try a different position.')
            return

    return BuildBuildingCmd(villagers, building_class, position,
                            this_is_a_help_build_command)


def build_wall(player, inpt_as_ls, this_is_a_help_build_command):
    """Returns a list"""
    print('Sorry this game is not yet finished. You cannot yet build walls.')
    return


def build_wall_fortification(player, inpt_as_ls, this_is_a_help_build_command):
    """Returns a list"""
    print('You must first build a wall before building a wallfortification.',
          'But unfortunatelly, this game is not finished, and you cannot '
          'build walls either.')
    return


def set_default_build_position(player, inpt_as_ls, selected_obj=None,
                               loading_game=False, resource='none'):
    """selected_obj must be a building that can build units
    Returns None"""
    if not selected_obj or not isinstance(selected_obj, SelectedBuilding):
        return
    building = selected_obj.building
    if not building:
        return

    i = str_to_int(inpt_as_ls[-2])
    j = str_to_int(inpt_as_ls[-1])
    if i is None or j is None:
        return

    position = Position(i, j)
    building.change_build_position_to(position, game_map)

    if building.kind == 'towncenter':
        if loading_game:
            if resource in resource_kind_to_class:
                building.initial_resource_to_collect = resource_kind_to_class[resource]
                player.log_command("Resource=" + resource)
            return
        # The following of course runs if not loading_game
        while True:
            resource = input('Which resource would you like newly built '
                             'villagers to collect?'
                             '\nIf none, type "none" or just hit enter. ').lower().strip()
            if resource in ('', 'none'):
                building.initial_resource_to_collect = None
                player.log_command("Resource=none")
                break
            elif resource in resource_kind_to_class:
                player.log_command("Resource=" + resource)
                building.initial_resource_to_collect = resource_kind_to_class[resource]
                break
            else:
                print('Your command was not understood. Please try again.')
