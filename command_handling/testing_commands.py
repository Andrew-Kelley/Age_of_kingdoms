
from player import Player
from game_map import Position, Vector
from input_handling.get_input import get_next_command
from buildings.resource_bldngs import Farm

from insert_commands import insert_command


p1 = Player(1, Position(80, 80), is_human=True)

def given_this_input_insert_command(inpt, sel_obj=None, player=p1):
    """Given this input, insert the command specified by the input"""
    command = get_next_command(player, inpt, sel_obj)
    insert_command(p1, command)


# The following tests were mostly done by first running them to see what
# they'd get and then creating a test that just states the results I just
# saw. (My purpose here is to check that when editing this file, the behavior
# of this module doesn't change.)
villagers = p1.units['villagers']
villager1 = villagers[1]
villager2 = villagers[2]
villager3 = villagers[3]

################################################################
# Checking the function insert_move_command
vector1 = Vector(-2, 5)
given_this_input_insert_command('move villager 1 n2 e5')
assert p1.commands['now']['move'][villager1] == vector1

vector2 = Vector(7, -8)
vector3 = Vector(3, -2)
# Note that vector2 + vector3 == Vector(10, -10)
given_this_input_insert_command('move villagers 2-3 s10 w10')
for v in villagers[2:]:
    assert p1.commands['now']['move'][v] == vector2
    assert p1.commands['later']['move'][v] == vector3

vector4 = Vector(4, 8)
given_this_input_insert_command('move villager 2 s4 e8')
assert p1.commands['now']['move'][villager2] == vector4

selected_obj = get_next_command(p1, 'select villagers 1-3')
vector5 = Vector(-1, -9)
given_this_input_insert_command('move n1 w9', selected_obj)
for villager in villagers[1:]:
    assert p1.commands['now']['move'][villager] == vector5

assert p1.commands['later']['move'] == {}

################################################################
# Checking the function insert_build_unit_command
towncenter = p1.buildings['towncenter'][1]

selected_obj = get_next_command(p1, 'select towncenter')
# The following line is to check that the unit test
# immediately after does have the proper input.
assert selected_obj.building == towncenter
given_this_input_insert_command('build 4 villagers', selected_obj)
assert p1.commands['now']['build unit'][towncenter] == ['villagers', 1]
assert p1.commands['later']['build unit'][towncenter] == ['villagers', 3]

from buildings.military_bldngs import Barracks
position = Position(80, 50)
barracks = Barracks(1, position, p1)
p1.buildings[Barracks.kind].append(barracks)
selected_obj = get_next_command(p1, 'select barracks')
assert selected_obj.building == barracks
get_next_command(p1, 'set build position 60 40', selected_obj)
the_build_position = Position(60, 40)
# The following line isn't really testing insert_build_unit_command
assert barracks.build_position == the_build_position

given_this_input_insert_command('build 6 pikemen', selected_obj)
assert p1.commands['now']['build unit'][barracks] == ['pikemen', 1]
assert p1.commands['later']['build unit'][barracks] == ['pikemen', 5]

################################################################
# Checking the function insert_collect_resource_now_command
from resources import Food

selected_obj = get_next_command(p1, 'select villagers 1-3')
given_this_input_insert_command('collect food', selected_obj)
for villager in (villager1, villager2):
    assert villager.current_action == 'collecting food'
    assert p1.commands['now']['collect resource'][villager] == Food
# villager3 is too far away to collect food now, and so his current
# action (which was to move) was overridden by the (failed) command
# to collect food.
assert villager3.current_action == 'doing nothing'

################################################################
# Checking the function insert_build_building_command

from buildings.other_bldngs import House

selected_obj = get_next_command(p1, 'select villagers 1-2')
given_this_input_insert_command('build house 75 75', selected_obj)
ls = p1.commands['now']['build building'][villager1]
house = ls[0]
assert isinstance(house, House)
position = ls[1]
assert position == Position(75, 75)
assert ls == p1.commands['later']['build building'][villager2]
delta = position - villager2.position
assert p1.commands['now']['move'][villager2] == delta

selected_obj = get_next_command(p1, 'select villager 3')
given_this_input_insert_command('help build house 75 75', selected_obj)
delta = position - villager3.position
assert p1.commands['now']['move'][villager3] == delta
assert ls == p1.commands['later']['build building'][villager3]

################################################################
# Checking the function insert_research_command
from research_classes import BronzeAge

selected_obj = get_next_command(p1, 'select towncenter')
given_this_input_insert_command('research bronze age', selected_obj)

assert isinstance(p1.commands['now']['research'][towncenter], BronzeAge)

################################################################
# Checking the function insert_farm_command

position = Position(74, 78)
farm = Farm(1, position, p1)
p1.buildings[Farm.kind].append(farm)

selected_obj = get_next_command(p1, 'select villager 1')
given_this_input_insert_command('farm 74 78', selected_obj)
assert p1.commands['now']['farm'][villager1] == farm

selected_obj = get_next_command(p1, 'select villager 3')
given_this_input_insert_command('farm 74 78', selected_obj)
assert p1.commands['later']['farm'][villager3] == farm
delta = p1.commands['now']['move'][villager3]
assert delta == position - villager3.position

# TODO: Doublecheck in the game itself that a 3rd villager
# more than 6 or maybe 15 units away from a farm cannot start
# farming it, if the farm already has 2 farmers farming it.
# selected_obj = get_next_command(p1, 'select villager 2')
# given_this_input_insert_command('farm 74 78', selected_obj)
# assert p1.commands['later']['farm'][villager2] == farm
