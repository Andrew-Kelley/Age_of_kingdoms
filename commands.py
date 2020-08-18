# Right now, the commands handled by the module command_handling.py
# are just lists. It would be better if they were instead their
# own classes. Then instead of accessing a part of a command through
# a quite arbitrary list index, you'd instead use an (informative)
# attribute name.

# Doing this change would probably be helpful for when I add more
# commands such as follows:
# - attack a building or unit
# - defend an area
# - garrison units in buildings
# - create a named "army" of military units
# - create a named "group" of villagers
# - sell or buy a particular resource at the market

# Also, having commands structured in this way will probably be
# helpful when creating an AI.


class Command:
    pass


class MoveCmd(Command):
    pass


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
