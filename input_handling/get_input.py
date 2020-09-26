from input_handling.help import help_on
from input_handling.build import build_something, set_default_build_position
from input_handling.select_an_object import select_something
from input_handling.move_units import move_unit_or_units
from input_handling.print import print_something
from input_handling.collect_resources import collect_resource, farm
from input_handling.research import research_something

from command_handling.commands import SaveGameCmd, EndOfTurnCmd


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
# NOTE: If main_commands is changed, then so should the functions dictionary, defined
# just before the input_next_command function.
main_commands = {'build', 'select', 'move', 'print', 'set', 'collect', 'chop', 'mine',
                 'quarry', 'research', 'help build', 'farm'}
possible_first_words = main_commands.union(done_with_turn).union(help_commands)
possible_first_words.add('save')

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


# The following dictionary of functions are the main functions that the function
# input_next_command uses to delegate its work. These functions all have the same arguments
# so that they can be called uniformly via **kwargs.

functions = {'build': build_something, 'help build': build_something,
             'select': select_something, 'farm': farm,
             'move': move_unit_or_units, 'set': set_default_build_position,
             'print': print_something, 'research': research_something}

# Intended use: 'collect <any resource>', 'chop wood', 'mine gold', 'mine bronze', 'mine iron'
for word in ('collect', 'quarry', 'chop', 'mine'):
    functions[word] = collect_resource

assert set(functions) == main_commands


def input_next_command(player, selected_obj=None):
    while True:
        inpt = input('Enter a command: ').lower()
        if inpt == '':
            continue
        inpt_as_ls = inpt.split()

        if inpt_as_ls[0] not in possible_first_words:
            print('The first word of your command did not make perfect sense.')
            guess = closest_word_to(inpt_as_ls[0], possible_first_words)
            yes_or_no = input("Is the first word of your command supposed "
                              "to be '{}'? [y/n?]".format(guess))
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
            player.log_command('done')
            return EndOfTurnCmd()
        elif first_argument_of_command == 'save':
            if inpt_as_ls[-1] == 'game':
                return SaveGameCmd()
            else:
                print("Command rejected.")
                return
        elif first_argument_of_command in help_commands and len(inpt_as_ls) == 1:
            help_on(selected_obj)
            continue
        elif first_argument_of_command == 'help' and len(inpt_as_ls) > 1 and \
                inpt_as_ls[1] == 'build':
            del inpt_as_ls[0]
            inpt_as_ls[0] = 'help build'
            first_argument_of_command = 'help build'
        elif first_argument_of_command not in main_commands:
            print('Your command was not understood. Please enter another command.')
            continue

        player.log_command(inpt)

        kwargs = {'player': player, 'inpt_as_ls': inpt_as_ls, 'selected_obj': selected_obj}

        return functions[first_argument_of_command](**kwargs)


def get_next_command(player, inpt='', selected_obj=None,
                     loading_game=False, resource='none'):
    """Return the command produced by the given input.

    This function is intended only for testing purposes,
    and for a rudimentary ability to load a saved game
    by re-entering commands (which also happens to be
    for testing purposes)."""
    if not inpt:
        return
    inpt_as_ls = inpt.split()
    if not type(inpt_as_ls) is list or len(inpt_as_ls) == 0:
        return

    first_arg = inpt_as_ls[0]
    if first_arg not in possible_first_words:
        return
    if first_arg in done_with_turn:
        return EndOfTurnCmd()
    elif first_arg == 'help' and len(inpt_as_ls) == 1:
        return
    elif first_arg == 'help' and inpt_as_ls[1] == 'build':
        del inpt_as_ls[0]
        inpt_as_ls[0] = 'help build'
        first_arg = 'help build'
    elif first_arg not in main_commands:
        return

    player.log_command(inpt)

    kwargs = {'player': player, 'inpt_as_ls': inpt_as_ls, 'selected_obj': selected_obj,
              'loading_game': loading_game}
    # The following would only be used if first_arg == 'set'
    kwargs['resource'] = resource
    if first_arg == 'set':
        return set_default_build_position(**kwargs)

    del(kwargs['resource'])

    if first_arg == 'research':
        return research_something(**kwargs)

    del(kwargs['loading_game'])

    return functions[first_arg](**kwargs)


if __name__ == '__main__':
    from units import unit_kinds

    assert closest_word_to('fnished', possible_first_words) == 'finished'
    assert closest_word_to('hlp', possible_first_words) == 'help'
    assert closest_word_to('pikemen', unit_kinds) == 'pikemen'
    assert closest_word_to('battering', unit_kinds) == 'batteringrams'
    assert closest_word_to('treebucket', unit_kinds) == 'trebuchets'


    # from player import Player
    # from game_map import Position
    #
    # p1 = Player(1, Position(80, 80), is_human=True)
    #
    # print(get_next_command(p1, 'move villager 1 n2 e5'))
    # selected_obj = get_next_command(p1, 'select villagers 2-3')
    # print(get_next_command(p1, 'build lumbercamp 67 76', selected_obj))
