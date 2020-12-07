from map_etc.position import Position
from map_etc.colors import Color, get_color_from_player_num
from resources import Resource

class GameMap():
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # The following stores buildings and resources
        self.bldngs_n_rsrcs = [[' '] * width for _ in range(height)]

        # If some_unit is a villager, then self.units at position some_unit.position
        # is a set containing some_unit. If some_unit is not a villager, then
        # self.units at position some_unit is just some_unit
        self.units = [[None] * width for _ in range(height)]

    def __call__(self, position, units=False):
        x, y = position.value
        if units:
            return self.units[y][x]
        else:
            return self.bldngs_n_rsrcs[y][x]

    def has_building_at(self, position):
        thing_on_map = self(position)
        # Many spots on map are empty. They are represented by a single space.
        if thing_on_map == ' ':
            return False
        # The only things not strings on the map are resources.
        if not isinstance(thing_on_map, str):
            return False
        return True

    def num_villagers_at(self, position):
        units_on_map = self(position, units=True)
        if isinstance(units_on_map, set):
            return len(units_on_map)
        else:
            return 0

    def has_unit_at(self, position):
        return self(position, units=True) is not None

    def print_centered_at(self, position, width=100, height=24):

        # The following is used to print the same number of digits when
        # printing row or column numbers:
        num_digits = 2 if self.height <= 100 else 3

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

        x0, y0 = position.value

        y_min = max(0, y0 - vertical_delta)
        y_max = min(self.height - 1, y0 + vertical_delta)

        x_start = max(0, x0 - horizontal_delta)
        x_stop = min(self.width, x0 + horizontal_delta)

        def print_column_numbers():
            for digit in range(num_digits):
                # The following line is to print an offset for the margin, which
                # (in the main part) is used to print the row numbers.
                print(' ' * num_digits, end='')
                for x in range(x_start, x_stop):
                    end = '' if x < x_stop - 1 else '\n'
                    print(int_to_str(x)[digit], end=end)

        def print_row(i):
            margin = int_to_str(i)
            row_content = ''.join(self.str_char_at(x, i) for x in range(x_start, x_stop))
            print(margin + row_content + margin)

        print_column_numbers()
        for i in range(y_max, y_min - 1, -1):
            print_row(i)
        print_column_numbers()


    # TODO: this is not finished!
    def str_char_at(self, x, y):
        """return the string character to be printed

        This for what is at Position(x,y) on the map."""
        output = ' '
        position = Position(x, y)
        if self.has_unit_at(position):
            num_villagers = self.num_villagers_at(position)
            if num_villagers == 1:
                return 'v' # TODO: get the color and add it
        else:
            return str(self.bldngs_n_rsrcs[y][x])
