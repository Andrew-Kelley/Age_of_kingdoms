from input_handling.select_an_object import SelectedUnits
from input_handling.from_ls_get_position import get_position_from_inpt_as_ls
from resources import resource_kind_to_class, Wood, Stone, Gold, Bronze, Iron
from buildings.resource_bldngs import Farm
from command_handling.commands import CollectResourceCmd, FarmCmd
from game_map import Position


def collect_resource(player, inpt_as_ls, selected_obj=None):
    """In order to not return None, selected_obj must consist of villagers.

    If not returning [], returns
    ['collect resource', <resource>, ls_of_villagers], where
    ls_of_villagers is non-empty"""
    if not isinstance(selected_obj, SelectedUnits):
        return
    if not selected_obj.consists_of_villagers:
        return


    if selected_obj.is_empty:
        print('Command to collect resources rejected since the selected '
              'object was empty.')
        return

    if len(inpt_as_ls) != 2:
        print('Your command was not understood. Any command to collect '
              'resources must consist',
              'of two words.')
        return

    resource = inpt_as_ls[1]
    if not resource in resource_kind_to_class:
        print('The resource you want to collect was not understood.')
        return

    resource = resource_kind_to_class[resource]
    command = inpt_as_ls[0]
    if command == 'chop':
        if not resource is Wood:
            print('Only wood can be chopped.')
            return

    if command == 'quarry':
        if not resource is Stone:
            print('Only stone can be quarried.')
            return

    if command == 'mine':
        if not resource in {Gold, Bronze, Iron}:
            print('Only gold, bronze, and iron can be mined.')
            return

    if resource == Iron:
        if player.age == 'stone age':
            print('Iron can only be mined in the Bronze age and later.')
            return

    villagers = selected_obj.units
    return CollectResourceCmd(resource, villagers)


def farm(player, inpt_as_ls, selected_obj=None):
    """In order to not return None, selected_obj must consist of villagers and
    inpt_as_ls must be in the following format:
    ['farm', ..., 'num1', 'num2'], where there is an available farm at
    Position(num1, num2)."""
    if len(inpt_as_ls) < 3:
        print('Your command was invalid.')
        return

    if not isinstance(selected_obj, SelectedUnits):
        print('Command rejected. Only villagers can farm.')
        return
    if not selected_obj.consists_of_villagers:
        print('Command rejected. Only villagers can farm.')
        return

    if selected_obj.is_empty:
        print('Command to farm was rejected since no villagers were selected.')
        return

    position = get_position_from_inpt_as_ls(inpt_as_ls)
    if not position:
        print('The position of the farm was not understood. Command rejected.')
        return

    if position in player.building_position_pairs:
        farm = player.building_position_pairs[position]
        if not isinstance(farm, Farm):
            print('There is no farm at position', position)
            return
    else:
        print('There is no building (or farm) at position', position)
        return

    villagers = selected_obj.units
    return FarmCmd(farm, villagers)


if __name__ == '__main__':
    from player import Player

    p1 = Player(1, Position(80, 80), is_human=True)
    inpt_as_ls = ['collect', 'wood']


    # TODO: fix these broken tests (which depend on the old usage
    # of selected_obj:
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
