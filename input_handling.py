from game_map import Vector


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

unit_kinds_singular = ['villager', 'pikeman', 'swordsman', 'archer', 'knight', 'batteringram',
                       'catapult', 'trebuchet', 'merchant']

unit_kinds = ['villagers', 'pikemen', 'swordsmen', 'archers', 'knights', 'batteringrams',
              'catapults', 'trebuchets', 'merchants']

# In case I change units or unit_kinds and forget to change the other:
assert len(unit_kinds_singular) == len(unit_kinds)

unit_singular_to_plural = dict((s, p) for s, p in zip(unit_kinds_singular, unit_kinds))

unit_kinds_singular = set(unit_kinds_singular)
unit_kinds = set(unit_kinds)
units_plural = unit_kinds

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


def direction_inpt_to_vector(direction_str):
    """direction_str must be a string. Returns a Vector or None.
    In order to not return None, direction_str must be a string of the form
    'D<num>' where D in 'nsew' (north, south, east, west) and <num> is an integer
    possible inputs: 'n5' 'e17' 's12' """
    if not type(direction_str) is str:
        return None
    if len(direction_str) < 2:
        return None
    direction = direction_str[0]
    if direction not in 'nsew':
        return None

    try:
        distance = int(direction_str[1:])
    except ValueError:
        return None

    if direction == 'n':
        return Vector(-1 * distance, 0)
    elif direction == 's':
        return Vector(distance, 0)
    elif direction == 'e':
        return Vector(0, distance)
    else:
        # assert direction == 'w'
        return Vector(0, -1 * distance)


def get_direction_vector(inpt_as_ls):
    """returns None or Vector.

    One thing that is a little odd about this function is that if inpt_as_ls[-2] is a direction in the
    wrong format, this function just ignores it and treats it as if it didn't exist."""
    if len(inpt_as_ls) < 2:
        return None

    delta1 = direction_inpt_to_vector(inpt_as_ls[-1])
    if delta1 is None:
        return None

    delta2 = direction_inpt_to_vector(inpt_as_ls[-2])
    if delta2 is None:
        delta2 = Vector(0, 0)

    return delta1 + delta2


def selected_obj_to_ls_of_units(player, selected_obj):
    """selected_obj must be of the type that the fn select_something returns"""
    if selected_obj is None or len(selected_obj) < 2:
        return []

    ls_of_units = []
    if selected_obj[0] == 'unit':
        # Then selected_obj == ['unit', unit.kind, starting_num, ending_num]
        # The following four lines of code should be unnecessary. I believe it is redundant, assuming that
        # the fn select_something works properly.
        if len(selected_obj) != 4 or selected_obj[1] not in unit_kinds:
            return []
        if not all(type(i) is int for i in selected_obj[2:]):
            return []

        unit_kind = selected_obj[1]
        n1 = selected_obj[2]
        n2 = selected_obj[3]
        for unit in player.units[unit_kind][n1:n2 + 1]:
            if unit.is_alive:
                ls_of_units.append(unit)
        return ls_of_units

    # TODO: implement the rest of this function (when the selected object is an army or a group)
    # I first need to implement the Group and Army classes.
    if selected_obj[0] == 'group':
        pass

    if selected_obj[0] == 'army':
        pass

    return []


def extract_selected_obj(inpt_as_ls):
    """returns the same as the fn select_something"""
    if len(inpt_as_ls) < 3:
        return []

    kind = inpt_as_ls[1]
    not_units = kind not in unit_kinds_singular and kind not in unit_kinds and kind not in {'group', 'army'}
    not_building = kind not in buildings
    if not_units and not_building:
        print("The second word in your command could not be understood.")
        return []

    if kind in unit_kinds:
        # inpt_as_ls[2] should be of the form 'num1-num2'
        num_range = inpt_as_ls[2].split('-')
        try:
            num_range = [int(i) for i in num_range]
        except ValueError:
            return []

        # In case num_range is a list of a single number...
        a = num_range[0]
        b = num_range[-1]

        selected_obj = ['unit', kind, a, b]
    else:
        # Now, inpt_as_ls[2] should be of the form 'num'
        try:
            num = int(inpt_as_ls[2])
        except ValueError:
            return []

    if kind in unit_kinds_singular:
        kind = unit_singular_to_plural[kind]
        selected_obj = ['unit', kind, num, num]

    if kind in {'group', 'army'}:
        selected_obj = [kind, num]

    if kind in buildings:
        selected_obj = ['building', kind, num]

    return selected_obj


