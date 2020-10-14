# This implements two types of loading a saved game:
# One is to load the game state using the pickle module.
# The other is to re-enter the commands of the players.

from input_handling.get_input import get_next_command
import input_handling.set_up_players as plyrs
from input_handling.select_an_object import SelectedObject
from command_handling.insert_commands import insert_command
from command_handling.update_now_and_later_cmds import update_now_and_later_commands
from command_handling.implement_commands import implement_commands_if_possible
from command_handling.commands import EndOfTurnCmd

import game_map as gm_module

import pickle
from copy import deepcopy

decision_both = "both"
decision_re_enter = "re-enter commands"
decision_pickle = "pickle"
decision_abort = "abort"


def load_game_if_user_wants_to():
    print()
    print("Do you want to load a saved game?")
    yes_or_no = input("Type 'y' or 'n' (or 'yes' or 'no'): ").lower()
    if len(yes_or_no) > 0 and yes_or_no[0] == 'y':
        decision = get_type_of_loading_to_do()
        if decision == decision_abort:
            print("Loading game aborted. Nothing was loaded.")
            return
        load_game(decision)
    else:
        print("Okay, no game was loaded.")


def get_type_of_loading_to_do():
    print()
    print("What type of loading do you want, pickle, re-enter commands, or both?")
    print("Type 'p' for pickle, 'r' to re-enter commands, and 'b' for both.")
    print("(Pickle is loading from a .p file.)")
    print("(Loading both ways is for testing purposes.)")
    decision = input("Enter your choice: ").lower()
    if not decision:
        return decision_abort
    elif decision[0] == 'b':
        return decision_both
    elif decision[0] == 'r':
        return decision_re_enter
    elif decision[0] == 'p':
        return decision_pickle
    else:
        return decision_abort


def load_game(type_of_loading_to_do):
    """This loads a game according to three options."""
    file_name = get_name_of_file_to_load()
    if type_of_loading_to_do == decision_both:
        # Then the commands need to be re-entered for a deepcopy of
        # plyrs.players
        players = deepcopy(plyrs.players)
        re_enter_commands(file_name, players)
    if type_of_loading_to_do in (decision_pickle, decision_both):
        load_pickled_file(file_name)
        if type_of_loading_to_do == decision_both:
            compare_two_modes_of_loading(players_copy=players)
        return
    if type_of_loading_to_do == decision_re_enter:
        re_enter_commands(file_name, plyrs.players)
        return
    if type_of_loading_to_do not in (decision_both, decision_pickle,
                                     decision_re_enter):
        print("Developer error! No game was loaded.")


def get_name_of_file_to_load():
    print()
    print("WARNING: This can use the Python pickle module.")
    print("Only load a pickle file if you completely trust it.")
    print("Without using the .p or .txt suffix,")
    file_name = input("enter the name of the file to load: ")
    return 'save_and_load/saved_games/' + file_name


def load_pickled_file(file_name):
    print("Loading from pickle...")
    file_name = file_name + ".p"
    try:
        with open(file_name, "rb") as f:
            players_and_map = pickle.load(f)
            plyrs.players = players_and_map[0]
            gm_module.game_map = players_and_map[1]
            print("Pickled file successfully loaded.")
    except IOError:
        print("The .p file was not found. Loading failed.")
        print("Attempted to open: ")
        print(file_name)


def re_enter_commands(file_name, players):
    print("Re-entering commands...")
    file_name = file_name + ".txt"
    loading_game = True
    resource = 'none'
    # resource is for when setting the default build position of the
    # towncenter, in which case the player is asked what (if any) resource
    # they want a newly built villager to collect.
    try:
        with open(file_name, 'r') as f:
            selected_obj = None
            starting_new_turn = True
            previous_cmd_txt = ''
            for line in f:
                player = get_player(line, players)
                if starting_new_turn:
                    update_now_and_later_commands(player)
                    starting_new_turn = False
                command_txt = get_command_from_line(line)
                if command_txt[:5] == "print":
                    # Then no need to re-enter the print commands.
                    continue
                if is_a_resource_specification(command_txt):
                    # Then the previous command was a set default build position
                    # and was not implemented in the else part below
                    resource = extract_resource_from_command(command_txt)
                    command_obj = get_next_command(player, previous_cmd_txt, selected_obj,
                                                       loading_game, resource)
                    insert_command(player, command_obj)
                else:
                    if is_a_yes_or_no_decision(command_txt):
                        # Ignoring this means this fn load_game is not quite
                        # fully implemented. It will be very rare when it makes a
                        # difference.
                        pass
                        # research_decision = get_decision(command_txt)
                    else:
                        # if command_txt == 'done':
                        #     starting_new_turn = True
                        #     implement_commands_if_possible(player)
                        #     selected_obj = None
                        #     resource = 'none'
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
                        # if command_obj == ['end of turn']:
                        if isinstance(command_obj, EndOfTurnCmd):
                            starting_new_turn = True
                            implement_commands_if_possible(player)
                            selected_obj = None
                            resource = 'none'
                            continue
                        insert_command(player, command_obj)
        print("Commands successfully re-entered.")
    except IOError:
        print("The .txt file was not found. Command to load game by "
              "re-entering commands rejected.")
        print("Attempted to open: ")
        print(file_name)


def get_command_from_line(line):
    # The first four characters of the command are of this form:
    # "P1: "
    # The last character of line is a new line character.
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
        return "yes"
    elif prefix == "No, ":
        return "no"


def get_player_number(line):
    return int(line[1])


def get_player(line, players):
    player_num = get_player_number(line)
    return players[player_num]


def compare_two_modes_of_loading(players_copy):
    """Test if re-entering the commands produces the same state as pickled file."""
    print("Comparing the two modes of loading this saved game...")
    if len(players_copy) != len(plyrs.players):
        print("The number of players doesn't match!!")
        return
    for playerA, playerB in zip(players_copy[1:], plyrs.players[1:]):
        playerA.compare_to(playerB)


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
    assert command == 'done'
