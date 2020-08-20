from input_handling.direction_vector import get_direction_vector
from input_handling.select_an_object import SelectedUnits, extract_selected_obj

def move_unit_or_units(player, inpt_as_ls, selected_obj=None):
    """If selected_obj must be None or an instance of SelectedObject

    In order for this function to not return [], inpt_as_ls must be of the following
    type:
    (In what follows, each list may end with one or two entries of <direction string>)

    # WHAT DID I MEAN BY THE FOLLOWING LINE?
    # In the first two cases, selected_obj must be of the type that select_something
    returns ['move', <direction string>], or

    ['move', unit.kind singular, 'unit.number', <direction string>], or
    ['move', unit.kind plural, 'num1-num2', <direction string>], or
    ['move', 'group', 'group_num', <direction string>], or
    ['move', 'army', 'army_num', <direction string>], where
    <direction string> must be formatted such that the fn direction_inpt_to_vector
    does not return None.

    Returns: [] or
    ['move', ls_of_units, delta], where delta is of type Vector
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