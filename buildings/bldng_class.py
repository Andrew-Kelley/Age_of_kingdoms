# To see which files contain which buildings, see directory_structure.txt

class Building:
    # Have a method to handle when a building is being attacked. Also have a method to handle building
    # destruction.
    # Perhaps have a method to handle
    # the buildings which are defensible (i.e. which shoot arrows at attackers if there are units garrisoned
    # in it.
    def __init__(self, number, position):
        """For each player, the first of each building is numbered 1.
        Further buildings built (of the same type) are consecutively numbered."""
        self.number = number
        self.position = position

    def can_build(self, position, game_map):
        i_init, j_init = position
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
        i_init, j_init = position
        i_final = i_init - self.size[0]
        j_final = j_init + self.size[1]
        for i in range(i_init, i_final, -1):
            for j in range(j_init, j_final):
                game_map[i][j] = self.letter_abbreviation
                # player.map[i][j] = self.letter_abbreviation
