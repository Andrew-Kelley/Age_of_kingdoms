from map_etc.position import Position, Vector
from map_etc.make_map import game_map


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


def positions_around(center, radius):
    """An iterator of all positions within radius of center.

    This first starts with the center and then goes around
    and around going further and further out.

    center must be an instance of Position"""
    if not type(radius) is int:
        print('radius must be an int')
        return
    if radius < 0:
        print('radius must not be negative')
        return
    if not center.is_on_the_map(game_map):
        return

    yield center

    for distance in range(1, radius+1):
        for position in down_left(center, distance):
            yield position
        for position in down_right(center, distance):
            yield position
        for position in up_right(center, distance):
            yield position
        for position in up_left(center, distance):
            yield position


# The following implements down_left, down_right, up_right, and up_left
def traverse_side(offset, delta):
    """Start at center + offset and traverse side of diamond

    This excludes the last vertex at the end of the side."""
    def iterator(center, distance):
        start = center + offset * distance
        for i in range(distance):
            current = start + delta * i
            if not current.is_on_the_map(game_map):
                continue
            yield current
    return iterator


# For equivalent code, see the commented section
down_left = traverse_side(Vector(0, 1), Vector(-1, -1))
down_right = traverse_side(Vector(-1, 0), Vector(1, -1))
up_right = traverse_side(Vector(0, -1), Vector(1, 1))
up_left = traverse_side(Vector(1, 0), Vector(-1, 1))


# def down_left(center, distance):
#     """start at the top and go down to the left
#     but stop before the far left point.
#
#     Each point this yields is exactly distance away form center.
#     The length of this side of the diamond is distance"""
#     start = center + Vector(0, distance)
#     for i in range(distance):
#         current = start + Vector(-i, -i)
#         if not current.is_on_the_map(game_map):
#             continue
#         yield current
#
# def down_right(center, distance):
#     """start at the far left and go down to the right
#     but stop before the bottom point."""
#     start = center + Vector(-distance, 0)
#     for i in range(distance):
#         current = start + Vector(i, -i)
#         if not current.is_on_the_map(game_map):
#             continue
#         yield current
#
# def up_right(center, distance):
#     """start at the bottom and go up to the right
#     but stop before the far right point."""
#     start = center + Vector(0,-distance)
#     for i in range(distance):
#         current = start + Vector(i, i)
#         if not current.is_on_the_map(game_map):
#             continue
#         yield current
#
# def up_left(center, distance):
#     """start at the far right and go up to the left
#     but stop before the top point."""
#     start = center + Vector(distance, 0)
#     for i in range(distance):
#         current = start + Vector(-i, i)
#         if not current.is_on_the_map(game_map):
#             continue
#         yield current


if __name__ == '__main__':
    from time import sleep
    center = Position(70, 70)
    for position in positions_around(center, radius = 4):
        x, y = position.value
        game_map[y][x] = '*'
        game_map.print_centered_at(center, width = 20, height = 20 )
        sleep(.2)