from input_handling.select_an_object import selected_obj_consists_of_villagers
from input_handling.select_an_object import selected_obj_to_ls_of_units
from input_handling.print import str_to_int
from resources import resource_kind_to_class, Wood, Stone, Gold, Bronze, Iron
from buildings.resource_bldngs import Farm
from game_map import Position


def collect_resource(player, inpt_as_ls, selected_obj=None, selected_town_num=1):
    """In order to not return [], selected_obj must be of villager type.

    If not returning [], returns
    ['collect resource', <resource>, ls_of_villagers], where
    ls_of_villagers is non-empty"""
    if not selected_obj_consists_of_villagers(selected_obj):
        return []

    ls_of_villagers = selected_obj_to_ls_of_units(player, selected_obj)
    if len(ls_of_villagers) == 0:
        print('Command to collect resources rejected since the selected '
              'object was empty.')
        return []

    if len(inpt_as_ls) != 2:
        print('Your command was not understood. Any command to collect '
              'resources must consist',
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

    if resource == Iron:
        if player.age == 'stone age':
            print('Iron can only be mined in the Bronze age and later.')
            return []

    return ['collect resource', resource, ls_of_villagers]


def farm(player, inpt_as_ls, selected_obj=None, selected_town_num=1):
    """In order to not return [], selected_obj must be of villager type and
    inpt_as_ls must be in the following format:
    ['farm', ..., 'num1', 'num2'], where there is an available farm at
    Position(num1, num2).

    If not returning [], returns
    ['farm', farm_instance, ls_of_villagers], where ls_of_villagers is non-empty"""
    if len(inpt_as_ls) < 3:
        print('Your command was invalid.')
        return []

    if not selected_obj_consists_of_villagers(selected_obj):
        print('Command rejected. Only villagers can farm.')
        return []

    ls_of_villagers = selected_obj_to_ls_of_units(player, selected_obj)
    if len(ls_of_villagers) == 0:
        print('Command to farm was rejected since no villagers were selected.')
        return []

    i = str_to_int(inpt_as_ls[-2])
    j = str_to_int(inpt_as_ls[-1])

    if i is None or j is None:
        print('The position of the farm was not understood. Command rejected.')
        return []

    position = Position(i, j)
    if position in player.building_position_pairs:
        farm = player.building_position_pairs[position]
        if not isinstance(farm, Farm):
            print('There is no farm at position', position)
            return []
    else:
        print('There is no building (or farm) at position', position)
        return []

    return ['farm', farm, ls_of_villagers]


if __name__ == '__main__':
    from player import Player

    p1 = Player(1, Position(80, 80), is_human=True)
    inpt_as_ls = ['collect', 'wood']
    for selected_obj in ([], None, ['unit', 'swordsmen', 1, 4]):
        assert collect_resource(p1, inpt_as_ls, selected_obj) == []

    selected_obj = ['unit', 'villagers', 4, 4]
    assert collect_resource(p1, inpt_as_ls, selected_obj) == []

    selected_obj = ['unit', 'villagers', 2, 3]
    print(collect_resource(p1, inpt_as_ls, selected_obj))

    # for inpt_as_ls in (['chop', 'gold'], ['mine', 'wood'], ['collect', 'blah']):
    #     print(collect_resource(p1, inpt_as_ls, selected_obj))
