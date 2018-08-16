# The main function this module defines is input_next_command, which is at the bottom of this file.

from game_map import Position, Vector, game_map
from help import help
from units import unit_kinds
from resources import resource_kind_to_class, Wood, Stone, Gold, Bronze, Iron

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
main_commands = {'build', 'select', 'move', 'print', 'set', 'collect', 'chop', 'mine'}
possible_first_words = main_commands.union(done_with_turn).union(help_commands)

unit_kinds_singular = ['villager', 'pikeman', 'swordsman', 'archer', 'knight', 'batteringram',
                       'catapult', 'trebuchet', 'merchant']

# In case I change units or unit_kinds and forget to change the other:
assert len(unit_kinds_singular) == len(unit_kinds)

unit_singular_to_plural = dict((s, p) for s, p in zip(unit_kinds_singular, unit_kinds))

unit_kinds_singular = set(unit_kinds_singular)
unit_kinds = set(unit_kinds)
units_plural = unit_kinds

buildings = {'towncenter', 'house', 'farm', 'lumbercamp', 'stonequarry', 'miningcamp', 'woodwall',
             'stonewall', 'wallfortification', 'tower', 'castle', 'barracks', 'archeryrange',
             'stable', 'siegeworks', 'blacksmith', 'library', 'market'}

# For building names that really are two words, I would like to be able to handle a space between those
# words, but as of now, the code doesn't use the following set:
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


