from command_handling.insert_commands import insert_move_later_command
from command_handling.commands import MoveCmd


# This is to be used only for newly built units, in their __init__ method
def set_unit_position_and_movement(building, new_unit, player, distance=6):
    """If the new_unit also requires to be initialized with a move command, then
    this function handles that too."""
    delta = building.build_position - building.position
    if delta.magnitude > distance:
        delta1, delta2 = delta.beginning_plus_the_rest(distance_in_one_turn=distance)
        build_position = building.position + delta1
        new_unit.position = build_position
        command = MoveCmd()
        command.add_unit_with_delta(new_unit, delta2)
        insert_move_later_command(player, command)
    else:
        # TODO: This is too simple to work properly for non-military units
        build_position = building.position + delta
        new_unit.position = build_position
