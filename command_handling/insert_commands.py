
from collections import deque

from game_map import Position, Vector, game_map
from buildings.bldng_class import Building
from units import unit_kinds, Villager
from resources import resource_ls
from buildings.resource_bldngs import Farm


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
        insert_collect_resource_now_command(player, command)
        return
    elif command[0] == 'build building':
        insert_build_building_command(player, command)
        return
    elif command[0] == 'research':
        insert_research_command(player, command)
        return
    elif command[0] == 'farm':
        insert_farm_command(player, command)
        return


def remove_unit_from_command_if_there(player, unit, command_type):
    """If unit is in player.commands['now'][command_type], then this function removes
    the unit from that command. If unit is not in player.commands['now'][command_type],
    this function does nothing.

    command_type should be one of the following:
    'move', 'build building', 'collect resource', 'farm' """
    if command_type not in ('move', 'build building', 'collect resource', 'farm'):
        return
    if unit in list(player.commands['now'][command_type]):
        del player.commands['now'][command_type][unit]
    if command_type == 'farm':
        if isinstance(unit, Villager):
            farm = unit.farm_currently_farming
            if isinstance(farm, Farm):
                farm.remove_farmer_if_there(unit)
            unit.farm_currently_farming = None


def insert_build_building_command(player, command):
    """command must be of the following format:
    ['build building', ls_of_villagers, building_class, position, is_help_bld_cmmd]"""
    if len(command) != 5:
        return

    building_class = command[2]

    ls_of_villagers = command[1]
    if not type(ls_of_villagers) is list or len(ls_of_villagers) == 0:
        return

    building_position = command[3]
    if not isinstance(building_position, Position):
        return

    for villager in ls_of_villagers:
        for command_type in ('move', 'collect resource', 'farm'):
            remove_unit_from_command_if_there(player, villager, command_type)

    # The following few lines are to handle the situation that other villagers are already
    # building an instance of building_class at building_position
    this_is_a_help_build_command = command[4]
    if this_is_a_help_build_command:
        building = building_already_in_progress(player, building_class, building_position)
        if not building:
            print('Sorry, your command to help build that building was rejected.')
            print('Remember, to help build a building already under construction,')
            print('You must use the exact position it was built at.')
            return
    else:
        if not player.can_build(building_class):
            print('You do not have enough resources to build that building.')
            return
        building_number = len(player.buildings[building_class.kind])
        building = building_class(building_number, building_position, player)
        player.resources -= building.cost
        building.build_on_map(building_position, game_map)

    for i, villager in enumerate(ls_of_villagers):
        if isinstance(building, Farm):
            if i < 2:
                player.commands['later']['farm'][villager] = building
        delta = building_position - villager.position
        if delta.magnitude <= 6:
            player.commands['now']['build building'][villager] = [building, building_position]
            villager.current_action = 'building {}'.format(building)
        else:
            new_command = ['move', [villager], delta]
            insert_move_command(player, new_command)
            player.commands['later']['build building'][villager] = [building, building_position]


def building_already_in_progress(player, building_class, position):
    """Returns the building instance if the player is already building an instance of
    building_class at position. Otherwise, this returns False."""
    for time in ('now', 'later'):
        for villager in player.commands[time]['build building']:
            ls = player.commands[time]['build building'][villager]
            if ls[1] == position and \
                    ls[0].letter_abbreviation == building_class.letter_abbreviation:
                return ls[0]
    return False


def insert_collect_resource_now_command(player, command):
    if not collect_resource_command_is_properly_formatted(command):
        return
    resource = command[1]
    ls_of_villagers = command[2]

    for unit in ls_of_villagers:
        for command_type in ('move', 'build building', 'farm'):
            remove_unit_from_command_if_there(player, unit, command_type)

    for villager in ls_of_villagers:
        if villager.can_collect_resource_now(resource, player):
            player.commands['now']['collect resource'][villager] = resource
            villager.current_action = 'collecting {}'.format(resource.kind)
        else:
            villager.current_action = 'doing nothing'
            print(villager, ' cannot collect {} now.'.format(resource.kind))


# The following is only intended to be used for newly built villagers (after a player has
# decided to give a default command to newly built villagers). However, it might also be
# useful for "smart" villagers i.e. for villagers who collect resources after building a
# building such as a lumber camp.
def insert_collect_resource_later_command(player, command):
    if not collect_resource_command_is_properly_formatted(command):
        return
    resource = command[1]
    ls_of_villagers = command[2]

    for villager in ls_of_villagers:
        player.commands['later']['collect resource'][villager] = resource


def collect_resource_command_is_properly_formatted(command):
    if len(command) != 3:
        return False
    resource = command[1]
    if resource not in resource_ls:
        return False
    ls_of_villagers = command[2]
    if not type(ls_of_villagers) is list or len(ls_of_villagers) == 0:
        return False
    if not all(isinstance(u, Villager) for u in ls_of_villagers):
        return False
    return True


