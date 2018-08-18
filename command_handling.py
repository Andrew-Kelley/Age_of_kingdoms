# This module handles the commands which are returned by the function input_next_command

from game_map import Position, Vector, game_map
from buildings.bldng_class import Building
from buildings.other_bldngs import TownCenter
from units import unit_kinds, unit_kind_to_class, unit_kind_to_singular, Villager
from resources import resource_ls

# player.commands['now'] is in the following format:
# {'move':dict( unit:position_delta for units to be moved ), # position_delta is a Vector
#  'build building':dict( villager:[building_to_be_built, position] for ...),
#  'collect resource':( villager:resource_object_to_collect for ...),
#  'build unit':dict( building:[unit_to_be_built, number_of_units_of_that_type_to_build] for ... ),
#  'research':dict( building:thing_to_be_researched for ...),
#  ...}
# Eventually, player.commands should also contain keywords such as follows:
# 'attack', 'defend'

# Note 1: I need to have a function which checks if a given unit has already been commanded to
# do something. I think newer commands will override older ones.

# Note 2: For each type of command given here, will this module contain three functions?
# The three functions are insert, update, and implement.


def insert_command(player, command):
    if not type(command) is list or len(command) == 0:
        return

    # MAYBE call all of the functions with one call (and a dictionary of functions).
    if command[0] == 'move':
        insert_move_command(player, command)
        return
    elif command[0] == 'build unit':
        insert_build_unit_command(player, command)
        return
    elif command[0] == 'collect resource':
        insert_collect_resource_command(player, command)
        return
    elif command[0] == 'build building':
        insert_build_building_command(player, command)
        return


def remove_unit_from_command_if_there(player, unit, command_type):
    """If unit is in player.commands['now'][command_type], then this function removes the unit from
    that command. If unit is not in player.commands['now'][command_type], this function does nothing.

    command_type should be one of the following:
    'move', 'build building', 'collect resource'"""
    if command_type not in ('move', 'build building', 'collect resource'):
        return
    if unit in player.commands['now'][command_type]:
        del player.commands['now'][command_type][unit]


def insert_build_building_command(player, command):
    """command must be of the following format:
    ['build building', ls_of_villagers, building_class, position]"""
    if len(command) != 4:
        return

    building_class = command[2]
    if not player.can_build(building_class):
        print('You do not have enough resources to build that building.')
        return

    ls_of_villagers = command[1]
    if not type(ls_of_villagers) is list or len(ls_of_villagers) == 0:
        return

    building_position = command[3]
    if not isinstance(building_position, Position):
        return

    for villager in ls_of_villagers:
        for command_type in ('move', 'collect resource'):
            remove_unit_from_command_if_there(player, villager, command_type)

    # The following few lines are to handle the situation that other villagers are already
    # building an instance of building_class at building_position
    building = building_already_in_progress(player, building_class, building_position)
    if building:
        pass
    else:
        building_number = len(player.buildings[building_class.kind])
        building = building_class(building_number, building_position)
        player.resources -= building.cost

    for villager in ls_of_villagers:
        delta = building_position - villager.position
        if delta.magnitude <= 6:
            player.commands['now']['build building'][villager] = [building, building_position]
        else:
            new_command = ['move', [villager], delta]
            insert_move_command(player, new_command)
            player.commands['later']['build building'][villager] = [building, building_position]


def building_already_in_progress(player, building_class, position):
    """Returns the building instance if the player is already building an instance of
    building_class at position. Otherwise, this returns False."""
    for time in ('now', 'later'):
        for villager in player.commands[time]['build building']:
            ls = player.commands['now']['build building'][villager]
            if ls[1] == position and ls[0].letter_abbreviation == building_class.letter_abbreviation:
                return ls[0]
    return False


