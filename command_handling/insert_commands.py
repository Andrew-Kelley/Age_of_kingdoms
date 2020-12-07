from collections import deque

from map_etc.position import Position
from map_etc.make_map import game_map

from units import Villager, unit_kind_to_class
from buildings.resource_bldngs import Farm
from buildings.bldng_class import BuildingUnderConstruction

from command_handling.commands import Command, BuildUnitCmd, BuildBuildingCmd
from command_handling.commands import CollectResourceCmd, ResearchCmd, FarmCmd
from command_handling.commands import MoveCmd

def insert_command(player, command):
    if command is None:
        return
    message = "Developer error: insert_command was called when command was"
    if not isinstance(command, Command):
        print(message)
        print(command)
        print("But command should have been an instance of Command.")
        return

    # MAYBE call all of the functions with one call (and a dictionary of functions).
    if isinstance(command, MoveCmd):
        insert_move_command(player, command)
        return
    elif isinstance(command, BuildUnitCmd):
        insert_build_unit_command(player, command)
        return
    elif isinstance(command, CollectResourceCmd):
        insert_collect_resource_now_command(player, command)
        return
    elif isinstance(command, BuildBuildingCmd):
        insert_build_building_command(player, command)
        return
    elif isinstance(command, ResearchCmd):
        insert_research_command(player, command)
        return
    elif isinstance(command, FarmCmd):
        insert_farm_command(player, command)
        return
    else:
        print(message)
        print(command)
        print("So command was not an instance of a sublcass of Command that")
        print("input_command can handle yet.")


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


def is_initialized_instance(command, CommandClass):
    if not isinstance(command, CommandClass):
        print("Developer error: command was not an instance of the proper class.")
        print("command: ", command)
        print("Class: ", CommandClass)
        return False
    if not command.is_initialized:
        print("Developer error. The following command was not initialized:")
        print(command)
        return False
    return True


def insert_build_building_command(player, command):
    if not is_initialized_instance(command, BuildBuildingCmd):
        return

    building_class = command.building_class

    villagers = command.villagers()

    building_position = command.position
    if not isinstance(building_position, Position):
        return

    for villager in villagers:
        for command_type in ('move', 'collect resource', 'farm'):
            remove_unit_from_command_if_there(player, villager, command_type)

    # The following few lines are to handle the situation that other villagers are already
    # building an instance of building_class at building_position
    this_is_a_help_build_command = command.is_a_help_build_cmd
    if this_is_a_help_build_command:
        building = building_already_in_progress(player, building_class, building_position)
        if not building:
            print('Sorry, your command to help build that building was rejected.')
            print('Remember, to help build a building already under construction,')
            print('You must use the exact position it was built at.')
            return
    else:
        if not player.has_resources_to_build(building_class):
            print('You do not have enough resources to build that building.')
            return
        building_number = len(player.buildings[building_class.kind])
        building = building_class(building_number, building_position, player)
        player.resources -= building.cost
        building.build_on_map(building_position, game_map)
        # The following is a placeholder until the building is completely built.
        temp_building = BuildingUnderConstruction(building_class, building_number,
                                                          building_position, player)
        player.buildings[building_class.kind].append(temp_building)
        building.construction_alias = temp_building

    for i, villager in enumerate(villagers):
        if isinstance(building, Farm):
            if i < 2:
                player.commands['later']['farm'][villager] = building
        delta = building_position - villager.position
        if delta.magnitude <= 6:
            player.commands['now']['build building'][villager] = [building, building_position]
            villager.current_action = 'building {}'.format(building)
        else:
            new_command = MoveCmd()
            new_command.add_unit_with_delta(villager, delta)
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


def collecting_resource_action(resource_kind):
    current_action = ''
    if resource_kind == "wood":
        current_action = "chopping " + resource_kind
    elif resource_kind in ("gold", "iron", "bronze"):
        current_action = "mining " + resource_kind
    elif resource_kind == "stone":
        current_action = "quarrying " + resource_kind
    elif resource_kind == "food":
        current_action = "collecting " + resource_kind
    else:
        print("Error: collecting ", resource_kind)
    return current_action


def insert_collect_resource_now_command(player, command):
    if not is_initialized_instance(command, CollectResourceCmd):
        return
    resource = command.resource

    for unit in command.villagers():
        for command_type in ('move', 'build building', 'farm'):
            remove_unit_from_command_if_there(player, unit, command_type)

    for villager in command.villagers():
        if villager.can_collect_resource_now(resource, player):
            player.commands['now']['collect resource'][villager] = resource
            villager.current_action = collecting_resource_action(resource.kind)
        else:
            villager.current_action = 'doing nothing'
            print(villager, ' cannot collect {} now.'.format(resource.kind))


