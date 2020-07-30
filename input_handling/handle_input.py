# The main function this module defines is input_next_command


from input_handling.help import help_on
from input_handling.build import build_something, set_default_build_position
from input_handling.select_an_object import select_something
from input_handling.move_units import move_unit_or_units
from input_handling.print import print_something
from input_handling.collect_resources import collect_resource, farm
from input_handling.research import research_something

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
main_commands = {'build', 'select', 'move', 'print', 'set', 'collect', 'chop', 'mine', 'research',
                 'help build', 'farm'}
possible_first_words = main_commands.union(done_with_turn).union(help_commands)


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



#  The following dictionary of functions are the main functions that the function
# input_next_command uses to delegate its work. These functions all have the same arguments
# so that they can be called uniformly via **kwargs.

functions = {'build': build_something, 'help build':build_something, 'select': select_something,
             'move': move_unit_or_units, 'set': set_default_build_position, 'print': print_something,
             'research':research_something, 'farm':farm}

# Intended use: 'collect <any resource>', 'chop wood', 'mine gold', 'mine bronze', 'mine iron'
for word in ('collect', 'chop', 'mine'):
    functions[word] = collect_resource

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
        elif first_argument_of_command in help_commands and len(inpt_as_ls) == 1:
            help_on(selected_obj)
            continue
        elif first_argument_of_command == 'help' and len(inpt_as_ls) > 1 and inpt_as_ls[1] == 'build':
            del inpt_as_ls[0]
            inpt_as_ls[0] = 'help build'
            first_argument_of_command = 'help build'
        elif first_argument_of_command not in main_commands:
            print('Your command was not understood. Please enter another command.')
            continue

        kwargs = {'player': player, 'inpt_as_ls': inpt_as_ls, 'selected_obj': selected_obj,
                  'selected_town_num': selected_town_num}

        return functions[first_argument_of_command](**kwargs)


if __name__ == '__main__':
    from units import unit_kinds

    assert closest_word_to('fnished', possible_first_words) == 'finished'
    assert closest_word_to('hlp', possible_first_words) == 'help'
    assert closest_word_to('pikemen', unit_kinds) == 'pikemen'
    assert closest_word_to('battering', unit_kinds) == 'batteringrams'
    assert closest_word_to('treebucket', unit_kinds) == 'trebuchets'

    # a = input_next_command(p1)
    # print(a)


