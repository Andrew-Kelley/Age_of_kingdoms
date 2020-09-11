# Age of Kingdoms - A text-based, turn-based strategy game inspired by
# Age of Empires.
# Started July 21, 2018.

from input_handling.get_input import input_next_command
from input_handling.select_an_object import SelectedObject
from input_handling.set_up_players import players, initialize_players
from command_handling import insert_command, update_now_and_later_commands
from command_handling import implement_commands_if_possible
from save_and_load.save_game import save_game
from save_and_load.load_game import load_game_if_user_wants_to


print("Starting a game of Age of Kingdoms...")

initialize_players()

load_game_if_user_wants_to()

max_num_turns = 5000
for turn_number in range(max_num_turns):
    if turn_number >= max_num_turns - 1:
        print('The limit of {} turns has been reached. '
              'Game over.'.format(max_num_turns))
        break

    for player in players[1:]:
        print("It is now Player number {}'s turn".format(player.number))
        print(player.resources)

        # player.messages contains all messages for the player produced
        # while the player's commands are being implemented.
        if player.messages:
            print(player.messages)
            player.messages = ''
        selected_obj = None
        update_now_and_later_commands(player)

        if not player.is_human:
            continue  # Even a rudimentary AI will have to wait quite some time.
        while True:
            command = input_next_command(player, selected_obj)
            if isinstance(command, SelectedObject):
                selected_obj = command
                continue
            if command == ['end of turn']:
                break
            elif command == ['save game']:
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
