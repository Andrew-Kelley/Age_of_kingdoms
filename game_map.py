from resources import Wood


class Position:
    """The i and j coordinates of a position on the map"""

    def __init__(self, i, j):
        self.value = (i, j)

    def __eq__(self, other):
        return self.value == other.value

    def __add__(self, other):
        """Intended use: self is a Position and other is a Vector."""
        i = self.value[0] + other.value[0]
        j = self.value[1] + other.value[1]
        return Position(i, j)

    def __sub__(self, other):
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
    def __add__(self, other):
        i = self.value[0] + other.value[0]
        j = self.value[1] + other.value[1]
        return Vector(i, j)

    @property
    def magnitude(self):
        return abs(self.value[0]) + abs(self.value[1])

    def beginning_plus_the_rest(self):
        """partitions self into two vectors v1, v2 such that self == v1 + v2
        and v1.magnitude <= 15

        The purpose of this is to be able to move units more than the allowable amount per turn.

        returns a tuple: (Vector, Vector)"""
        if self.magnitude <= 15:
            return (self, Vector(0, 0))

        i0, j0 = self.value
        i = special_min(i0, 7)
        j = special_min(j0, 8)

        # The following is only ready to be returned if beginning.magnitude == 15 or ...
        # ...if beginning == self
        beginning = Vector(i, j)
        the_rest = self - beginning

        max_left = 15 - beginning.magnitude

        i1, j1 = the_rest.value
        i = special_min(i1, max_left)
        j = special_min(j1, max_left)

        beginning += Vector(i, j)
        the_rest -= Vector(i, j)

        return (beginning, the_rest)


def special_min(x, other=7):
    """returns x, other, or -1 * other"""
    value = min(other, abs(x))
    if x < 0:
        value *= -1
    return value


# Eventually, I should create a function that makes a random map
game_map = [[' '] * 100 for i in range(100)]
for i in range(60, 66):
    for j in range(75, 85):
        game_map[i][j] = Wood(Position(i, j))

# Eh, I feel like adding more wood:
for i in range(66, 72):
    for j in range(80, 90):
        game_map[i][j] = Wood(Position(i, j))


# For larger maps, this function should really only print part of the map (which would need to
# be specified).
def print_map(some_map):
    for ls in game_map:
        print(''.join(map(str, ls)))


if __name__ == '__main__':
    print_map(game_map)
    # pos1 = Position(5, 6)
    # vec1 = Vector(2, -1)
    # print(pos1 - vec1)
    # print(vec1.magnitude)

    for tpl in ((-1, 5), (100, 20), (90, 100), (120, 200)):
        position = Position(*tpl)
        assert not position.is_on_the_map(game_map)

    # for tpl in ((20, 0), (0, 20), (30, 10), (10, 8)):
    #     v = Vector(*tpl)
    #     beginning, the_rest = v.beginning_plus_the_rest()
    #     print(v, beginning + the_rest, beginning, the_rest)

    # Testing the method beginning_plus_the_rest
    # wrong = []
    # for i in range(-200, 200):
    #     for j in range(-200, 200):
    #         v = Vector(i, j)
    #         beginning, the_rest = v.beginning_plus_the_rest()
    #         if beginning + the_rest != v:
    #             wrong.append(v)
    #         if beginning != v and beginning.magnitude != 15:
    #             wrong.append(v)
    # print(len(wrong)) #  Great! len(wrong) == 0
    # print(wrong[:5])
