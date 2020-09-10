# The first version of this will only re-enter the commands of
# each player. (Hence, if I add randomness to how things are
# executed, then the game loaded won't be exactly what the state
# the game was in when it was saved.)

from input_handling.get_input import get_next_command

# TODO: the following line fails, so fix it!
from main import players

# some global variables for use in loading:
loading_game = True
# the following is used by the set_default_build_position fn in input_handling/build.py
resource = 'none'
# The following is used by the research_something fn in input_handling/research.py
queue_research_decision = 'yes'


def get_name_of_file_to_load():
    file_name = input("Enter the name of the file to load: ")
    return 'save_and_load/saved_games/' + file_name


def get_command_from_line(line):
    return line[4:]


def extract_resource_from_command(command):
    index = command.index('=')
    return command[index+1:]


def is_a_resource_specification(command):
    resource_prefix = "Resource="
    length = len(resource_prefix)
    if command[:length] == resource_prefix:
        return True
    else:
        return False


def is_a_yes_or_no_decision(command):
    if len(command) < 2:
        return False
    prefix = command[:4]
    return prefix in ("Yes,", "No, ")


def set_decision(command):
    global queue_research_decision
    prefix = command[:4]
    if prefix == "Yes,":
        queue_research_decision = 'yes'
    elif prefix == "No, ":
        queue_research_decision = "no"


def load_game():
    global resource
    global queue_research_decision
    file_name = get_name_of_file_to_load()
    try:
        with open(file_name, 'r') as f:
            for line in f:
                command_txt = get_command_from_line(line)
                if is_a_resource_specification(command_txt):
                    resource = extract_resource_from_command(command_txt)
                elif is_a_yes_or_no_decision(command_txt):
                    set_decision(command_txt)
                else:
                    pass
                    # command_obj = get_next_command() #TODO Fill this in
    except IOError:
        print("File not found. Command to load game rejected.")


def load_game_if_user_wants_to():
    global loading_game
    print()
    print("Do you want to load a saved game?")
    yes_or_no = input("Type 'y' or 'n' (or 'yes' or 'no'): ").lower()
    if len(yes_or_no) > 0 and yes_or_no[0] == 'y':
        load_game()
    else:
        print("Okay, no game was loaded.")

    loading_game = False


if __name__ == '__main__':
    line = "P1: Resource=wood"
    command = get_command_from_line(line)
    if is_a_resource_specification(command):
        resource = extract_resource_from_command(command)
    assert resource == 'wood'

    line = "P1: Yes, add to research queue."
    command = get_command_from_line(line)
    assert is_a_yes_or_no_decision(command)

    line = "P2: No, do not add to research queue."
    command = get_command_from_line(line)
    assert is_a_yes_or_no_decision(command)

    line = "P1: select towncenter"
    command = get_command_from_line(line)
    assert not is_a_yes_or_no_decision(command)
