class Position:
    """The i and j coordinates of a position on the map"""
    def __init__(self, i, j):
        self.value = (i, j)

    def __add__(self, other):
        """Intended use: self is a Position and other is a Vector."""
        i = self.value[0] + other.value[0]
        j = self.value[1] + other.value[1]
        return Position(i, j)

    def __sub__(self, other):
        """Intended use: self is a Position and other is a Position."""
        i = self.value[0] - other.value[0]
        j = self.value[1] - other.value[1]
        return Vector(i, j)

    def __repr__(self):
        return str(self.value)

    def is_on_the_map(self, the_map):
        if self.value[0] < 0 or self.value[1] < 0:
            return False
        if self.value[0] >= len(the_map) or self.value[1] >= len(the_map[0]):
            return False
        return True

class Vector(Position):
    @property
    def magnitude(self):
        return abs(self.value[0]) + abs(self.value[1])


# Eventually, I should create a function that makes a random map
game_map  = [[' '] * 100 for i in range(100)]
for i in range(60, 66):
    for j in range(75, 85):
        game_map[i][j] = 'w'

# Eh, I feel like adding more wood:
for i in range(66, 72):
    for j in range(80, 90):
        game_map[i][j] = 'w'

# For larger maps, this function should really only print part of the map (which would need to be specified).
def print_map(some_map):
    for ls in game_map:
        print(''.join(ls))


if __name__ == '__main__':
    pos1 = Position(5, 6)
    vec1 = Vector(2, -1)
    print(pos1 - vec1)
    print(vec1.magnitude)

    for tpl in ((-1, 5), (100, 20), (90, 100), (120, 200)):
        position = Position(*tpl)
        assert not position.is_on_the_map(game_map)
