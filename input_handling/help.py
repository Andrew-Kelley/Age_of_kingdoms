# The purpose of this module is to implement the help function, which players may
# call during their turn.

# The following is copied from the file input_handling.py
done_with_turn = {'finished', 'done'}
help_commands = {'help', 'commands'}
# NOTE: If main_commands is changed, then so should the functions dictionary, defined
# just before the input_next_command function.
main_commands = {'build', 'select', 'move', 'print', 'set'}
possible_first_words = main_commands.union(done_with_turn).union(help_commands)


def print_finished_command(selected_obj):
    print("After exiting this help mode, if you are done with your turn, type 'done' "
          "or 'finished' (without the quotes).")


def print_select_command(selected_obj):
    print('SELECTING')
    print('You may select a unit or units or building by typing any of the following commands:')
    print('select Villager 2')
    print('select villagers 1-4')
    print('select barracks 1', end='\n\n')

def print_move_command(selected_obj):
    print('MOVEMENT')
    print('You may move a unit north 1 spots and east 3 spots by typing the following command:')
    print('move Villager 1 N5 E3')
    print('or')
    print('move swordsman 7 n5 e3    (which moves Swordsman number 7 in the stated direction.)')
    print('You may move multiple units south 7 spots and west 2 spots by the following command:')
    print('move pikemen 5-20 s7 w2')
    print('or')
    print('move archers 1-15 S7 W2')
    print('ALSO, if you have already selected a unit or units, you may move them by '
          'the following:')
    print('move n7 w5', end='\n\n')

def print_print_command(selected_obj):
    print('PRINTING')
    print('You may print a selected object by the following command:')
    print('print')
    print('You can also print by typing any of the following:')
    print('print villager 3')
    print('print archeryrange 1')

def print_build_command(selected_obj):
    #TODO this function should probably depend on what selected_obj is
    print('Sorry, the help function has not yet included information on the "build" command')

def print_set_command(selected_obj):
    print("The command 'set' is used to set the default build position of "
          "unit-producing buildings.")
    print("To use this command, you must first select an appropriate building "
          "(you have already built)")
    print("by using the 'select' command.")
    print("Once a building is selected, you can set its default build position "
          "by typing the following:")
    print("set default build position s3 e2")
    print('...where the direction is relative to the bottom left corner of the building. '
          'So the above '
          'command sets the default build position of the selected building to the position '
          'south 3 spots'
          "and east 2 spots, from the building's bottom left corner.")

help_functions = {'finished':print_finished_command, 'done':print_finished_command,
                  'select':print_select_command, 'move':print_move_command,
                  'print':print_print_command, 'build':print_build_command,
                  'set':print_set_command}

def help_on(selected_obj):
    # TODO: Fill this in better as I update what possible commands a user can input
    # Instead of the following, I should describe a use case for each possible first word
    print()
    print("Set of possible first words for a command:")
    print(possible_first_words)
    while True:
        print()
        print("To exit this help mode type 'exit' (without the quotes).")
        inpt = input('Which possible command would you like a description for? ').lower()
        if inpt == 'exit':
            return
        print()
        if inpt in help_functions:
            f = help_functions[inpt]
            f(selected_obj)
        else:
            print('Sorry, either the command you requested information on does not exist, '
                  'or the help function does not yet include information on that command.')