def insert_collect_resource_command(player, command):
    if len(command) != 3:
        return
    resource = command[1]
    if not resource in resource_ls:
        return
    ls_of_villagers = command[2]
    if not type(ls_of_villagers) is list or len(ls_of_villagers)  == 0:
        return
    if not all((lambda u:isinstance(u, Villager) for u in ls_of_villagers)):
        return

    for unit in ls_of_villagers:
        for command_type in ('move', 'build building'):
            remove_unit_from_command_if_there(player, unit, command_type)

    for villager in ls_of_villagers:
        if villager.can_collect_resource_now(resource, player):
            player.commands['now']['collect resource'][villager] = resource
        else:
            print('Player {}:'.format(player.number),
                  villager, ' cannot collect {} now.'.format(resource.kind))


# The following function could instead be named insert_a_command_of_type_move
def insert_move_command(player, command):
    """In order for command to be handled properly, it must be in the following format:
    ['move', ls_of_units, delta], where delta is of type Vector"""
    if len(command) != 3:
        return
    ls_of_units = command[1]
    if not type(ls_of_units) is list:
        return
    delta = command[2]
    if not isinstance(delta, Vector):
        return

    for unit in ls_of_units:
        for command_type in ('build building', 'collect resource'):
            remove_unit_from_command_if_there(player, unit, command_type)

    if delta.magnitude > 15:
        beginning, the_rest = delta.beginning_plus_the_rest()
        move_now = dict((unit, beginning) for unit in ls_of_units)
        move_later = dict((unit, the_rest) for unit in ls_of_units)
    else:
        move_now = dict((unit, delta) for unit in ls_of_units)
        move_later = dict()

    # NOTE: THE FOLLOWING TWO LINES DO NOT WORK! The reason is that the player might make multiple
    # move commands during a turn (each of which might move different units). What the following two
    # lines would do would be to erase all previous move commands and replace them with the most
    # current one.
    # player.commands['now']['move'] = move_now
    # player.commands['later']['move'] = move_later

    # The following only replaces old move commands with new ones if they are about the same unit.
    for unit in move_now:
        player.commands['now']['move'][unit] = move_now[unit]
        if unit in player.commands['later']['move']:
            del player.commands['later']['move'][unit]
    for unit in move_later:
        player.commands['later']['move'][unit] = move_later[unit]
    return


def insert_build_unit_command(player, command):
    """Modifies player.commands['now']['build unit'] and player.commands['later']['build unit']

    The argument command must be of the following format (which is what the function build_unit
    in the input_handling module returns):
    ['build unit', <building>, <unit type>, num_to_be_built]"""
    if len(command) != 4:
        # This should never be the case.
        print('Python Error! The function insert_build_unit_command was given an argument command',
              'that is not of length 4.')
        return

    building = command[1]
    unit_type = command[2]
    num_to_be_built = command[3]
    if not isinstance(building, Building):
        return
    if not unit_type in unit_kinds:
        return
    if num_to_be_built < 1 or not type(num_to_be_built) is int:
        return

    if not unit_type in building.units_which_can_be_built(player):
        print('The selected building cannot build that unit.')
        print(cannot_build_unit_yet_error_message(player, building, unit_type))
        return

    num_can_build = number_of_units_can_build_in_one_turn(player, building, unit_type)

    num_to_build_now = min(num_can_build, num_to_be_built)
    num_to_build_later = num_to_be_built - num_to_build_now
    player.commands['now']['build unit'][building] = [unit_type, num_to_build_now]
    if num_to_build_later > 0:
        player.commands['later']['build unit'][building] = [unit_type, num_to_build_later]
    return


def number_of_units_can_build_in_one_turn(player, building, unit_type):
    if isinstance(building, TownCenter):
        if unit_type == 'villagers':
            num_can_build = building.num_villagers_can_build_in_turn(player)
        else:
            num_can_build = 0
    else:
        # I may later want to change this and allow some units besides villagers to be built more
        # than 1 per turn per building.
        num_can_build = 1
    return num_can_build


def cannot_build_unit_yet_error_message(player, building, unit_type):
    if unit_type == 'swordsmen':
        message =  "A barracks can build a swordsmen only after the Bronze Age is researched "
        message += "and after the following two things are researched at the Blacksmith:"
        message += "\n (a) bronze shields, and (b) bronze swords"
    elif unit_type == 'trebuchets':
        message = "A SiegeWorks can build a trebuchet only after the Iron Age is researched."
    else:
        message = ''
    return message

