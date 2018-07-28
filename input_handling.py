

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
                Enter a number from {0} to {1}.""".format(min_number,max_number,text))
        except ValueError:
            print('Please enter a numeral (such as 1 or 2).')



done_with_turn = {'finished', 'done'}
help_commands = {'help', 'commands'}
possible_first_words = {'select', 'move', 'print', 'set'}.union(done_with_turn).union(help_commands)

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
    #TODO: Fill this in better as I update what possible commands a user can input
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


def input_next_command(player):
    while True:
        inpt = input('Enter a command: ').lower()
        if inpt == '':
            continue
        parts = inpt.split()
        if parts[0] in done_with_turn:
            return

        if parts[0] not in possible_first_words:
            print('The first word of your command did not make perfect sense.')
            guess = closest_word_to(parts[0], possible_first_words)
            yes_or_no = input("Is the first word of your command supposed to be '{}'? [y/n?]".format(guess))
            if len(yes_or_no) > 0 and yes_or_no[0].lower() == 'y':
                parts[0] = guess
            else:
                print("Ok, please type your entire command again.", end=' ')
                print("For help, type 'help' (without the quote marks).")
                continue

        if parts[0] == 'help':
            help()
            continue




if __name__ == '__main__':
    print(closest_word_to('fnished', possible_first_words))
    print(closest_word_to('hlp', possible_first_words))
    print(closest_word_to('pikemen',units))
    print(closest_word_to('battering', units))
    print(closest_word_to('treebucket', units))
    print(closest_word_to('archery', buildings))

    from player import Player
    from game_map import Position
    p1 = Player(1, Position(80, 80), is_human=True)
    a = input_next_command(p1)