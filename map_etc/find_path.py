from heapq import heappush, heappop


def distance(position1, position2):
    difference = position1 - position2
    return difference.magnitude


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


class FindPath:
    def __init__(self, start, goal):
        self.frontier = []  # a heap implementation of a min priority queue
        self.start = start
        self.goal = goal
        self.end = start # To be changed by find_path
        self.came_from = dict()
        self.came_from[start] = None

    def push(self, position):
        heappush(self.frontier, (distance(position, self.goal),
                diagonal_weight(position, self.goal), position))

    def found_goal(self):
        return self.goal in self.came_from

    def find_path(self):
        """A greedy best-first search."""
        counter = 0
        while not is_empty(self.frontier):
            counter += 1
            if counter > 10**5:
                print("OOPS!")
                print("This was probably an infinite loop.")
                return

            current = heappop(self.frontier)[2]

            if self.found_goal():
                return

            # TODO: FIX REFERENCE TO NEIGHBORS!!!
            for next_position in current.neighbors():
                if next_position not in self.came_from:
                    self.push(next_position)
                    self.came_from[next_position] = current
                    if distance(next_position, self.goal) < distance(self.end, self.goal):
                        self.end = next_position

    def return_path(self):
        path = [self.end]
        current = self.end
        while current != self.start:
            path.append(self.came_from[current])
            current = self.came_from[current]
        return list(reversed(path))
