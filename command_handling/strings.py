# These string constants are used in saving commands in the internal
# state of the program.

# For a command to be implemented "now", it means that it will be implemented
# at the end of this turn, when all players' commands are implemented.
NOW = "now"
# For a command to be implemented "later", it means that it will be implemented
# at some later turn.
LATER = "later"

# The commands:
BUILD_BUILDING = "build building"
BUILD_UNIT = "build unit"
COLLECT_RESOURCE = "collect resource"
MOVE = "move"
RESEARCH = "research"
FARM = "farm"

END_OF_TURN = "end of turn"
QUIT_GAME = "quit game"
SAVE_GAME = "save game"
