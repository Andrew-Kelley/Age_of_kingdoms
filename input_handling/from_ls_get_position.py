from map_etc.position import Position

def str_to_int(s):
    try:
        return int(s)
    except ValueError:
        return None


def get_position_from_inpt_as_ls(inpt_as_ls):
    """Return None or an instance of Position.

    This assumes the last two entries of inpt_as_ls are the coordinates
    of a position on the map."""
    if len(inpt_as_ls) < 2:
        return

    x = str_to_int(inpt_as_ls[-2])
    y = str_to_int(inpt_as_ls[-1])
    if x is None or y is None:
        return

    return Position(x, y)
