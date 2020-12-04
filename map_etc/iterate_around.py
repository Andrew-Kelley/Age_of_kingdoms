from map_etc.position import Position


def within_given_distance(obj1, obj2, distance):
    vector = obj1.position - obj2.position
    return vector.magnitude <= distance


def everything_within_given_distance_on(the_map, distance, position):
    """Iterates through everything on the_map that is within the given distance
    of position.

    This portion of the_map is in the shape of a diamond.

    position must be of type Position
    distance must be a non-negative int"""
    if not type(distance) is int:
        print('distance must be an int')
        return
    if distance < 0:
        print('distance must not be negative')
        return

    # The following is the center of the diamond-shaped portion of the map.
    x0, y0 = position.value

    # The following iterates through the diamond shaped portion of the_map
    # from bottom to top, left to right.
    for y_delta in range(-1 * distance, distance + 1):
        sign_to_mult_by = 1 if y_delta <= 0 else -1
        horizontal_radius = distance + y_delta * sign_to_mult_by
        # height is how far up or down the map, we need to go
        for x_delta in range(-1 * horizontal_radius, horizontal_radius + 1):
            x = x0 + x_delta
            y = y0 + y_delta
            this_position = Position(x, y)
            if this_position.is_on_the_map(the_map):
                yield the_map[y][x]
