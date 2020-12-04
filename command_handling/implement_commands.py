
from map_etc.position import Vector
from map_etc.make_map import game_map
from units import unit_kind_to_class, unit_kind_to_singular


def implement_commands_if_possible(player):
    implement_build_building_command(player)
    implement_collect_resource_command(player)
    implement_move_commands(player)
    implement_build_unit_commands(player)
    implement_research_commands(player)
    implement_farm_commands(player)
    # Eventually, this will probably be replaced with the following code, where functions
    # is a list of all the functions which need to be run.
    # for function in functions:
    #     function(player)


def implement_build_building_command(player):
    for villager in player.commands['now']['build building']:
        building, building_position = player.commands['now']['build building'][villager]
        delta = building_position - villager.position
        if delta == Vector(0, 0):
            pass
        else:
            villager.move_by(delta)
        building.build_by(villager)


def implement_collect_resource_command(player):
    for villager in player.commands['now']['collect resource']:
        resource = player.commands['now']['collect resource'][villager]
        if villager.can_collect_resource_now(resource, player):
            villager.collect_resource(resource, player)


def implement_move_commands(player):
    for unit in player.commands['now']['move']:
        delta = player.commands['now']['move'][unit]
        if unit.can_move(delta, game_map):
            unit.move_by(delta)


def implement_build_unit_commands(player):
    for building in player.commands['now']['build unit']:
        unit_type, num_to_build = player.commands['now']['build unit'][building]
        for i in range(num_to_build):
            if player.population < player.population_cap:
                if unit_type not in unit_kind_to_class:
                    continue
                unit = unit_kind_to_class[unit_type]
                if player.can_build(unit):
                    building.build_unit(unit_type)
                else:
                    unit_type = unit_kind_to_singular[unit.kind].capitalize()
                    print('You do not have enough resources to build a ', unit_type)
                    continue
            else:
                print('Population cap reached. You cannot build more units.')
                return


def implement_research_commands(player):
    for building in player.commands['now']['research']:
        thing_to_research = player.commands['now']['research'][building]
        building.research(thing_to_research)


def implement_farm_commands(player):
    for villager in player.commands['now']['farm']:
        the_farm = player.commands['now']['farm'][villager]
        villager.farm(the_farm, player)
