def input_number_of_players(human=True):
    if human:
        min_number = 1
        text = 'human'
        max_number = 2
    else:
        min_number = 0
        text = 'computer'
        max_number = 7
    while True:
        num_players = input('How many {} players are there? '.format(text))
        try:
            num_players = int(num_players)
            if min_number <= num_players <= max_number:
                return num_players
            else:
                print("""Only {0} to {1} {2} players can play at the same time. 
                Enter a number from {0} to {1}.""".format(min_number, max_number, text))
        except ValueError:
            print('Please enter a numeral (such as 1 or 2).')


done_with_turn = {'finished', 'done'}
help_commands = {'help', 'commands'}
# NOTE: If main_commands is changed, then so should the functions dictionary, defined just before
# the input_next_command function.
main_commands = {'build', 'select', 'move', 'print', 'set'}
possible_first_words = main_commands.union(done_with_turn).union(help_commands)

units = {'villager', 'pikeman', 'swordsman', 'archer', 'knight', 'batteringram',
         'catapult', 'trebuchet', 'merchant'}

buildings = {'towncenter', 'house', 'farm', 'lumbercamp', 'stonequarry', 'miningcamp', 'woodwall',
             'stonewall', 'wallfortification', 'tower', 'castle', 'barracks', 'archeryrange',
             'stable', 'siegeworks', 'blacksmith', 'library', 'market'}

# For building names that really are two words, I would like to be able to handle a space between those words
building_first_words = {'town', 'lumber', 'stone', 'mining', 'wood', 'archery', 'siege'}


def closest_word_to(word, some_words):
    """This function is not perfect, but it should work well enough."""
    closest = ''
    distance = len(word)
    for target in some_words:
        this_distance = len(set(target) - set(word))
        if this_distance < distance:
            distance = this_distance
            closest = target
    return closest


def help():
    # TODO: Fill this in better as I update what possible commands a user can input
    # Instead of the following, I should describe a use case for each possible first word
    print()
    print("Set of possible first words for a command:")
    print(possible_first_words)
    while True:
        print()
        print("To exit this help mode type 'exit' (without the quotes).")
        inpt = input('Which possible first word would you like a description for? ').lower()
        if inpt == 'exit':
            return
        print()
        if inpt in {'finished', 'done'}:
            print("'{}': ".format(inpt), end='')
            print("After exiting this help mode, if you are done with your turn, type 'done' or 'finished'.")
        else:
            print('Uh, sorry, as it turns out, this help mode cannot yet describe most of the words.')
            print("Type 'exit' to leave this not-very-helpful help mode.")

########  NOTE: The following several functions have the same arguments so that they can be called
# uniformly via **kwargs.

def build_something(player, inpt_as_ls, selected_obj=None, selected_town_number=1):
    # selected_obj could be the villager(s) which will build the building
    # selected_town_num will be used when building walls.
    # I need to decide on the format of the output
    return ['build']


def select_something(player, inpt_as_ls, selected_obj=None, selected_town_number=1):
    """returns [] or a list in one of the following formats:

    ['unit', unit.kind, starting_num, ending_num], where starting_num <= ending_num
    or
    ['army', ls_of_army_members],
    or
    ['group', ls_of_group_members],
    or
    ['building', building.kind, building_num]
    or
    ['town', town_number]"""
    if len(inpt_as_ls) < 2:
        return []

    # Fill in this code

    return []


def move_unit_or_units(player, inpt_as_ls, selected_obj=None, selected_town_number=1):
    """If selected_obj is not None, then it must be in the format of what the
    function select_something returns"""
    # I need to decide on the format of the output
    return ['move']


def set_default_build_position(player, inpt_as_ls, selected_obj=None, selected_town_number=1):
    """selected_obj (if not None) must be in the following format:
    ['building', building.kind, building_num]"""
    # I need to decide on the format of the output
    return ['set build position']


def print_something(player, inpt_as_ls, selected_obj=None, selected_town_number=1):
    # I need to decide on the format of the output
    return ['print']

functions = {'build':build_something, 'select':select_something, 'move':move_unit_or_units,
             'set':set_default_build_position, 'print':print_something}

assert set(functions) == main_commands

def input_next_command(player, selected_obj=None, selected_town_number=1):
    if selected_obj is None:
        selected_obj = []
    while True:
        inpt = input('Enter a command: ').lower()
        if inpt == '':
            continue
        inpt_as_ls = inpt.split()

        if inpt_as_ls[0] not in possible_first_words:
            print('The first word of your command did not make perfect sense.')
            guess = closest_word_to(inpt_as_ls[0], possible_first_words)
            yes_or_no = input("Is the first word of your command supposed to be '{}'? [y/n?]".format(guess))
            if len(yes_or_no) > 0 and yes_or_no[0].lower() == 'y':
                inpt_as_ls[0] = guess
            else:
                print("Ok, please type your entire command again.", end=' ')
                print("For help, type 'help' (without the quote marks).")
                continue

        first_argument_of_command = inpt_as_ls[0]


        if first_argument_of_command == '':
            # This can only happen if the function closest_word_to is called and returns ''
            continue

        assert first_argument_of_command in possible_first_words

        if first_argument_of_command in done_with_turn:
            return ['end of turn']
        elif first_argument_of_command in help_commands:
            help()
            continue

        kwargs = {'player':player, 'inpt_as_ls':inpt_as_ls, 'selected_obj':selected_obj,
                  'selected_town_number':selected_town_number}

        return functions[first_argument_of_command](**kwargs)

        # if first_argument_of_command == 'build':
        #     build_something(player, inpt_as_ls, selected_town_number)
        # elif first_argument_of_command == 'select':
        #     # I can't just call the function, I'll need to have a variable which somehow 'selects' the desired
        #     # unit or units or building.
        #     selected_obj = select_something(player, inpt_as_ls, selected_town_number)
        #     if len(selected_obj) > 0 and selected_obj[0] == 'town':
        #         selected_town_number = selected_obj[1]
        # elif first_argument_of_command == 'move':
        #     if selected_obj:
        #         move_unit_or_units(player, inpt_as_ls, selected_obj)
        #     else:
        #         move_unit_or_units(player, inpt_as_ls)
        # elif first_argument_of_command == 'set':
        #     # To set a default build position for a unit-producing building, the player must first select
        #     # the building.
        #     set_default_build_position(player, inpt_as_ls, selected_obj)
        # elif first_argument_of_command == 'print':
        #     print_something(player, inpt_as_ls)
        #


if __name__ == '__main__':
    print(closest_word_to('fnished', possible_first_words))
    print(closest_word_to('hlp', possible_first_words))
    print(closest_word_to('pikemen', units))
    print(closest_word_to('battering', units))
    print(closest_word_to('treebucket', units))
    print(closest_word_to('archery', buildings))

    from player import Player
    from game_map import Position

    p1 = Player(1, Position(80, 80), is_human=True)
    a = input_next_command(p1)
    print(a)
