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

    BACK_GRAY = '\033[47m'

    ENDC = '\033[0m'

    # This was only used to print all colors to find what would be a good background
    # color.
    @classmethod
    def return_color(self, num):
        return '\033[' + str(num) + 'm'



if __name__ == '__main__':
    print(Color.DARK_BLUE + "dark blue" + Color.ENDC)
    print(Color.GREEN + "green" + Color.ENDC)
    print(Color.MAGENTA + "magenta" + Color.ENDC)
    print(Color.UNDERLINE + Color.RED + "R" + Color.ENDC)
    print(Color.LIGHT_BLUE + "light blue" + Color.ENDC)

    print(Color.BOLD + Color.DARK_BLUE + "dark blue bold" + Color.ENDC)
    print(Color.BOLD + Color.LIGHT_BLUE + "light blue bold" + Color.ENDC)
    print("Is color back to normal now?")

    print(Color.BACK_GRAY + "Hello people" + Color.ENDC)

    for color in (Color.DARK_BLUE, Color.GREEN, Color.MAGENTA, Color.RED, Color.LIGHT_BLUE):
        print(Color.BACK_GRAY + color + "some text" + Color.ENDC)

    # for n in range(1, 256):
    #     print(n, Color.return_color(n) + "some text" + Color.ENDC)
