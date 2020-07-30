# Age of Kingdoms - A text-based, turn-based strategy game inspired by
# Age of Empires.
# Started July 21, 2018.

from input_handling.handle_input import input_next_command
from input_handling.select_an_object import is_a_selected_obj
from command_handling import insert_command, update_now_and_later_commands
from command_handling import implement_commands_if_possible

from game_map import game_map
from player import Player, initial_position_of_player


print("Starting a game of Age of Kingdoms...")
# n1 = input_number_of_players(human=True)
# n2 = input_number_of_players(human=False)
# Note: for testing purposes, I'll start off with only 1 human player
# (and no computer players).
n1 = 1
n2 = 0
print("Starting a game with {} human player(s) and {} "
      "computer player(s).".format(n1, n2))

# The actual players are listed starting at index 1.
# Thus players[i] == player number i.
players = [None]
for i in range(1, n1+1):
    initial_position = initial_position_of_player(i, game_map)
    players.append(Player(number=i, position=initial_position, is_human=True))
for i in range(n1+1, n1 + n2 + 1):
    initial_position = initial_position_of_player(i, game_map)
    players.append(Player(number=i, position=initial_position, is_human=False))

for player in players[1:]:
    print("Is player number {} human? {}".format(player.number, player.is_human))


turn_number = 0
while True:
    turn_number += 1
    if turn_number > 5000:
        print('The limit of {} turns has been reached. '
              'Game over.'.format(turn_number - 1))
        break

    for player in players[1:]:
        print("It is now Player number {}'s turn".format(player.number))
        print(player.resources)

        # player.messages contains all messages for the player produced
        # while the player's commands are being implemented.
        if player.messages:
            print(player.messages)
            player.messages = ''
        selected_obj = []
        update_now_and_later_commands(player)

        if not player.is_human:
            continue  # Even a rudimentary AI will have to wait quite some time.
        while True:
            command = input_next_command(player, selected_obj)
            if is_a_selected_obj(command):
                selected_obj = command
                continue
            if command == ['end of turn']:
                break
            insert_command(player, command)

    # Every other turn, the order in which the players' commands are
    # implemented is switched.
    if turn_number % 2 == 1:
        player_iterator = players[1:]
    else:
        player_iterator = reversed(players[1:])

    for player in player_iterator:
        implement_commands_if_possible(player)
