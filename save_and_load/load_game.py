# The first version of this will only re-enter the commands of
# each player. (Hence, if I add randomness to how things are
# executed, then the game loaded won't be exactly what the state
# the game was in when it was saved.)

from input_handling.get_input import get_next_command
from input_handling.set_up_players import players
from input_handling.select_an_object import SelectedObject
from command_handling import insert_command, update_now_and_later_commands
from command_handling import implement_commands_if_possible


def get_name_of_file_to_load():
    file_name = input("Enter the name of the file to load: ")
    return 'save_and_load/saved_games/' + file_name


def get_command_from_line(line):
    return line[4:-1]


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


def get_decision(command):
    prefix = command[:4]
    if prefix == "Yes,":
        return 'yes'
    elif prefix == "No, ":
        return "no"


def get_player_number(line):
    return int(line[1])


def get_player(line):
    player_num = get_player_number(line)
    return players[player_num]


def load_game():
    """This re-enters all the commands saved in a file."""
    resource = 'none'
    # resource is for when setting the default build position of the
    # towncenter, in which case the player is asked what (if any) resource
    # they want a newly built villager to collect.
    loading_game = True
    file_name = get_name_of_file_to_load()
    try:
        with open(file_name, 'r') as f:
            selected_obj = None
            starting_new_turn = True
            previous_cmd_txt = ''
            for line in f:
                player = get_player(line)
                if starting_new_turn:
                    update_now_and_later_commands(player)
                    starting_new_turn = False
                command_txt = get_command_from_line(line)
                if is_a_resource_specification(command_txt):
                    # Then the previous command was a set default build position
                    # and was not implemented in the else part below
                    resource = extract_resource_from_command(command_txt)
                    command_obj = get_next_command(player, previous_cmd_txt, selected_obj,
                                                       loading_game, resource)
                    insert_command(player, command_obj)
                else:
                    if is_a_yes_or_no_decision(command_txt):
                        # Ignoring this means a slight bug
                        # is introduced. It will be very rare when it makes a
                        # difference.
                        pass
                        # research_decision = get_decision(command_txt)
                    else:
                        if command_txt == 'done':
                            starting_new_turn = True
                            implement_commands_if_possible(player)
                            selected_obj = None
                            resource = 'none'
                            continue
                        if command_txt[:3] == 'set':
                            # Then we need to get the resource from the next line
                            # before implementing this command
                            previous_cmd_txt = command_txt
                            continue
                        command_obj = get_next_command(player, command_txt, selected_obj,
                                                       loading_game, resource)
                        if isinstance(command_obj, SelectedObject):
                            selected_obj = command_obj
                            continue
                        if command_obj == ['end of turn']:
                            continue
                        insert_command(player, command_obj)
    except IOError:
        print("File not found. Command to load game rejected.")


def load_game_if_user_wants_to():
    print()
    print("Do you want to load a saved game?")
    yes_or_no = input("Type 'y' or 'n' (or 'yes' or 'no'): ").lower()
    if len(yes_or_no) > 0 and yes_or_no[0] == 'y':
        load_game()
    else:
        print("Okay, no game was loaded.")


if __name__ == '__main__':
    line = "P1: Resource=wood\n"
    command = get_command_from_line(line)
    if is_a_resource_specification(command):
        resource = extract_resource_from_command(command)
    else:
        resource = ''
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

    line = 'P1: done\n'
    command = get_command_from_line(line)
    print(command)
    assert command == 'done'
