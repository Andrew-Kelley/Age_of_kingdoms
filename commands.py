# Right now, the commands handled by the module command_handling.py
# are just lists. It would be better if they were instead their
# own classes. Then instead of accessing a part of a command through
# a quite arbitrary list index, you'd instead use an (informative)
# attribute name.

# This change should probably work better when I add more
# commands such as to attack or defend or to enter a building
# (to garrison in it).

# Also, having commands structured in this will probably be
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
