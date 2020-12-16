# This is used as a backup, in case the position a unit tries to move
# to is not available and nothing close to the desired position is
# available either.

from collections import deque
from map_etc.position import distance


# breadth first search
def bfs_for_open_spot(unit, game_map, bound_on_search_distance=12):
    """Return Vector or None

    If returning a Vector, this is the smallest vector that unit
    can move by.

    Also, see the comment at the top of the file."""
    queue = deque()
    positions_found = set()
    start_position = unit.position
    queue.append(start_position)
    positions_found.add(start_position)
    while queue:
        position = queue.popleft()
        delta = position - start_position
        if unit.can_move(delta, game_map):
            return delta
        if distance(start_position, position) > bound_on_search_distance:
            return
        for next in position.neighbors(game_map):
            if next not in positions_found:
                positions_found.add(next)
                queue.append(next)


if __name__ == '__main__':
    from map_etc.position import Position

    position = Position(80, 80)
