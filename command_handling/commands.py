# When a user inputs a command, it gets translated into an
# instance of a subclass of the Command class.

# Commands to add:
# - attack a building or unit
# - set selected military units' aggression level
# - garrison units in buildings
# - create a named "army" of military units
# - create a named "group" of villagers
# - add selected units to an already existing named "army" or "group"
# - sell or buy a particular resource at the market
# - give (or trade?) a resource with another player

from units.unit_kinds import unit_kinds
from buildings.bldng_class import Building
from buildings.resource_bldngs import Farm
from map_etc.position import Vector, Position
from research_classes import ResearchObject
from resources import Resource
from command_handling.strings import BUILD_BUILDING, BUILD_UNIT
from command_handling.strings import COLLECT_RESOURCE, MOVE, RESEARCH, FARM
from command_handling.strings import END_OF_TURN, QUIT_GAME, SAVE_GAME

from inspect import isclass


class Command:
    # The _kind attribute should always be overridden by subclasses
    _kind = 'a command'
    _is_initialized = False

    @property
    def is_initialized(self):
        return self._is_initialized

    @property
    def kind(self):
        return self._kind


class MoveCmd(Command):
    # Prior format: ['move', ls_of_units, delta]
    # But I want to eventually allow multiple units to be commanded to move
    # to a given position (instead of saying all should move by the same
    # delta). Hence each unit should have its own delta.

    _kind = MOVE

    def __init__(self):
        self._unit_delta_pairs = []
        # As this is guaranteed to run when a MoveCmd instance is created,
        # I will instead set self._is_initialized to True if at least
        # one (unit, delta) pair has been successfully added.

    def add_unit_with_delta(self, unit, delta):
        message = "Error. Developer message: MoveCmd.__init__ was called,"
        # The following line is what I mean in the first if statement.
        # if not isinstance(unit, Unit):
        # I cannot do this because importing from units.py would give a
        # circular import.
        if unit.__class__.__bases__[0].kind != 'units':
            print(message)
            print("but unit was not an instance of Unit.")
            return
        if not isinstance(delta, Vector):
            print(message)
            print("but delta was not an instance of Vector.")
            return
        self._unit_delta_pairs.append((unit, delta))
        self._is_initialized = True

    def units(self):
        for pair in self._unit_delta_pairs:
            yield pair[0]

    def units_and_deltas(self):
        for pair in self._unit_delta_pairs:
            yield pair


class BuildUnitCmd(Command):
    # Prior format: ['build unit', building, unit_type, num_to_be_built]
    # building was an instance of Building
    # unit_type was a string in unit_kinds from units.py

    _kind = BUILD_UNIT
    _building = None
    _unit_kind = None
    _num_to_build = None

    def __init__(self, building, unit_kind, num_to_be_built):
        message = "Error. Developer message: BuildUnitCmd.__init__ was called,"
        if not isinstance(building, Building):
            print(message)
            print("but building was not an instance of Building.")
            return
        if unit_kind not in unit_kinds:
            print(message)
            print("but unit_kind was not in unit_kinds.")
            return
        if not type(num_to_be_built) is int:
            print(message)
            print("but num_to_be_built was not an int.")
            return
        if num_to_be_built < 1:
            print(message)
            print("but num_to_be_built < 1")
            return
        # if unit_kind not in building.units_which_can_be_built()
        self._building = building
        self._unit_kind = unit_kind
        self._num_to_build = num_to_be_built
        self._is_initialized = True

    @property
    def building(self):
        return self._building

    @property
    def unit_kind(self):
        return self._unit_kind

    @property
    def num_to_build(self):
        return self._num_to_build


class BuildBuildingCmd(Command):
    # Prior format: ['build building', ls_of_villagers, building_class,
    #             position, this_is_a_help_build_command]
    # position was an instance of Position
    # this_is_a_help_build_command was a bool

    _kind = BUILD_BUILDING
    _villagers = tuple()
    _building_class = None
    _position = None
    _is_a_help_build_cmd = None

    def __init__(self, villagers, building_class, position, is_a_help_build_cmd):
        # villagers can be any iterator of villagers
        message = "Error. Developer message: BuildBuildingCmd.__init__ was called,"
        villagers = list(villagers)
        for v in villagers:
            # if not isinstance(v, Villager):
            if v.kind != 'villagers':
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
        
        def is_bool(x):
            return x is False or x is True
        
        if not is_bool(is_a_help_build_cmd):
            print(message)
            print("and is_a_help_build_cmd was not a bool.")
            return

        self._villagers = villagers
        self._building_class = building_class
        self._position = position
        self._is_a_help_build_cmd = is_a_help_build_cmd
        self._is_initialized = True

    def villagers(self):
        return self._villagers

    @property
    def building_class(self):
        return self._building_class

    @property
    def position(self):
        return self._position

    @property
    def is_a_help_build_cmd(self):
        return self._is_a_help_build_cmd


class ResearchCmd(Command):
    # Prior format: ['research', building, thing_to_be_researched]
    # building was an instance of Building
    # thing_to_be_researched was an instance of a subclass of ResearchObject

    _kind = RESEARCH
    _building = None
    _thing_to_be_researched = None

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
        self._building = building
        self._thing_to_be_researched = thing_to_be_researched
        self._is_initialized = True

    @property
    def building(self):
        return self._building

    @property
    def thing_to_be_researched(self):
        return self._thing_to_be_researched


class CollectResourceCmd(Command):
    # Prior format: ['collect resource', resource, ls_of_villagers]
    # resource was one of the classes Food, Gold, Stone, etc.

    _kind = COLLECT_RESOURCE
    _resource = None
    _villagers = tuple()

    def __init__(self, resource, villagers):
        message = "Error. Developer message: CollectResourceCmd.__init__ was called,"
        villagers = list(villagers)
        for v in villagers:
            # if not isinstance(v, Villager):
            if v.kind != 'villagers':
                print(message)
                print("and some element of villagers was not a villager.")
                return
        if not issubclass(resource, Resource):
            print(message)
            print("and resource was not an instance of Resource.")
            return

        self._resource = resource
        self._villagers = villagers
        self._is_initialized = True

    @property
    def resource(self):
        return self._resource

    def villagers(self):
        for villager in self._villagers:
            yield villager

    def __str__(self):
        kind = self._kind + " "
        resource = str(self._resource) + " "
        villagers = str(self._villagers)
        return kind + resource + villagers


class FarmCmd(Command):
    # Prior format: ['farm', farm, ls_of_villagers]
    # farm was an instance of Farm

    _kind = FARM
    _farm = None
    _villagers = None

    def __init__(self, farm, villagers):
        message = "Error. Developer message: FarmCmd.__init__ was called,"
        if not isinstance(farm, Farm):
            print(message)
            print("and farm was not an instance of Farm.")
            return
        for v in villagers:
            # if not isinstance(v, Villager):
            if v.kind != 'villagers':
                print(message)
                print("and some element of villagers was not a villager.")
                return
        self._farm = farm
        self._villagers = villagers
        self._is_initialized = True

    def villagers(self):
        for villager in self._villagers:
            yield villager

    @property
    def farm(self):
        return self._farm


class EndOfTurnCmd(Command):
    # Prior format: ['end of turn']
    _kind = END_OF_TURN


class QuitGameCmd(Command):
    _kind = QUIT_GAME


class SaveGameCmd(Command):
    # Prior format: ['save game']
    _kind = SAVE_GAME


if __name__ == '__main__':
    obj = BuildUnitCmd(1, 2, 3)
    print(obj.building)
    print(obj.kind)

    cmd = QuitGameCmd()
    assert isinstance(cmd, Command)
