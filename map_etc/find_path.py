from heapq import heappush, heappop

from map_etc.position import distance
from map_etc.make_map import game_map


def diagonal_weight(position1, position2):
    """Weight 2 positions less if they are more diagonal to each other

    The purpose of this is to augment the distance between them with
    a second number so that the greedy best-first search algorithm
    zig zags as it goes from the start to the goal. Without this
    weighted diagonal, the path stays completely vertical as far as
    it can and then stays completely horizontal as far as it can."""
    x = abs(position1[0] - position2[0])
    y = abs(position1[1] - position2[1])
    return max(x, y) - min(x,y)


def is_empty(heap):
    return len(heap) == 0


# A player's unit can walk through positions where the player's
# own units are already.
class FindPath:
    """Used for all units except villagers."""
    def __init__(self, start, goal, player):
        self.player_num = player.number
        self.frontier = []  # a heap implementation of a min priority queue
        self.start = start
        self.goal = goal
        self.end = start # To be changed by find_path
        self.came_from = dict()
        self.came_from[start] = None

        self.find_path()

    def push(self, position):
        heappush(self.frontier, (distance(position, self.goal),
                diagonal_weight(position, self.goal), position))

    def found_goal(self):
        return self.goal in self.came_from

    def find_path(self):
        """A greedy best-first search."""
        counter = 0
        max_num_steps = self.max_num_steps_to_search
        while not is_empty(self.frontier):
            counter += 1
            if counter > max_num_steps:
                return

            current = heappop(self.frontier)[2]

            if self.found_goal():
                return

            for next_position in current.neighbors():
                available = True
                if game_map.has_unit_at(next_position):
                    available = False
                    player_num = self.player_num
                    if player_num != game_map.get_player_num_for_unit_at(next_position):
                        # Then units cannot walk through them
                        continue
                if next_position not in self.came_from:
                    self.push(next_position)
                    self.came_from[next_position] = current
                    if distance(next_position, self.goal) < distance(self.end, self.goal):
                        if available:
                            self.end = next_position

    def return_path(self):
        path = [self.end]
        current = self.end
        while current != self.start:
            path.append(self.came_from[current])
            current = self.came_from[current]
        return list(reversed(path))

    @property
    def max_num_steps_to_search(self):
        """return a limit on how many steps find_path should take"""
        # Right now, this function is largely a hunch on how many steps
        # might be needed. If it takes longer than this, then self.goal
        # likely is not reachable.
        delta = self.goal - self.start
        distance = delta.magnitude
        if distance < 5:
            return 10 + 4 * distance
        if distance < 10:
            return 12 + 3 * distance
        return 22 + 2 * distance

    def end_is_within(self, threshold):
        return distance(self.start, self.end) <= threshold
