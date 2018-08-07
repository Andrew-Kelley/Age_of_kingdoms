# This module handles the commands which are returned by the function input_next_command
# The main function of this module is insert_command

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

    player.commands['now']['move'] = move_now
    player.commands['later']['move'] = move_later
