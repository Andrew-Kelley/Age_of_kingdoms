from command_handling.insert_commands import insert_move_later_command
from command_handling.commands import MoveCmd

from map_etc.search_for_open_position import bfs_for_open_spot
from map_etc.make_map import game_map
from map_etc.iterate_around import positions_around

# This is to be used only for newly built units, in their __init__ method
def set_unit_position_and_movement(building, new_unit, player, distance=6):
    """If the new_unit also requires to be initialized with a move command, then
    this function handles that too."""
    delta = building.build_position - building.position
    if delta.magnitude > distance:
        delta1, delta2 = delta.beginning_plus_the_rest(distance_in_one_turn=distance)
        build_position = building.position + delta1

        # The line "new_unit.position = build_position" is not sufficient.
        # The issue would be if there already is a unit or building at
        # build_position, which is why reset_initial_position... is called later
        new_unit.position = build_position

        # resetting the initial position doesn't affect new_unit.position if
        # that position didn't already have something else there.
        # The value of radius is somewhat arbitrary. The larger it is, the
        # greater the likelihood that some position will be open.
        reset_initial_position_to_first_open_spot(new_unit, radius=12)
        delta2 = building.build_position - new_unit.position

        command = MoveCmd()
        command.add_unit_with_delta(new_unit, delta2)
        insert_move_later_command(player, command)
    else:
        # bfs_for_open_spot starts searching at the position of the input unit
        build_position = building.position + delta
        new_unit.position = build_position
        # The 50 is just any large number to practically guarantee that the
        # search will be successful (assuming build_position isn't in the
        # middle of a building)
        delta = bfs_for_open_spot(new_unit, game_map, bound_on_search_distance=50)
        if delta is not None:
            new_unit.position += delta
        else:
            # This "else" section is necessary in the case that a building's
            # build_position is some position that the building occupies.

            # The 40 is just any large number to practically guarantee that the
            # search will be successful
            reset_initial_position_to_first_open_spot(new_unit, radius=40)


def reset_initial_position_to_first_open_spot(new_unit, radius):
    """Set the position of new_unit to be any open spot around it.

    This is used in case the initial position of new_unit is already
    taken by something else."""
    for position in positions_around(new_unit.position, radius):
        delta = position - new_unit.position
        if new_unit.can_move(delta, game_map):
            new_unit.position += delta
            return
