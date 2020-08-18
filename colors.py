# To be able to print colors in the terminal in both Mac (and Linux) and Windows,
# I found this answer:
# https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python
# The answer I chose is to use the package colorama:
# https://pypi.org/project/colorama/
from colorama import init
init()

class Color:
    MAGENTA = '\033[95m'
    DARK_BLUE = '\033[94m'
    GREEN = '\033[92m'
    LIGHT_YELLOW = '\033[93m'
    GOLD = '\033[33m'
    LIGHT_BLUE = '\033[96m'
    RED = '\033[91m'

    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    ENDC = '\033[0m'



if __name__ == '__main__':
    print(Color.LIGHT_BLUE + "light blue" + Color.ENDC)
    print(Color.DARK_BLUE + "blue" + Color.ENDC)
    print(Color.UNDERLINE + Color.RED + "R" + Color.ENDC)
    print(Color.BOLD + Color.DARK_BLUE + "blue" + Color.ENDC)
    print("Is color back to normal now?")