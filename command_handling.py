# This module handles the commands which are returned by the function input_next_command

# player.commands['now'] is in the following format:
# {'move':dict( unit:new_position for units to be moved ),
#  'build building':dict( villager:building_to_be_built for ...),
#  'collect resource':( villager:resource_object_to_collect for ...),
#  'build unit':dict( building:[unit_to_be_built, number_of_units_of_that_type_to_build] for ... ),
#  'research':dict( building:thing_to_be_researched for ...),
#  ...}
# Eventually, player.commands should also contain keywords such as follows:
# 'attack', 'defend'

# I need to have a function which checks if a given unit has already been commanded to do something. I think
# newer commands will override older ones.