###################################################################################################
###################################################################################################
###################################################################################################
# The following is called at the beginning of each player's turn.
def update_now_and_later_commands(player):
    update_build_building_command(player)
    update_collect_resource_command(player)
    update_move_commands(player)
    update_build_unit_commands(player)


def update_build_building_command(player):
    for villager in list(player.commands['later']['build building']):
        building, building_position = player.commands['later']['build building'][villager]
        delta = building_position - villager.position
        if delta.magnitude <= 6:
            del player.commands['later']['build building'][villager]
            player.commands['now']['build building'][villager] = [building, building_position]


# The following will only be used if I eventually end up using
# player.commands['later']['collect resource']
def update_collect_resource_command(player):
    pass


# The following removes all the old commands in player.commands['now']['move'], and it updates
# player.commands['now']['move'] based on what player.commands['later']['move'] is.
def update_move_commands(player):
    for unit in list(player.commands['now']['move']):
        del player.commands['now']['move'][unit]

    for unit in list(player.commands['later']['move']):
        delta = player.commands['later']['move'][unit]
        if delta.magnitude > 15:
            beginning, the_rest = delta.beginning_plus_the_rest()
            player.commands['now']['move'][unit] = beginning
            player.commands['later']['move'][unit] = the_rest
        else:
            player.commands['now']['move'][unit] = delta
            del player.commands['later']['move'][unit]


def update_build_unit_commands(player):
    for building in list(player.commands['now']['build unit']):
        del player.commands['now']['build unit'][building]

    for building in list(player.commands['later']['build unit']):
        unit_type = player.commands['later']['build unit'][building][0]
        num_left_to_build = player.commands['later']['build unit'][building][1]
        num_can_build = number_of_units_can_build_in_one_turn(player, building, unit_type)

        num_to_build_now = min(num_can_build, num_left_to_build)
        num_to_build_later = num_left_to_build - num_to_build_now
        player.commands['now']['build unit'][building] = [unit_type, num_to_build_now]
        if num_to_build_later > 0:
            player.commands['later']['build unit'][building] = [unit_type, num_to_build_later]
        else:
            del player.commands['later']['build unit'][building]


###################################################################################################
###################################################################################################
###################################################################################################
def implement_commands_if_possible(player):
    implement_build_building_command(player)
    implement_collect_resource_command(player)
    implement_move_commands(player)
    implement_build_unit_commands(player)
    # Eventually, this will probably be replaced with the following code, where functions is a list
    # of all the functions which need to be run.
    # for function in functions:
    #     function(player)

def implement_build_building_command(player):
    for villager in player.commands['now']['build building']:
        building = player.commands['now']['build building'][villager][0]
        building.build(villager, player)


def implement_collect_resource_command(player):
    for villager in player.commands['now']['collect resource']:
        resource = player.commands['now']['collect resource'][villager]
        if villager.can_collect_resource_now(resource, player):
            villager.collect_resource(resource, player)


def implement_move_commands(player):
    for unit in player.commands['now']['move']:
        delta = player.commands['now']['move'][unit]
        if unit.can_move(delta, game_map):
            unit.move_by(delta)


def implement_build_unit_commands(player):
    for building in player.commands['now']['build unit']:
        unit_type, num_to_build = player.commands['now']['build unit'][building]
        for i in range(num_to_build):
            if player.population < player.population_cap:
                if not unit_type in unit_kind_to_class:
                    continue
                unit = unit_kind_to_class[unit_type]
                if player.can_build(unit):
                    building.build_unit(player, unit_type)
                else:
                    unit_type = unit_kind_to_singular[unit.kind].capitalize()
                    print('You do not have enough resources to build a ', unit_type)
                    continue
            else:
                print('Population cap reached. You cannot build more units.')
                return

if __name__ == '__main__':
    pass
