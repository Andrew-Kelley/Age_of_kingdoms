from input_handling.direction_vector import get_direction_vector
from input_handling.select_an_object import SelectedUnits, extract_selected_obj


def move_unit_or_units(player, inpt_as_ls, selected_obj=None):
    """Returns [] or ['move', ls_of_units, delta],
    where delta is of type Vector

    selected_obj must be None or an instance of SelectedUnits

    In order for this function to not return [], inpt_as_ls must be of the
    following type: (In what follows, <direction string> can be one or two
    entries of the list.)
    ['move', <direction string>] where selected_obj is not None, or
    ['move', unit.kind singular, 'unit.number', <direction string>], or
    ['move', unit.kind plural, 'num1-num2', <direction string>], or
    ['move', 'group', 'group_num', <direction string>], or
    ['move', 'army', 'army_num', <direction string>].
    In each case, <direction string> must be formatted such that the
    fn direction_inpt_to_vector does not return None.
    """
    if len(inpt_as_ls) < 2:
        return []

    delta = get_direction_vector(inpt_as_ls)
    if delta is None:
        return []

    if len(inpt_as_ls) in {2, 3}:
        # Then the player is trying to move selected_obj

        if not isinstance(selected_obj, SelectedUnits):
            # TODO: edit this once I add the Army and Group class?
            return []
        if selected_obj.is_empty:
            return []

        # Todo: Change the following so that I can use an iterator instead.
        ls_of_units = list(selected_obj.units)
        return ['move', ls_of_units, delta]

    else:  # len(inpt_as_ls) > 3
        selected_obj = extract_selected_obj(inpt_as_ls, player)
        if not isinstance(selected_obj, SelectedUnits):
            # TODO: edit this once I add the Army and Group class?
            return []

        if selected_obj.is_empty:
            return []
        # Todo: Change the following so that I can use an iterator instead.
        ls_of_units = list(selected_obj.units)
        return ['move', ls_of_units, delta]
