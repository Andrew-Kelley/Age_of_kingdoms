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
# - give (or trade?) a resource with another player
# - quit game
# - save game (hopefully, at some point)

# Also, having commands structured in this way will probably be
# helpful when creating an AI.

from units import Unit, unit_kinds
from buildings.bldng_class import Building
from game_map import Vector


class Command:
    # The following should always be overridden by subclasses
    kind = 'a command'


class MoveCmd(Command):
    # Prior format: ['move', ls_of_units, delta]
    # But I want to eventually allow multiple units to be commanded to move
    # to a given position (instead of saying all should move by te same
    # delta). Hence each unit should have its own delta.

    kind = 'move'

    def __init__(self):
        self.__unit_delta_pairs = []

    def add_unit_with_delta(self, unit, delta):
        if not isinstance(unit, Unit):
            print("Error. Developer message: MoveCmd.__init__ was called,")
            print("but unit was not an instance of Unit.")
            return
        if not isinstance(delta, Vector):
            print("Error. Developer message: MoveCmd.__init__ was called,")
            print("but delta was not an instance of Vector.")
            return
        self.__unit_delta_pairs.append((unit, delta))

    def units(self):
        for pair in self.__unit_delta_pairs:
            yield pair[0]

    def units_and_deltas(self):
        for pair in self.__unit_delta_pairs:
            yield pair


class BuildUnitCmd(Command):
    # Prior format: ['build unit', building, unit_type, num_to_be_built]
    # building was an instance of Building
    # unit_type was a string in unit_kinds from units.py

    kind = 'build unit'

    def __init__(self, building, unit_kind, num_to_be_built):
        if not isinstance(building, Building):
            print("Error. Developer message: BuildUnitCmd.__init__ was called,")
            print("but building was not an instance of Building.")
            return
        if unit_kind not in unit_kinds:
            print("Error. Developer message: BuildUnitCmd.__init__ was called,")
            print("but unit_kind was not in unit_kinds.")
            return
        if not type(num_to_be_built) is int:
            print("Error. Developer message: BuildUnitCmd.__init__ was called,")
            print("but num_to_be_built was not an int.")
            return
        if num_to_be_built < 1:
            print("Error. Developer message: BuildUnitCmd.__init__ was called,")
            print("but num_to_be_built < 1")
            return
        # if unit_kind not in building.units_which_can_be_built()
        self.building = building
        self.unit_kind = unit_kind
        self.num_to_build = num_to_be_built




class BuildBuildingCmd(Command):
    # Prior format: ['build building', ls_of_villagers, building_class,
    #             position, this_is_a_help_build_command]
    # position was an instance of Position
    # this_is_a_help_build_command was a bool

    kind = 'build building'


class ResearchCmd(Command):
    # Prior format: ['research', building, thing_to_be_researched]
    # building was an instance of Building
    # thing_to_be_researched was an instance of a subclass of ResearchObject

    kind = 'research'


class CollectResourceCmd(Command):
    # Prior format: ['collect resource', resource, ls_of_villagers]
    # resource was one of the classes Food, Gold, Stone, etc.

    kind = 'collect resource'


class FarmCmd(Command):
    # Prior format: ['farm', farm, ls_of_villagers]
    # farm was an instance of Farm

    kind = 'farm'


class EndOfTurnCmd(Command):
    # Prior format: ['end of turn']

    kind = 'end of turn'
