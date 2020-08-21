# Right now, the commands handled by the module command_handling.py
# are just lists. It would be better if they were instead their
# own classes. Then instead of accessing a part of a command through
# a quite arbitrary list index, you'd instead use an (informative)
# attribute name. Also, if an instance is created, then that should
# guarantee that the command is proper (with all its attributes
# initialized).

# Doing this change would probably be helpful for when I add more
# commands such as follows:
# - attack a building or unit
# - defend an area
# - garrison units in buildings
# - create a named "army" of military units
# - create a named "group" of villagers
# - sell or buy a particular resource at the market
# - quit game
# - save game (hopefully, at some point)

# Also, having commands structured in this way will probably be
# helpful when creating an AI.

from units import Unit
from game_map import Vector


class Command:
    pass


class MoveCmd(Command):
    # A move command used to be of this form: ['move', ls_of_units, delta]
    # But I want to eventually allow multiple units to be commanded to move
    # to a given position (instead of saying all should move by te same
    # delta). Hence each unit should have its own delta.
    def __init__(self):
        self.__unit_delta_pairs = []

    def add_unit_with_delta(self, unit, delta):
        if not isinstance(unit, Unit):
            return
        if not isinstance(delta, Vector):
            return
        self.__unit_delta_pairs.append((unit, delta))

    def units_iter(self):
        for pair in self.__unit_delta_pairs:
            yield pair[0]

    def units_and_deltas_iter(self):
        for pair in self.__unit_delta_pairs:
            yield pair


class BuildUnitCmd(Command):
    pass


class BuildBuildingCmd(Command):
    pass


class ResearchCmd(Command):
    pass


class CollectResourceCmd(Command):
    pass


class FarmCmd(Command):
    pass


class EndOfTurnCmd(Command):
    pass
