

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