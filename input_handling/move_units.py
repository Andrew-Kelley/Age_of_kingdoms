from input_handling.direction_vector import get_direction_vector
from input_handling.select_an_object import SelectedUnits, extract_selected_obj
from input_handling.from_ls_get_position import get_position_from_inpt_as_ls
from command_handling.commands import MoveCmd
from map_etc.make_map import game_map

def move_unit_or_units(player, inpt_as_ls, selected_obj=None):
    """Returns None or an instance of MoveCmd

    selected_obj must be None or an instance of SelectedUnits

    In order for this function to not return None, inpt_as_ls must be of the
    following type: (In what follows, <direction string> can be one or two
    entries of the list.)
    ['move', 'to', i, j] where selected_obj is not None and (i, j) is a
                         position on the map.
                         (Actually ['move', 'to', ..., i, j] works where what
                         is in the ellipsis is ignored.
    ['move', <direction string>] where selected_obj is not None, or
    ['move', unit.kind singular, 'unit.number', <direction string>], or
    ['move', unit.kind plural, 'num1-num2', <direction string>], or
    ['move', 'group', 'group_num', <direction string>], or
    ['move', 'army', 'army_num', <direction string>].
    In each case, <direction string> must be formatted such that the
    fn direction_inpt_to_vector does not return None.
    """
    if len(inpt_as_ls) < 2:
        return

    if inpt_as_ls[1] == 'to':
        # This is a 'move to absolute position' command
        position_to_move_to = get_position_from_inpt_as_ls(inpt_as_ls)
        if not position_to_move_to:
            print("Command rejected. The position to move your unit(s) to in your")
            print("command was not understood.")
            return

        if not position_to_move_to.is_on_the_map(game_map):
            print_not_on_map_error_message(position_to_move_to)
            return

        if nothing_is_selected(selected_obj):
            return

        command = MoveCmd()
        for unit in selected_obj.units:
            delta = position_to_move_to - unit.position
            command.add_unit_with_delta(unit, delta)
        return command

    # If this is reached, then the command is to move units to a position relative
    # to the units' positions (such as n10 e4 i.e. north 10 and east 4)
    delta = get_direction_vector(inpt_as_ls)
    if delta is None:
        return

    if len(inpt_as_ls) in {2, 3}:
        # Then the player is trying to move selected_obj and

        if nothing_is_selected(selected_obj):
            return

        command = MoveCmd()
        for unit in selected_obj.units:
            position = unit.position + delta
            if not position.is_on_the_map(game_map):
                print_not_on_map_error_message(position)
                return
            command.add_unit_with_delta(unit, delta)
        return command
    else:  # len(inpt_as_ls) > 3
        selected_obj = extract_selected_obj(inpt_as_ls, player)
        if nothing_is_selected(selected_obj):
            return

        command = MoveCmd()
        for unit in selected_obj.units:
            position = unit.position + delta
            if not position.is_on_the_map(game_map):
                print_not_on_map_error_message(position)
                return
            command.add_unit_with_delta(unit, delta)
        return command


def nothing_is_selected(selected_obj):
    if not isinstance(selected_obj, SelectedUnits):
        # TODO: edit this once I add the Army and Group class?
        return True
    if selected_obj.is_empty:
        return True

    return False


def print_not_on_map_error_message(position):
    print("Command rejected.")
    print("Position ", position, " is not on the map.")