def direction_inpt_to_vector(direction_str):
    """direction_str must be a string. Returns a Vector or None.
    In order to not return None, direction_str must be a string of the form
    'D<num>' where D is in 'nsew' (north, south, east, west) and <num> is an integer
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
        print('The last direction vector input was not understood.')
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
        return []

    if selected_obj[0] == 'army':
        return []

    return []


def selected_obj_to_actual_building(player, selected_obj):
    """In order to not return None, selected_obj must be in the following format:
    ['building', building.kind, building_num]"""
    if len(selected_obj) != 3:
        return
    if selected_obj[0] != 'building':
        return
    kind = selected_obj[1]
    if kind not in buildings:
        return

    building_num = selected_obj[2]
    if not 1 <= building_num < len(player.buildings[kind]):
        print('There is no {} with number {}'.format(kind, building_num))
        return

    return player.buildings[kind][building_num]


def selected_obj_consists_of_villagers(selected_obj):
    if not selected_obj:
        print('You must first select some villager(s) before giving a command to ',
              'collect a resource or build a building.')
        return False

    if not type(selected_obj) is list or len(selected_obj) < 2:
        print('Error: selected_obj is not proper')
        return False

    if not selected_obj[0] in ('unit', 'group'):
        return False

    if selected_obj[0] == 'unit' and not selected_obj[1] == 'villagers':
        print('Only villagers can collect resources. Your selected object was not a ',
              'group of villagers.')
        return False
    return True

def extract_selected_obj(inpt_as_ls):
    """The return format is the same as the fn select_something"""
    if len(inpt_as_ls) < 3:
        return []

    kind = inpt_as_ls[1]
    not_units = kind not in unit_kinds_singular and kind not in unit_kinds and kind not in {'group', 'army'}
    not_building = kind not in buildings
    not_town = kind != 'town'
    if not_units and not_building and not_town:
        print("The second word in your command could not be understood.")
        return []

    if kind in unit_kinds:
        # inpt_as_ls[2] should be of the form 'num1-num2'
        num_range = inpt_as_ls[2].split('-')
        try:
            num_range = [int(i) for i in num_range]
        except ValueError:
            print('The third part of your command could not be understood.', end=' ')
            print("A number range (such as 1-4) was expected.")
            return []

        # In case num_range is a list of a single number...
        a = num_range[0]
        b = num_range[-1]
        if a < 1 or b < a:
            return []

        selected_obj = ['unit', kind, a, b]
        return selected_obj
    else:
        # Now, inpt_as_ls[2] should be of the form 'num'
        try:
            num = int(inpt_as_ls[2])
        except ValueError:
            return []

    if num < 1:
        return []

    if kind in unit_kinds_singular:
        kind = unit_singular_to_plural[kind]
        selected_obj = ['unit', kind, num, num]
    elif kind in {'group', 'army'}:
        selected_obj = [kind, num]
    elif kind in buildings:
        selected_obj = ['building', kind, num]
    elif kind == 'town':
        selected_obj = ['town', num]
    else:
        # Due to the second conditional statement in this function, this code should never be reached.
        selected_obj = []

    return selected_obj


########  NOTE: Most of the following several functions have the same arguments so that they can be
# called uniformly via **kwargs.
def build_something(player, inpt_as_ls, selected_obj=None, selected_town_num=1):
    """In order to not return [], selected_obj must either be
    (a) a villager, or villagers, or group of villagers OR
    (b) a building (which builds units)"""
    # selected_town_num will be used when building walls.
    if len(inpt_as_ls) < 2:
        return []
    if not selected_obj or not type(selected_obj) is list:
        print('Command rejected:')
        print('You must first select an object before building something.')
        print('For building a building, you must first select which villagers to build it.')
        print('To build units, you must first select which building to build them from.')
        return []
    if len(selected_obj) < 2:
        return []

    if selected_obj[0] == 'building':
        return build_unit(player, inpt_as_ls, selected_obj, selected_town_num)

    elif selected_obj[0] == 'unit':
        if selected_obj[1] == 'villagers':
            return build_building(player, inpt_as_ls, selected_obj, selected_town_num)
        else:
            print('In order to build a building, the selected object needs to be some villager(s)',
                  "--possibly a 'group' of villagers.")
            return []
    elif selected_obj[0] == 'group':
        return build_building(player, inpt_as_ls, selected_obj, selected_town_num)
    else:
        return []


# The following is intended to only be used by the function build_something
def build_unit(player, inpt_as_ls, selected_obj, selected_town_num=1):
    """Returns a list.

    In order to not return [],
    (a) The building which builds the unit(s) must be selected as selected_obj, and
    (b) inpt_as_ls must be of the following type:
    ['build', <unit type>], (which builds 1 of the given unit type) or
    ['build', 'num', <unit type>]

    If not returning [], this function returns a list of the following format:
    ['build unit', <building>, <unit type>, num_to_be_built], where
    num_to_be_built >= 1"""
    if not selected_obj or not type(selected_obj) is list:
        return []
    if len(selected_obj) < 2:
        return []

    building = selected_obj_to_actual_building(player, selected_obj)
    if not building:
        return []

    unit_type = inpt_as_ls[-1]
    if unit_type not in unit_kinds and unit_type not in unit_kinds_singular:
        print('The last part of your command (which type of unit to be built) was not understood.')
        return []
    if unit_type in unit_kinds_singular:
        unit_type = unit_singular_to_plural[unit_type]

    if len(inpt_as_ls) == 3:
        try:
            num_to_be_built = int(inpt_as_ls[1])
            if num_to_be_built < 1:
                print('Your command must specify a positive number of units to be built.')
                return []
        except ValueError:
            print('The second part of your command (how many units to be built) was not understood.')
            return []
    else:
        num_to_be_built = 1

    return ['build unit', building, unit_type, num_to_be_built]


# The following is intended to only be used by the function build_something
def build_building(player, inpt_as_ls, selected_obj=None, selected_town_num=1):
    return ['build building']


def collect_resource(player, inpt_as_ls, selected_obj=None, selected_town_num=1):
    """In order to not return [], selected_obj must be of villager type.

    If not returning [], returns
    ['collect resource', <resource>, ls_of_villagers], where ls_of_villagers is non-empty"""
    if not selected_obj_consists_of_villagers(selected_obj):
        return []

    ls_of_villagers = selected_obj_to_ls_of_units(player, selected_obj)
    if len(ls_of_villagers) == 0:
        print('Command to collect resources rejected since the selected object was empty.')
        return []

    if len(inpt_as_ls) != 2:
        print('Your command was not understood. Any command to collect resources must consist',
              'of two words.')
        return []

    resource = inpt_as_ls[1]
    if not resource in resource_kind_to_class:
        print('The resource you want to collect was not understood.')
        return []

    resource = resource_kind_to_class[resource]
    command = inpt_as_ls[0]
    if command == 'chop':
        if not resource is Wood:
            print('Only wood can be chopped.')
            return []

    if command == 'mine':
        if not resource in {Stone, Gold, Bronze, Iron}:
            print('Only stone, gold, bronze, and iron can be mined.')
            return []

    return ['collect resource', resource, ls_of_villagers]



def select_something(player, inpt_as_ls, selected_obj=None, selected_town_num=1):
    """The point of this function is to return an output selected_obj
    returns [] or a list in one of the following formats:

    ['unit', unit.kind, starting_num, ending_num],  1 <= where starting_num <= ending_num
    or
    ['army', army_num], where 1 <= army_num
    or
    ['group', group_num], where 1 <= group_num
    or
    ['building', building.kind, building_num], where 1 <= building_num
    or
    ['town', town_num], where 1 <= town_num

    Note: The arguments player, selected_obj, and selected_town_num are not used.
    """
    if len(inpt_as_ls) > 2:
        # Then the player has specified the building or unit number(s)
        return extract_selected_obj(inpt_as_ls)
    elif len(inpt_as_ls) < 2:
        return []
    else:
        # Current Usage: In this case, there is an implied '1' as the building or unit number.
        # Alternate usage (not used): It would make sense that ['select', 'barracks'] is
        # selecting the only barracks in the town with the given selected_town_num.
        inpt_as_ls.append('1')
        return extract_selected_obj(inpt_as_ls)


def is_a_selected_obj(ls):
    """Returns True if ls is a non-empty list of the format of what select_something returns"""
    if type(ls) != list:
        return False
    if len(ls) < 2 or len(ls) > 4:
        return False
    if ls[0] not in ('unit', 'army', 'group', 'building', 'town'):
        return False

    if ls[0] == 'unit':
        if len(ls) != 4:
            return False
        if ls[1] not in unit_kinds:
            return False
        if not type(ls[2]) is int or not type(ls[3]) is int:
            return False
        if not 1 <= ls[2] <= ls[3]:
            return False
        return True

    if ls[0] in ('army', 'group',  'town'):
        if len(ls) != 2:
            return False
        return type(ls[1]) is int and 1 <= ls[1]

    if ls[0] == 'building':
        if len(ls) != 3:
            return False
        if ls[1] not in buildings:
            return False
        return type(ls[2]) is int and 1 <= ls[2]


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
    """returns []"""
    if selected_obj is None:
        selected_obj = []

    def print_selected_obj(player, selected_obj):
        if len(selected_obj) == 0:
            print('There is nothing to print.')
            return []
        if selected_obj[0] == 'building':
            building = selected_obj_to_actual_building(player, selected_obj)
            print(building)
            return []
        else:
            ls_of_units = selected_obj_to_ls_of_units(player, selected_obj)
            for unit in ls_of_units:
                print(unit)
            return []

    if len(inpt_as_ls) == 1:
        # The player is trying to print selected_obj and inpt_as_ls == ['print']
        return print_selected_obj(player, selected_obj)
    elif len(inpt_as_ls) == 2:
        if inpt_as_ls[1] == 'commands':
            # Then inpt_as_ls == ['print', 'commands']
            help(selected_obj)
            return []
        elif inpt_as_ls[1] == 'resources':
            print(player.resources)
            return []
        else:
            inpt_as_ls.append('1')

    if len(inpt_as_ls) >= 4:
        if inpt_as_ls[1] == 'map':
            return print_part_of_map(player, inpt_as_ls)

    selected_obj = extract_selected_obj(inpt_as_ls)

    return print_selected_obj(player, selected_obj)


def print_part_of_map(player, inpt_as_ls):
    """In order to print properly, inpt_as_ls must be of the following form:
    ['print', 'map',...,'num1', 'num2']
    where anything at all can be placed in the ellipsis. Also, of course,
    Position(num1, num2) must be on the map. The reason why the first two entries of
    inpt_as_ls must be 'print' 'map' is that that is necessary for this function to
    even be called by the function print_something."""

    # I may eventually change this function so that each player has their own copy of the map,
    # and this would then print their copy. In this case, the variable player would be used.

    def str_to_int(s):
        try:
            return int(s)
        except ValueError:
            return None

    i = str_to_int(inpt_as_ls[-2])
    j = str_to_int(inpt_as_ls[-1])

    if i is None or j is None:
        return []

    game_map.print_centered_at(Position(i, j))
    return []

functions = {'build': build_something, 'select': select_something, 'move': move_unit_or_units,
             'set': set_default_build_position, 'print': print_something}

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
        elif first_argument_of_command in help_commands:
            help(selected_obj)
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

    p1 = Player(1, Position(80, 80), is_human=True)
    print(selected_obj_to_actual_building(p1, ['building', 'towncenter', 1]))
    assert selected_obj_to_actual_building(p1, ['building', 'blah', 1]) == None
    assert selected_obj_to_actual_building(p1, ['building', 'barracks', 1]) == None
    # a = input_next_command(p1)
    # print(a)

    # Testing the function collect_resource
    # inpt_as_ls = ['collect', 'wood']
    # for selected_obj in ([], None, ['unit', 'swordsmen', 1, 4]):
    #     assert collect_resource(p1, inpt_as_ls, selected_obj) == []
    #
    # selected_obj = ['unit', 'villagers', 4, 4]
    # assert collect_resource(p1, inpt_as_ls, selected_obj) == []
    #
    # selected_obj = ['unit', 'villagers', 2, 3]
    # print(collect_resource(p1, inpt_as_ls, selected_obj))

    # for inpt_as_ls in (['chop', 'gold'], ['mine', 'wood'], ['collect', 'blah']):
    #     print(collect_resource(p1, inpt_as_ls, selected_obj))

    # Testing the function print_part_of_map
    # inpt_as_ls = ['print', 'map', '80', '80']
    # print_part_of_map(p1, inpt_as_ls)
    # print("--------------------------------------------------------------------------------------")
    # inpt_as_ls = ['print', 'map', 'n10', 'e15']
    # print_part_of_map(p1, inpt_as_ls)
    # inpt_as_ls = ['print','map','blah','yeah']
    # print_part_of_map(p1, inpt_as_ls)
    # print("--------------------------------------------------------------------------------------")
    # inpt_as_ls = ['print', 'map', 'centered', 'on', '40', '60']
    # print_part_of_map(p1, inpt_as_ls)




