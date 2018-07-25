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

