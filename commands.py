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
    # Prior format: ['move', ls_of_units, delta]
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
    # Prior format: ['build unit', building, unit_type, num_to_be_built]
    # building was an instance of Building
    # unit_type was a string in unit_kinds from units.py
    pass


class BuildBuildingCmd(Command):
    # Prior format: ['build building', ls_of_villagers, building_class,
    #             position, this_is_a_help_build_command]
    # position was an instance of Position
    # this_is_a_help_build_command was a bool
    pass


class ResearchCmd(Command):
    # Prior format: ['research', building, thing_to_be_researched]
    # building was an instance of Building
    # thing_to_be_researched was an instance of a subclass of ResearchObject
    pass


class CollectResourceCmd(Command):
    # Prior format: ['collect resource', resource, ls_of_villagers]
    # resource was one of the classes Food, Gold, Stone, etc.
    pass


class FarmCmd(Command):
    # Prior format: ['farm', farm, ls_of_villagers]
    # farm was an instance of Farm
    pass


class EndOfTurnCmd(Command):
    # Prior format: ['end of turn']
    pass