# The following is only intended to be used for newly built villagers (after a player has
# decided to give a default command to newly built villagers). However, it might also be
# useful for "smart" villagers i.e. for villagers who collect resources after building a
# building such as a lumber camp.
def insert_collect_resource_later_command(player, command):
    if not is_initialized_instance(command, CollectResourceCmd):
        return

    resource = command.resource
    villagers = command.villagers()

    for villager in villagers:
        player.commands['later']['collect resource'][villager] = resource


# The following function could instead be named insert_a_command_of_type_move
def insert_move_command(player, command):
    if not is_initialized_instance(command, MoveCmd):
        return

    for unit, delta in command.units_and_deltas():
        for command_type in ('build building', 'collect resource', 'farm'):
            remove_unit_from_command_if_there(player, unit, command_type)

        unit.current_action = 'moving to {}'.format(unit.position + delta)

        if delta.magnitude > 15:
            beginning, the_rest = delta.beginning_plus_the_rest()
            player.commands['now']['move'][unit] = beginning
            player.commands['later']['move'][unit] = the_rest
        else:
            player.commands['now']['move'][unit] = delta
            if unit in player.commands['later']['move']:
                del player.commands['later']['move'][unit]

    # TODO: delete the following commented code if this function works.
    # if delta.magnitude > 15:
    #     beginning, the_rest = delta.beginning_plus_the_rest()
    #     move_now = dict((unit, beginning) for unit in ls_of_units)
    #     move_later = dict((unit, the_rest) for unit in ls_of_units)
    # else:
    #     move_now = dict((unit, delta) for unit in ls_of_units)
    #     move_later = dict()
    #
    # # NOTE: THE FOLLOWING TWO COMMENTED LINES DO NOT WORK! The reason is that
    # # the player might make multiple move commands during a turn (each of which
    # # might move different units).
    # # What the following two lines would do would be to erase all previous
    # # move commands and replace them with the most current one.
    # # player.commands['now']['move'] = move_now
    # # player.commands['later']['move'] = move_later
    #
    # # The following only replaces old move commands with new ones if they are about the
    # # same unit.
    # for unit in move_now:
    #     player.commands['now']['move'][unit] = move_now[unit]
    #     unit.current_action = 'moving to {}'.format(unit.position + delta)
    #     if unit in player.commands['later']['move']:
    #         del player.commands['later']['move'][unit]
    # for unit in move_later:
    #     player.commands['later']['move'][unit] = move_later[unit]
    # return


def insert_move_later_command(player, command):
    """This should ONLY be used when a unit is initially built."""
    if not is_initialized_instance(command, MoveCmd):
        return

    for unit, delta in command.units_and_deltas():
        player.commands['later']['move'][unit] = delta
        unit.current_action = 'moving to {}'.format(unit.position + delta)


def insert_build_unit_command(player, command):
    """Modifies player.commands['now']['build unit'] and...
    also modifies player.commands['later']['build unit']
    """
    if not is_initialized_instance(command, BuildUnitCmd):
        return

    building = command.building
    unit_kind = command.unit_kind
    num_to_be_built = command.num_to_build

    if unit_kind not in building.units_which_can_be_built():
        print('The selected building cannot build that unit.')
        print(cannot_build_unit_yet_error_message(player, building, unit_kind))
        return

    unit_class = unit_kind_to_class[unit_kind]
    the_cost = unit_class.cost * num_to_be_built
    if not player.resources >= the_cost:
        print("You do not have enough resources. Command rejected.")
        return
    player.resources -= the_cost

    num_can_build = number_of_units_can_build_in_one_turn(player, building, unit_kind)

    num_to_build_now = min(num_can_build, num_to_be_built)
    num_to_build_later = num_to_be_built - num_to_build_now
    player.commands['now']['build unit'][building] = [unit_kind, num_to_build_now]
    if num_to_build_later > 0:
        player.commands['later']['build unit'][building] = [unit_kind, num_to_build_later]
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
    if not is_initialized_instance(command, ResearchCmd):
        return

    building = command.building
    thing_to_be_researched = command.thing_to_be_researched
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
    if not is_initialized_instance(command, FarmCmd):
        return

    farm = command.farm

    villagers = command.villagers()

    for villager in villagers:
        delta = farm.position - villager.position
        if delta.magnitude <= 6:
            if delta.magnitude >= 2:
                villager.move_by(delta, game_map)
            if farm.number_of_farmers < 2:
                player.commands['now']['farm'][villager] = farm
                farm.add_farmer(villager)
                villager.farm_currently_farming = farm
                # TODO: Does the following print properly?
                villager.current_action = 'farming {}'.format(farm)
            else:
                print('The farm already has 2 villagers farming it.')
        else:
            new_command = MoveCmd()
            new_command.add_unit_with_delta(villager, delta)
            insert_move_command(player, new_command)
            player.commands['later']['farm'][villager] = farm
