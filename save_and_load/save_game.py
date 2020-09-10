# My first implementation of saving a game will only save the
# commands that each player enters. (And as of now, all players
# are human.)

# TODO: These also need to be edited:
# - the set_default_build_position fn in input_handling/build.py
# - the research_something fn in input_handling/research.py

from datetime import datetime


def replace_with(string, index, replacement):
    """replace character at index with replacement string"""
    return string[:index] + replacement + string[index+1:]


def get_name_of_file():
    """The name of the file is based solely on the current date and time."""
    date = str(datetime.today())

    colon_index = date.index(':')
    date = replace_with(date, colon_index, 'hr')

    colon_index = date.index(':')
    date = replace_with(date, colon_index, 'min')

    date = date.replace(' ', '_')
    period_index = date.index('.')
    return "saved_at_" + date[:period_index] + "sec.txt"
    # When I first wrote this function, I had it ask the user for the
    # name of the file.
    # while True:
    #     inpt = input("Enter the name of the file you'd like to save the game as: ")
    #     if inpt == '':
    #         continue
    #     if len(inpt) < 4:
    #         print("Your file name is too short.")
    #         continue
    #     if inpt[-4:] != '.txt':
    #         print("Your file name must end in .txt")
    #         continue
    #     if ' ' in inpt:
    #         print("You cannot contain spaces in the file name.")
    #         continue
    #
    #     return inpt


def still_saving_given(indexes, players):
    """Checks value of indexes to see if saving is still in progress."""
    for player in players:
        if player is None:
            continue
        if indexes[player.number] < len(player._commands_history):
            return True
    return False


def prefix(player):
    return 'P' + str(player.number) + ': '


file_first_part = 'save_and_load/saved_games/'


def save_game(players):
    file_name = get_name_of_file()
    indexes = [0] * len(players)
    file_name = file_first_part + file_name
    with open(file_name, 'w') as f:
        while True:
            for player_num, player in enumerate(players):
                if player_num == 0:
                    # Then so-called player is None
                    continue
                while True:
                    if indexes[player_num] >= len(player._commands_history):
                        break
                    cmd = player._commands_history[indexes[player_num]]
                    indexes[player_num] += 1
                    f.write(prefix(player) + cmd + '\n')
                    if cmd == 'done':
                        break

            if not still_saving_given(indexes, players):
                print('Game successfully saved.')
                return
