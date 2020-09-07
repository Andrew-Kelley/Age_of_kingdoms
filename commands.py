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

from units import Unit, unit_kinds, Villager
from buildings.bldng_class import Building
from game_map import Vector, Position
from research_classes import ResearchObject
from resources import Resource

from inspect import isclass


class Command:
    # The following should always be overridden by subclasses
    kind = 'a command'
    __is_initialized = False

    @property
    def is_initialized(self):
        return self.__is_initialized


class MoveCmd(Command):
    # Prior format: ['move', ls_of_units, delta]
    # But I want to eventually allow multiple units to be commanded to move
    # to a given position (instead of saying all should move by te same
    # delta). Hence each unit should have its own delta.

    kind = 'move'

    def __init__(self):
        self.__unit_delta_pairs = []
        # As this is guaranteed to run when a MoveCmd instance is created,
        # I will instead set self.__is_initialized to True if at least
        # one (unit, delta) pair has been successfully added.

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
        self.__is_initialized = True

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
    __building = None
    __unit_kind = None
    __num_to_build = None

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
        self.__building = building
        self.__unit_kind = unit_kind
        self.__num_to_build = num_to_be_built
        self.__is_initialized = True

    @property
    def building(self):
        return self.__building

    @property
    def unit_kind(self):
        return self.__unit_kind

    @property
    def num_to_build(self):
        return self.__num_to_build




class BuildBuildingCmd(Command):
    # Prior format: ['build building', ls_of_villagers, building_class,
    #             position, this_is_a_help_build_command]
    # position was an instance of Position
    # this_is_a_help_build_command was a bool

    kind = 'build building'
    __building_class = None
    __position = None
    __is_a_help_build_cmd = None

    def __init__(self, villagers, building_class, position, is_a_help_build_cmd):
        message = "Error. Developer message: BuildBuildingCmd.__init__ was called,"
        for v in villagers:
            if not isinstance(v, Villager):
                print(message)
                print("and some element of villagers was not a villager.")
                return
        if not isclass(building_class):
            print(message)
            print("and building_class was not a class.")
            return
        if not issubclass(building_class, Building):
            print(message)
            print("and building_class was not a subclass of Building.")
            return
        if not isinstance(position, Position):
            print(message)
            print("and position was not an instance of Position.")
            return
        def is_bool(obj):
            return obj is False or obj is True
        if not is_bool(is_a_help_build_cmd):
            print(message)
            print("and is_a_help_build_cmd was not a bool.")
            return

        self.__building_class = building_class
        self.__position = position
        self.__is_a_help_build_cmd = is_a_help_build_cmd
        self.__is_initialized = True

    @property
    def building_class(self):
        return self.__building_class

    @property
    def position(self):
        return self.__position

    @property
    def is_a_help_build_cmd(self):
        return self.__is_a_help_build_cmd



class ResearchCmd(Command):
    # Prior format: ['research', building, thing_to_be_researched]
    # building was an instance of Building
    # thing_to_be_researched was an instance of a subclass of ResearchObject

    kind = 'research'
    __building = None
    __thing_to_be_researched = None

    def __init__(self, building, thing_to_be_researched):
        message = "Error. Developer message: ResearchCmd.__init__ was called,"
        if not isinstance(building, Building):
            print(message)
            print("but building was not an instance of Building.")
            return
        if not isinstance(thing_to_be_researched, ResearchObject):
            print(message)
            print("but thing_to_be_researched was not an instance of")
            print("ResearchObject.")
            return
        self.__building = building
        self.__thing_to_be_researched = thing_to_be_researched
        self.__is_initialized = True

    @property
    def building(self):
        return self.__building

    @property
    def thing_to_be_researched(self):
        return self.__thing_to_be_researched


class CollectResourceCmd(Command):
    # Prior format: ['collect resource', resource, ls_of_villagers]
    # resource was one of the classes Food, Gold, Stone, etc.

    kind = 'collect resource'
    __resource = None
    __villagers = tuple()

    def __init__(self, resource, villagers):
        message = "Error. Developer message: CollectResourceCmd.__init__ was called,"
        for v in villagers:
            if not isinstance(v, Villager):
                print(message)
                print("and some element of villagers was not a villager.")
                return
        if not isinstance(resource, Resource):
            print(message)
            print("and resource was not an instance of Resource.")
            return

        self.__resource = resource
        self.__villagers = []
        for villager in villagers:
            self.__villagers.append(villager)
        self.__is_initialized = True

    @property
    def resource(self):
        return self.__resource

    def villagers(self):
        for villager in self.__villagers:
            yield villager


class FarmCmd(Command):
    # Prior format: ['farm', farm, ls_of_villagers]
    # farm was an instance of Farm

    kind = 'farm'


class EndOfTurnCmd(Command):
    # Prior format: ['end of turn']

    kind = 'end of turn'


if __name__ == '__main__':
    obj = BuildUnitCmd(1, 2, 3)
    print(obj.building)
