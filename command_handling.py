# This module handles the commands which are returned by the function input_next_command

from game_map import Vector

# player.commands['now'] is in the following format:
# {'move':dict( unit:position_delta for units to be moved ), # position_delta is a Vector
#  'build building':dict( villager:building_to_be_built for ...),
#  'collect resource':( villager:resource_object_to_collect for ...),
#  'build unit':dict( building:[unit_to_be_built, number_of_units_of_that_type_to_build] for ... ),
#  'research':dict( building:thing_to_be_researched for ...),
#  ...}
# Eventually, player.commands should also contain keywords such as follows:
# 'attack', 'defend'

# I need to have a function which checks if a given unit has already been commanded to do something. I
# think newer commands will override older ones.


def insert_command(player, command):
    if not type(command) is list or len(command) == 0:
        return

    # MAYBE call any of the functions with one call
    if command[0] == 'move':
        insert_a_move_command(player, command)
        return


def insert_a_move_command(player, command):
    if len(command) != 3:
        return
    ls_of_units = command[1]
    if not type(ls_of_units) is list:
        return
    delta = command[2]
    if not isinstance(delta, Vector):
        return

    if delta.magnitude > 15:
        beginning, the_rest = delta.beginning_plus_the_rest()
        move_now = dict((unit, beginning) for unit in ls_of_units)
        move_later = dict((unit, the_rest) for unit in ls_of_units)
    else:
        move_now = dict((unit, delta) for unit in ls_of_units)
        move_later = dict()

    # NOTE: THE FOLLOWING TWO LINES DOES NOT WORK! The reason is that the player might make multiple
    # move commands during a turn (each of which might move different units). What the following two
    # lines would do would be to erase all previous move commands and replace them with the most current
    # one.
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


# The following is called at the beginning of each player's turn.
def update_now_and_later_commands(player):
    update_now_and_later_move_commands(player)


def update_now_and_later_move_commands(player):
    for unit in player.commands['now']['move']:
        del player.commands['now']['move'][unit]

    for unit in player.commands['later']['move']:
        delta = player.commands['later']['move'][unit]
        if delta.magnitude > 15:
            beginning, the_rest = delta.beginning_plus_the_rest()
            player.commands['now']['move'][unit] = beginning
            player.commands['later']['move'][unit] = the_rest
        else:
            player.commands['now']['move'][unit] = delta
            del player.commands['later']['move'][unit]