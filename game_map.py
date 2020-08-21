from resources import Wood, Stone, Food, Gold, Bronze, Iron


class Position:
    """The i and j coordinates of a position on the map"""

    def __init__(self, i, j):
        self.value = (i, j)

    def __eq__(self, other):
        return self.value == other.value

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

    def __eq__(self, other):
        coord0_matches = self.value[0] == other.value[0]
        coord1_matches = self.value[1] == other.value[1]
        return  coord0_matches and coord1_matches

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


# One reason I see now for why I want this class for representing the map
# is that given a position object, I can use it directly to find what is at
# that position, rather than re-implementing the code in __call__ every time.
class GameMap(list):
    def __call__(self, position):
        i, j = position.value
        return self[i][j]

    def __str__(self):
        rows = [''.join(map(str, ls)) for ls in self]
        return '\n'.join(rows)

    def print_centered_at(self, position, width=100, height=24):

        # The following is used to print the same number of digits when
        # printing row or column numbers:
        num_digits = 2 if len(self) <= 100 else 3
        def int_to_str(i):
            """Returns the i as a string with num_digits digits if i % 5 == 0.

            Otherwise this returns num_digits spaces"""
            if i % 5 == 0:
                return str(i).zfill(num_digits)
            else:
                return ' ' * num_digits

        if not position.is_on_the_map(self):
            print('You must choose a position that is on the map.')
            return

        horizontal_delta = width // 2
        vertical_delta = height // 2

        i0, j0 = position.value

        i_start = max(0, i0 - vertical_delta)
        i_stop = min(len(self), i0 + vertical_delta)

        j_start = max(0, j0 - horizontal_delta)
        j_stop = min(len(self[0]), j0 + horizontal_delta)

        def print_column_numbers():
            for digit in range(num_digits):
                # The following line is to print an offset for the margin, which
                # (in the main part) is used to print the row numbers.
                print(' ' * num_digits, end='')
                for j in range(j_start, j_stop):
                    end = '' if j < j_stop - 1 else '\n'
                    print(int_to_str(j)[digit], end=end)


        def print_row(i):
            margin = int_to_str(i)
            row_content = ''.join(map(str, self[i][j_start:j_stop]))
            print(margin + row_content + margin)

        print_column_numbers()
        for i in range(i_start, i_stop):
            print_row(i)
        print_column_numbers()


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

    i0, j0 = position.value

    # The following iterates through the diamond shaped portion of the_map
    # from left to right, bottom to top.
    for j_delta in range(-1 * distance, distance + 1):
        sign = 1 if j_delta <= 0 else -1
        height = distance + j_delta * sign
        # height is how far up or down the map, we need to go
        for i_delta in range(-1 * height, height + 1):
            i = i0 + i_delta
            j = j0 + j_delta
            this_position = Position(i, j)
            if this_position.is_on_the_map(the_map):
                # the_map[i][j] = '*'  # This was used for testing purposes only.
                yield the_map[i][j]


def within_given_distance(obj1, obj2, distance):
    vector = obj1.position - obj2.position
    return vector.magnitude <= distance


# Eventually, I should create a function that makes a random map
game_map = GameMap([[' '] * 100 for i in range(100)])
for i in range(60, 66):
    for j in range(75, 85):
        game_map[i][j] = Wood(Position(i, j))

# Eh, I feel like adding more wood:
for i in range(66, 72):
    for j in range(80, 90):
        game_map[i][j] = Wood(Position(i, j))

# Filling the top left corner with wood:
for i in range(30):
    for j in range(30 - i):
        game_map[i][j] = Wood(Position(i, j))

# Filling the bottom left corner with wood:
for i in range(80, 100):
    for j in range(i - 80):
        game_map[i][j] = Wood(Position(i, j))

# Filling the top right corner with wood:
for i in range(30):
    for j in range(70 + i, 100):
        game_map[i][j] = Wood(Position(i, j))

# Filling the bottom right corner with wood:
for i in range(80, 100):
    for j in range(179 - i, 100):
        game_map[i][j] = Wood(Position(i, j))

# Fill the middle with stone:
for i in range(40, 60):
    for j in range(40, 60):
        game_map[i][j] = Stone(Position(i, j))

# Put gold around the corners of the large stone deposit:
for i_offset, j_offset in ((-15, -15), (-15, 10), (10, -15), (10, 10)):
    for i in range(50 + i_offset, 50 + i_offset + 5):
        for j in range(50 + j_offset, 50 + j_offset + 5):
            game_map[i][j] = Gold(Position(i, j))

# Adding Food:
for i_start, j_start in ((80, 80), (80, 20), (20, 80), (20, 20)):
    for i in range(i_start, i_start + 4):
        for j in range(j_start - 7, j_start - 4):
            game_map[i][j] = Food(Position(i, j))


for i_start, j_start in ((85, 70), (85, 10), (5, 70), (15, 25)):
    for i in range(i_start, i_start + 2):
        for j in range(j_start, j_start + 2):
            game_map[i][j] = Bronze(Position(i, j))

for i in range(90, 92):
    game_map[i][87] = Gold(Position(i, 87))

for i in range(94, 97):
    for j in range(77, 79):
        game_map[i][j] = Stone(Position(i, j))

# The following can be printed, even though it is in the far right column of the map:
game_map[50][99] = Iron(Position(50, 99))

# Adding some Iron at the bottom of the map (which now can be printed):
for i in range(97, 100):
    for j in range(60, 61):
        game_map[i][j] = Iron(Position(i, j))



if __name__ == '__main__':
    for tpl in ((60, 75), (62, 78), (64, 84), (50, 50)):
        position = Position(*tpl)
        print(position, game_map(position))

    # print(game_map)
    # print('-------------------------------------------------------------------')
    # game_map.print_centered_at(Position(50, 60))
    # print('-------------------------------------------------------------------')
    # game_map.print_centered_at(Position(90, 50))
    # print_map(game_map)
    # The following code was run for various values of distance and Position(i, j):
    # When it was run, the code within the function everything_within_given_distance_on
    # was uncommented so that the map was modified.
    # for i in everything_within_given_distance_on(game_map, 20, Position(5, 92)):
    #     pass
    # print_map(game_map)

    # pos1 = Position(5, 6)
    # vec1 = Vector(2, -1)
    # print(pos1 - vec1)
    # print(vec1.magnitude)


    if len(game_map) == 100 and len(game_map[0]) == 100:
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

    v1 = Vector(1, 2)
    v2 = Vector(1, 2)

    assert v1 == v2
    v3 = Vector(2, 1)
    assert v1 != v3