# The following function could instead be named insert_a_command_of_type_move
def insert_move_command(player, command):
    """In order for command to be handled properly, it must be in the following format:
    ['move', ls_of_units, delta], where delta is of type Vector"""
    if not move_command_is_properly_formatted(command):
        return
    ls_of_units = command[1]
    delta = command[2]

    for unit in ls_of_units:
        for command_type in ('build building', 'collect resource', 'farm'):
            remove_unit_from_command_if_there(player, unit, command_type)

    if delta.magnitude > 15:
        beginning, the_rest = delta.beginning_plus_the_rest()
        move_now = dict((unit, beginning) for unit in ls_of_units)
        move_later = dict((unit, the_rest) for unit in ls_of_units)
    else:
        move_now = dict((unit, delta) for unit in ls_of_units)
        move_later = dict()

    # NOTE: THE FOLLOWING TWO LINES DO NOT WORK! The reason is that the player might
    # make multiple move commands during a turn (each of which might move different
    # units). What the following two lines would do would be to erase all previous
    # move commands and replace them with the most current one.
    # player.commands['now']['move'] = move_now
    # player.commands['later']['move'] = move_later

    # The following only replaces old move commands with new ones if they are about the
    # same unit.
    for unit in move_now:
        player.commands['now']['move'][unit] = move_now[unit]
        unit.current_action = 'moving to {}'.format(unit.position + delta)
        if unit in player.commands['later']['move']:
            del player.commands['later']['move'][unit]
    for unit in move_later:
        player.commands['later']['move'][unit] = move_later[unit]
    return


def insert_move_later_command(player, command):
    """This should ONLY be used when a unit is initially built."""
    if not move_command_is_properly_formatted(command):
        return
    ls_of_units = command[1]
    delta = command[2]

    for unit in ls_of_units:
        player.commands['later']['move'][unit] = delta
        unit.current_action = 'moving to {}'.format(unit.position + delta)


def move_command_is_properly_formatted(command):
    if len(command) != 3:
        return False
    ls_of_units = command[1]
    if not type(ls_of_units) is list:
        return False
    delta = command[2]
    if not isinstance(delta, Vector):
        return False
    return True


def insert_build_unit_command(player, command):
    """Modifies player.commands['now']['build unit'] and player.commands['later']['build unit']

    The argument command must be of the following format (which is what the function build_unit
    in the input_handling module returns):
    ['build unit', <building>, <unit type>, num_to_be_built]"""
    if len(command) != 4:
        # This should never be the case.
        print('Python Error! The function insert_build_unit_command was given an '
              'argument command that is not of length 4.')
        return

    building = command[1]
    unit_type = command[2]
    num_to_be_built = command[3]
    if not isinstance(building, Building):
        return
    if unit_type not in unit_kinds:
        return
    if num_to_be_built < 1 or not type(num_to_be_built) is int:
        return

    if unit_type not in building.units_which_can_be_built():
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
    if building.kind == 'towncenter':
        if unit_type == 'villagers':
            num_can_build = building.num_villagers_can_build_in_turn(player)
        else:
            num_can_build = 0
    else:
        # I may later want to change this and allow some units besides villagers to be
        # built more than 1 per turn per building.
        num_can_build = 1
    return num_can_build


def cannot_build_unit_yet_error_message(player, building, unit_type):
    if unit_type == 'swordsmen':
        message = "A barracks can build a swordsmen only after the Bronze Age is researched "
        message += "and after the following two things are researched at the Blacksmith:"
        message += "\n (a) bronze shields, and (b) bronze swords"
    elif unit_type == 'trebuchets':
        message = "A SiegeWorks can build a trebuchet only after the Iron Age is researched."
    else:
        message = ''
    return message


def insert_research_command(player, command):
    if len(command) != 3:
        return

    building = command[1]
    thing_to_be_researched = command[2]
    if not player.has_resources_to_research(thing_to_be_researched):
        print("You do not have enough resources to research this:")
        print(thing_to_be_researched.name)
        return
    player.resources -= thing_to_be_researched.cost
    if building in player.commands['now']['research']:
        if building in player.commands['later']['research']:
            player.commands['later']['research'][building].append(thing_to_be_researched)
        else:
            player.commands['later']['research'][building] = deque([thing_to_be_researched])
    else:
        player.commands['now']['research'][building] = thing_to_be_researched
        print('Beginning the following research: {}\n'.format(thing_to_be_researched.name))


def insert_farm_command(player, command):
    if len(command) != 3:
        return

    farm = command[1]
    if not isinstance(farm, Farm):
        return

    ls_of_villagers = command[2]
    if not type(ls_of_villagers) is list or len(ls_of_villagers) == 0:
        return
    if not all(isinstance(u, Villager) for u in ls_of_villagers):
        return

    for villager in ls_of_villagers:
        delta = farm.position - villager.position
        if delta.magnitude <= 6:
            if delta.magnitude >= 2:
                villager.move_by(delta)
            if farm.number_of_farmers < 2:
                player.commands['now']['farm'][villager] = farm
                farm.add_farmer(villager)
                villager.farm_currently_farming = farm
                # TODO: Does the following print properly?
                villager.current_action = 'farming {}'.format(farm)
            else:
                print('The farm already has 2 villagers farming it.')
        else:
            new_command = ['move', [villager], delta]
            insert_move_command(player, new_command)
            player.commands['later']['farm'][villager] = farm

