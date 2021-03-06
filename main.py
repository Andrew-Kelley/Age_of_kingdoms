# Age of Kingdoms - A text-based, turn-based strategy game inspired by
# Age of Empires.
# Started July 21, 2018.

from input_handling.get_input import input_next_command
from input_handling.select_an_object import SelectedObject
from input_handling.set_up_players import initialize_players
# The following line is to reference plyrs.players directly
import input_handling.set_up_players as plyrs
from command_handling.insert_commands import insert_command
from command_handling.update_now_and_later_cmds import update_now_and_later_commands
from command_handling.implement_commands import implement_commands_if_possible
from command_handling.commands import SaveGameCmd, EndOfTurnCmd, QuitGameCmd
from save_and_load.save_game import save_game
from save_and_load.load_game import load_game_if_user_wants_to
import sys


print("Starting a game of Age of Kingdoms...")

initialize_players()

load_game_if_user_wants_to()

players = plyrs.players

max_num_turns = 5000
for turn_number in range(max_num_turns):
    if turn_number >= max_num_turns - 1:
        print('The limit of {} turns has been reached. '
              'Game over.'.format(max_num_turns))
        break

    for player in players[1:]:
        print("It is now Player number {}'s turn".format(player.number))
        print(player.resources)

        player.print_and_clear_messages()
        selected_obj = None
        update_now_and_later_commands(player)

        if not player.is_human:
            continue  # Even a rudimentary AI will have to wait quite some time.
        while True:
            command = input_next_command(player, selected_obj)
            if isinstance(command, SelectedObject):
                selected_obj = command
                continue
            if isinstance(command, EndOfTurnCmd):
                break
            if isinstance(command, QuitGameCmd):
                print("Quitting the game...")
                sys.exit()
            if isinstance(command, SaveGameCmd):
                save_game(players)
                continue
            insert_command(player, command)

    # Every other turn, the order in which the players' commands are
    # implemented is switched.
    if turn_number % 2 == 1:
        player_iterator = players[1:]
    else:
        player_iterator = reversed(players[1:])

    for player in player_iterator:
        implement_commands_if_possible(player)
