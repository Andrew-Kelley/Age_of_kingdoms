# Instances of Position are supposed to be positions on the map


class Position:
    """The i and j coordinates of a position on the map"""

    def __init__(self, i, j):
        self.value = (i, j)

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __hash__(self):
        return hash(self.value)

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
        x, y = self.value
        if x < 0 or y < 0:
            return False
        if y >= the_map.height or x >= the_map.width:
            return False
        return True

    def neighbors(self, the_map):
        """all adjacent positions on map that are not buildings"""
        Vec = Vector
        for delta in (Vec(0,1), Vec(0,-1), Vec(1, 0), Vec(-1,0)):
            position = self + delta
            if position.is_on_the_map(the_map):
                if not the_map.has_building_at(position):
                    yield position


# A vector is something you can add to a position to get another position

class Vector(Position):
    def __add__(self, other):
        i = self.value[0] + other.value[0]
        j = self.value[1] + other.value[1]
        return Vector(i, j)

    def __mul__(self, n):
        x, y = self.value
        return Vector(x * n, y * n)

    @property
    def magnitude(self):
        return abs(self.value[0]) + abs(self.value[1])

    def beginning_plus_the_rest(self, distance_in_one_turn=15):
        """partitions self into two vectors v1, v2 such that self == v1 + v2
        and v1.magnitude <= 15

        The purpose of this is to be able to move units more than the
        allowable amount per turn.

        returns a tuple: (Vector, Vector)"""
        if self.magnitude <= distance_in_one_turn:
            return (self, Vector(0, 0))

        def special_min(x, other=7):
            """returns x, other, or -1 * other"""
            value = min(other, abs(x))
            if x < 0:
                value *= -1
            return value

        a = distance_in_one_turn // 2
        b = distance_in_one_turn - a
        i0, j0 = self.value
        i = special_min(i0, a)
        j = special_min(j0, b)

        # The following is only ready to be returned if
        # beginning.magnitude == 15 or if beginning == self
        beginning = Vector(i, j)
        the_rest = self - beginning

        max_left = distance_in_one_turn - beginning.magnitude

        i1, j1 = the_rest.value
        i = special_min(i1, max_left)
        j = special_min(j1, max_left)

        beginning += Vector(i, j)
        the_rest -= Vector(i, j)

        return (beginning, the_rest)


def distance(position1, position2):
    difference = position1 - position2
    return difference.magnitude


if __name__ == '__main__':
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

    v1 = Vector(1, 2)
    v2 = Vector(1, 2)

    assert v1 == v2
    v3 = Vector(2, 1)
    assert v1 != v3