########  NOTE: The following several functions have the same arguments so that they can be called
# uniformly via **kwargs.
def build_something(player, inpt_as_ls, selected_obj=None, selected_town_num=1):
    # selected_obj could be the villager(s) which will build the building
    # selected_town_num will be used when building walls.
    # I need to decide on the format of the output
    return ['build']


def select_something(player, inpt_as_ls, selected_obj=None, selected_town_num=1):
    """The point of this function is to return an output selected_obj
    returns [] or a list in one of the following formats:

    ['unit', unit.kind, starting_num, ending_num],  1 <= where starting_num <= ending_num
    or
    ['army', army_num], where 1 <= army_num
    or
    ['group', group_num], where 1 <= group_num
    or
    ['building', building.kind, building_num]
    or
    ['town', town_num]

    Note: The arguments selected_obj and selected_town_num are not used.
    """
    if len(inpt_as_ls) < 2:
        return []

    # Fill in this code

    return []


def move_unit_or_units(player, inpt_as_ls, selected_obj=None, selected_town_num=1):
    """If selected_obj is not None, then it must be in the format of what the
    function select_something returns

    In order for this function to not return [], inpt_as_ls must be of the following type:
    (In what follows, each list may end with one or two entries of <direction string>

    # In the first two cases, selected_obj must be of the type that select_something returns
    ['move', <direction string>], or

    ['move', unit.kind singular, 'unit.number', <direction string>], or
    ['move', unit.kind plural, 'num1-num2', <direction string>], or
    ['move', 'group', 'group_num', <direction string>], or
    ['move', 'army', 'army_num', <direction string>], where
    <direction string> must be formatted such that the fn direction_inpt_to_vector does not
    return None.

    Returns: [] or
    ['move', ls_of_units, delta], where delta is of type Vector
    """
    if len(inpt_as_ls) < 2:
        return []

    delta = get_direction_vector(inpt_as_ls)
    if delta is None:
        return []

    if len(inpt_as_ls) in {2, 3}:
        # Then the player is trying to move selected_obj
        if selected_obj is None or len(selected_obj) < 2:
            return []

        ls_of_units = selected_obj_to_ls_of_units(player, selected_obj)
        if len(ls_of_units) == 0:
            return []
        return ['move', ls_of_units, delta]

    else:  # len(inpt_as_ls) > 3
        selected_obj = extract_selected_obj(inpt_as_ls)
        if selected_obj == []:
            return []

        ls_of_units = selected_obj_to_ls_of_units(player, selected_obj)
        if len(ls_of_units) == 0:
            return []
        return ['move', ls_of_units, delta]


def set_default_build_position(player, inpt_as_ls, selected_obj=None, selected_town_num=1):
    """selected_obj (if not None) must be in the following format:
    ['building', building.kind, building_num]"""
    # I need to decide on the format of the output
    return ['set build position']


def print_something(player, inpt_as_ls, selected_obj=None, selected_town_num=1):
    # I need to decide on the format of the output
    return ['print']


functions = {'build': build_something, 'select': select_something, 'move': move_unit_or_units,
             'set': set_default_build_position, 'print': print_something}

assert set(functions) == main_commands


def input_next_command(player, selected_obj=None, selected_town_num=1):
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

        kwargs = {'player': player, 'inpt_as_ls': inpt_as_ls, 'selected_obj': selected_obj,
                  'selected_town_num': selected_town_num}

        return functions[first_argument_of_command](**kwargs)


if __name__ == '__main__':
    # print(closest_word_to('fnished', possible_first_words))
    # print(closest_word_to('hlp', possible_first_words))
    # print(closest_word_to('pikemen', units))
    # print(closest_word_to('battering', units))
    # print(closest_word_to('treebucket', units))
    # print(closest_word_to('archery', buildings))

    for s in ('nn', 'n14s', '4s', 'j3', 'n'):
        assert direction_inpt_to_vector(s) is None

    # for s in ('n4', 'n10', 's5', 's12', 'e100', 'e0', 'w2', 'w25'):
    #     print(s, direction_inpt_to_vector(s))

    from player import Player
    from game_map import Position

    p1 = Player(1, Position(80, 80), is_human=True)
    a = input_next_command(p1)
    print(a)
