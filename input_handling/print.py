from game_map import game_map
from input_handling.select_an_object import SelectedBuilding
from input_handling.select_an_object import extract_selected_obj
from game_map import Position
from input_handling.help import help_on


def print_something(player, inpt_as_ls, selected_obj=None):
    """returns []"""

    def print_selected_obj(player, selected_obj):
        if not selected_obj:
            print('There is nothing to print.')
            return []
        if isinstance(selected_obj, SelectedBuilding): #selected_obj[0] == 'building':
            building = selected_obj.building
            print(building)
            return []
        else:
            #Todo Check that this works for Army and Group
            for unit in selected_obj.units:
                print(unit)
            return []

    if len(inpt_as_ls) == 1:
        # The player is trying to print selected_obj and inpt_as_ls == ['print']
        return print_selected_obj(player, selected_obj)
    elif len(inpt_as_ls) == 2:
        if inpt_as_ls[1] == 'commands':
            # Then inpt_as_ls == ['print', 'commands']
            help_on(selected_obj)
            return []
        elif inpt_as_ls[1] == 'resources':
            print(player.resources)
            return []
        #TODO: add the following lines:
        # elif inpt_as_ls[1] == 'population':
        #     then print the current population and the current pop limit.
        else:
            inpt_as_ls.append('1')

    if len(inpt_as_ls) >= 4:
        if inpt_as_ls[1] == 'map':
            return print_part_of_map(player, inpt_as_ls)

    selected_obj = extract_selected_obj(inpt_as_ls, player)

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

    i = str_to_int(inpt_as_ls[-2])
    j = str_to_int(inpt_as_ls[-1])

    if i is None or j is None:
        return []

    game_map.print_centered_at(Position(i, j))
    return []


def str_to_int(s):
    try:
        return int(s)
    except ValueError:
        return None


if __name__ == '__main__':
    from player import Player

    p1 = Player(1, Position(80, 80), is_human=True)

    # Testing the function print_part_of_map
    inpt_as_ls = ['print', 'map', '80', '80']
    print_part_of_map(p1, inpt_as_ls)
    print("----------------------------------------------------------------------------------")
    inpt_as_ls = ['print', 'map', 'n10', 'e15']
    print_part_of_map(p1, inpt_as_ls)
    inpt_as_ls = ['print', 'map', 'blah', 'yeah']
    print_part_of_map(p1, inpt_as_ls)
    print("----------------------------------------------------------------------------------")
    inpt_as_ls = ['print', 'map', 'centered', 'on', '40', '60']
    print_part_of_map(p1, inpt_as_ls)
