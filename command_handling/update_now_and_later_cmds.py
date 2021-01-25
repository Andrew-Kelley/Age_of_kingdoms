from .insert_commands import number_of_units_can_build_in_one_turn
from .insert_commands import collecting_resource_action
from command_handling.strings import NOW, LATER, BUILD_BUILDING, BUILD_UNIT
from command_handling.strings import COLLECT_RESOURCE, MOVE, RESEARCH, FARM

# The following is called at the beginning of each player's turn.
def update_now_and_later_commands(player):
    # update_build_building_command must come before update_collect_resource_command(player)
    update_build_building_command(player)
    update_move_commands(player)  # This MUST come before update_collect_resource_command(player)
    update_collect_resource_command(player)
    update_build_unit_commands(player)
    update_research_commands(player)
    # The following should come after update_build_building and update_move_commands
    update_farm_commands(player)


# The reason why this function must come before update_collect_resource_command in the function
# update_now_and_later_commands is that once a player finishes building a farm, the villager
# must be deleted from player.commands[NOW][BUILD_BUILDING] before the villager can start
# collecting food from that farm.
def update_build_building_command(player):
    for villager in list(player.commands[LATER][BUILD_BUILDING]):
        building, building_position = player.commands[LATER][BUILD_BUILDING][villager]
        delta = building_position - villager.position
        if delta.magnitude <= 6:
            del player.commands[LATER][BUILD_BUILDING][villager]
            player.commands[NOW][BUILD_BUILDING][villager] = [building, building_position]
            villager.current_action = 'building {}'.format(building)
    for villager in list(player.commands[NOW][BUILD_BUILDING]):
        building, building_position = player.commands[NOW][BUILD_BUILDING][villager]
        if building.progress_to_construction >= building.time_to_build:
            del player.commands[NOW][BUILD_BUILDING][villager]
            # The following statement could probably be run without checking the condition.
            # This is as long as update_build_building_command comes first in the function
            # update_now_and_later_commands
            if villager.current_action.startswith('building'):
                villager.current_action = 'doing nothing'


# Villagers are commanded to collect resources later is if they first have to move or if they
# build a building from resource_bldngs.py. The former case (of having to move first) is
# intended to be used only for newly built villagers.
def update_collect_resource_command(player):
    for villager in list(player.commands[LATER][COLLECT_RESOURCE]):
        not_moving = villager not in player.commands[NOW][MOVE]
        not_building = villager not in player.commands[NOW][BUILD_BUILDING]
        if not_moving and not_building:
            resource = player.commands[LATER][COLLECT_RESOURCE][villager]
            del player.commands[LATER][COLLECT_RESOURCE][villager]
            player.commands[NOW][COLLECT_RESOURCE][villager] = resource
            # In order for the following action to be correct, I think the present function
            # should come after update_move_commands in the
            # function update_now_and_later_commands
            villager.current_action = collecting_resource_action(resource.kind)


# The following removes all the old commands in player.commands[NOW][MOVE], and it updates
# player.commands[NOW][MOVE] based on what player.commands[LATER][MOVE] is.
def update_move_commands(player):
    for unit in list(player.commands[NOW][MOVE]):
        del player.commands[NOW][MOVE][unit]
        # If a villager had to move to start building a building, then the function
        # update_build_building_command may have changed unit.current_action. And this change
        # should not be overwritten.
        if unit.current_action.startswith('moving'):
            unit.current_action = 'doing nothing'

    for unit in list(player.commands[LATER][MOVE]):
        delta = player.commands[LATER][MOVE][unit]
        if delta.magnitude > 15:
            beginning, the_rest = delta.beginning_plus_the_rest()
            player.commands[NOW][MOVE][unit] = beginning
            # The following line is necessary because the present function changed
            # current_action to 'doing nothing'
            unit.current_action = 'moving to {}'.format(unit.position + delta)
            player.commands[LATER][MOVE][unit] = the_rest
        else:
            player.commands[NOW][MOVE][unit] = delta
            unit.current_action = 'moving to {}'.format(unit.position + delta)
            del player.commands[LATER][MOVE][unit]


def update_build_unit_commands(player):
    for building in list(player.commands[NOW][BUILD_UNIT]):
        del player.commands[NOW][BUILD_UNIT][building]

    for building in list(player.commands[LATER][BUILD_UNIT]):
        unit_type = player.commands[LATER][BUILD_UNIT][building][0]
        num_left_to_build = player.commands[LATER][BUILD_UNIT][building][1]
        num_can_build = number_of_units_can_build_in_one_turn(player, building, unit_type)

        num_to_build_now = min(num_can_build, num_left_to_build)
        num_to_build_later = num_left_to_build - num_to_build_now
        player.commands[NOW][BUILD_UNIT][building] = [unit_type, num_to_build_now]
        if num_to_build_later > 0:
            player.commands[LATER][BUILD_UNIT][building] = [unit_type, num_to_build_later]
        else:
            del player.commands[LATER][BUILD_UNIT][building]


def update_research_commands(player):
    for building in list(player.commands[NOW][RESEARCH]):
        thing_to_be_researched = player.commands[NOW][RESEARCH][building]
        if thing_to_be_researched.name in player.things_researched:
            del player.commands[NOW][RESEARCH][building]

    for building in list(player.commands[LATER][RESEARCH]):
        queue = player.commands[LATER][RESEARCH][building]
        if len(queue) > 0:  # As it should be at this point
            if building not in player.commands[NOW][RESEARCH]:
                research_this_next = queue.popleft()
                player.commands[NOW][RESEARCH][building] = research_this_next
                print('Beginning the following research: {}\n'.format(research_this_next.name))
        if len(queue) == 0:
            del player.commands[LATER][RESEARCH][building]


# The reason why this function should be called after the functions update_build_building and
# update_move_commands (in the update_now_and_later_commands function) is that when a villager
# is finished building or moving, it ought to be able to start farming.
def update_farm_commands(player):
    for villager in list(player.commands[LATER][FARM]):
        farm = player.commands[LATER][FARM][villager]
        not_moving = villager not in player.commands[NOW][MOVE]
        not_building = villager not in player.commands[NOW][BUILD_BUILDING]
        if not_moving and not_building:
            del player.commands[LATER][FARM][villager]
            delta = farm.position - villager.position
            if delta.magnitude < 2:
                if farm.number_of_farmers < 2:
                    player.commands[NOW][FARM][villager] = farm
                    farm.add_farmer(villager)
                    villager.farm_currently_farming = farm
                    villager.current_action = 'farming {}'.format(farm)
                else:
                    # This really should never happen. If it does, I have a coding error.
                    print(villager, ' cannot farm', farm, 'because that farm already has',
                          'two farmers. Regardless, the villager is removed from ',
                          "player.commands[LATER][FARM]")
            else:
                # This also should never happen (assuming no coding errors elsewhere).
                print(villager, 'cannot farm', farm, 'because the villager is not within',
                      'one spot of the farm. Regardless, the villager is removed from ',
                      "player.commands[LATER][FARM]")
