# To see which files contain which buildings, see directory_structure.txt


class Building:
    # Have a method to handle when a building is being attacked. Also have a method to handle building
    # destruction.
    # Perhaps have a method to handle
    # the buildings which are defensible (i.e. which shoot arrows at attackers if there are units garrisoned
    # in it.
    def __init__(self, number, position):
        """For each player, the first of each building is numbered 1.
        Further buildings built (of the same type) are consecutively numbered.

        position is the south-west (i.e. bottom left) corner of the building."""
        self.number = number
        self.position = position
        # The following is only relevant for unit-producing buildings. It sets the default position where units
        # are produced as the south-west corner of the building. Even though such units are technically "in"
        # the building, they are not counted as garrisoned. The reason why I do not want to check if it's possible
        # to build units immediately to the north, south, east, or west, of the building, is I would have to
        # include the game_map as a parameter to the class __init__ function.
        self.build_position = position

    def change_build_position_to(self, new_position, game_map):
        """Only relevant for unit-producing buildings. This function specifies a new position for where units
        built by the building self should begin their existence."""
        delta = new_position - self.position
        if delta.magnitude > 15:
            print("Sorry, the new position must be within 15 of the building's south-west corner.")
            return
            # SHOULD I CHANGE THIS? Should it instead be within 15 of any part of the building?
        if not new_position.is_on_the_map(game_map):
            print("You must pick a position that is on the map.")
            return
        # TODO: Check that there are no enemy walls between the building's position and the proposed build position
        self.build_position = new_position

    def enough_resources_to_build(self, player):
        if player.resources >= self.cost:
            return True
        else:
            return False

    def can_build_on_map(self, position, game_map):
        """Returns True if the building can be built at stated position."""
        i_init, j_init = position.value
        height, length = self.size
        # First check if the building will be placed within the boundaries of the  map:
        if i_init - (height - 1) < 0:
            print('Sorry, building placement too far north.')
            return False
        if i_init >= len(game_map):
            print('Sorry, building placement too far south.')
            return False
        if j_init < 0:
            print('Sorry, building placement too far west.')
            return False
        if j_init + (length - 1) >= len(game_map[0]):
            print('Sorry, building placement too far east.')
            return False

        # Next, check that there are no obstructions. Buildings are allowed to be built only where there are
        # blank spaces or wood or food sources.
        i_final = i_init - self.size[0]
        j_final = j_init + self.size[1]
        for i in range(i_init, i_final, -1):
            for j in range(j_init, j_final):
                if game_map[i][j] not in (' ', 'w', 'f'):
                    print('Sorry, there is {} occupying part of that space.'.format(game_map[i][j]))
                    return False

        return True

    def build(self, player, position, game_map):
        i_init, j_init = position.value
        i_final = i_init - self.size[0]
        j_final = j_init + self.size[1]
        for i in range(i_init, i_final, -1):
            for j in range(j_init, j_final):
                game_map[i][j] = self.letter_abbreviation
                # player.map[i][j] = self.letter_abbreviation
