# The first version of this will only re-enter the commands of
# each player. (Hence, if I add randomness to how things are
# executed, then the game loaded won't be exactly what the state
# the game was in when it was saved.)


loading_game = True


def get_name_of_file_to_load():
    file_name = input("Enter the name of the file to load: ")
    return 'save_and_load/saved_games/' + file_name

def load_game():
    global loading_game

    file_name = get_name_of_file_to_load()
    try:
        with open(file_name, 'r') as f:
            for line in f:
                print(line, end='')
            loading_game = False
            print("inside the function: " +str(loading_game))
            print("ok people")

    except IOError:
        loading_game = False
        print("File not found. Command to load game rejected.")


def load_game_if_user_wants_to():
    print()
    print("Do you want to load a game?")
    yes_or_no = input("Type 'y' or 'n' (or 'yes' or 'no'): ").lower()
    if len(yes_or_no) > 0 and yes_or_no[0] == 'y':
        load_game()
    else:
        print("Okay, no game was loaded.")
