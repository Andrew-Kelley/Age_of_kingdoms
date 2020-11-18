from game_map import Vector


def direction_inpt_to_vector(direction_str):
    """direction_str must be a string. Returns a Vector or None.
    In order to not return None, direction_str must be a string of the form
    'D<num>' where D is in 'nsew' (north, south, east, west) and <num> is
    an integer possible inputs: 'n5' 'e17' 's12' """
    if not type(direction_str) is str:
        return None
    if len(direction_str) < 2:
        return None
    direction = direction_str[0]
    if direction not in 'nsew':
        return None

    try:
        distance = int(direction_str[1:])
    except ValueError:
        return None

    if direction == 'n':
        return Vector(0, distance)
    elif direction == 's':
        return Vector(0, -1 * distance)
    elif direction == 'e':
        return Vector(distance, 0)
    elif direction == 'w':
        return Vector(-1 * distance, 0)
    else:
        # I think it is impossible for this code to run, due to one of the if
        # statements at the beginning of this function.
        print("Error. direction_inpt_to_vector was called and the")
        print("direction string was not understood.")


def get_direction_vector(inpt_as_ls):
    """returns None or Vector.

    One thing that is a little odd about this function is that if inpt_as_ls[-2]
    is a direction in the wrong format, this function just ignores it and treats
    it as if it didn't exist."""
    if len(inpt_as_ls) < 2:
        return None

    delta1 = direction_inpt_to_vector(inpt_as_ls[-1])
    if delta1 is None:
        print('The last direction vector input was not understood.')
        return None

    delta2 = direction_inpt_to_vector(inpt_as_ls[-2])
    if delta2 is None:
        delta2 = Vector(0, 0)

    return delta1 + delta2


if __name__ == '__main__':
    for s in ('nn', 'n14s', '4s', 'j3', 'n'):
        assert direction_inpt_to_vector(s) is None

    # for s in ('n4', 'n10', 's5', 's12', 'e100', 'e0', 'w2', 'w25'):
    #     print(s, direction_inpt_to_vector(s))