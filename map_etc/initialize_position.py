from command_handling.insert_commands import insert_move_later_command
from command_handling.commands import MoveCmd

from map_etc.search_for_open_position import bfs_for_open_spot
from map_etc.make_map import game_map

# This is to be used only for newly built units, in their __init__ method
def set_unit_position_and_movement(building, new_unit, player, distance=6):
    """If the new_unit also requires to be initialized with a move command, then
    this function handles that too."""
    delta = building.build_position - building.position
    if delta.magnitude > distance:
        delta1, delta2 = delta.beginning_plus_the_rest(distance_in_one_turn=distance)
        build_position = building.position + delta1
        # The following line might be a small bug. The issue would be if there
        # already is a unit or building at build_position
        new_unit.position = build_position
        command = MoveCmd()
        command.add_unit_with_delta(new_unit, delta2)
        insert_move_later_command(player, command)
    else:
        # bfs_for_open_spot starts searching at the position of the input unit
        build_position = building.position + delta
        new_unit.position = build_position
        # The 50 is just any large number to practically guarantee that the
        # search will be successful
        delta = bfs_for_open_spot(new_unit, game_map, bound_on_search_distance=50)
        if delta is not None:
            new_unit.position += delta
