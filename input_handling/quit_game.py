from command_handling.commands import QuitGameCmd

# At some point, I may want to double check that the user really wants to quit the game.
# Also, if it is multiplayer, I might want to allow a human player to be controlled by AI
# when they quit.


def quit_game():
    """Maybe add functionality mentioned in the above comment"""
    return QuitGameCmd()