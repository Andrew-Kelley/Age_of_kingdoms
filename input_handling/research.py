from input_handling.select_an_object import selected_obj_to_actual_building
from buildings.bldng_class import Building
from research_classes import research_string_to_class


def research_something(player, inpt_as_ls, selected_obj=None, selected_town_num=1):
    """To not return [], inpt_as_ls must be of the following format:
    ['research','word1', <optional> 'word2'], and
    'word1 word2' must be something that can be researched from the selected building.

    Returns [] or
    ['research', building, thing_to_be_researched], where thing_to_be_researched is a
    subclass of ResearchObject."""
    if not selected_obj:
        print('You must first select a building to research something.')
        return []

    building = selected_obj_to_actual_building(player, selected_obj)
    if not isinstance(building, Building):
        print('The selected object was not a building.')
        print('You must first select a building to research something.')
        return []

    thing_to_be_researched = ' '.join(inpt_as_ls[1:])
    if thing_to_be_researched not in building.strings_ls_of_things_which_can_be_researched(player):
        print('Sorry, a {} cannot research {}.'.format(building.kind, thing_to_be_researched))
        return []

    if thing_to_be_researched not in research_string_to_class:
        print('Error. This game is still unfinished, and researching',
              thing_to_be_researched, 'has not yet been enabled.',
              'Developer note: specifically, ', thing_to_be_researched,
              'has not yet been added to the research_string_to_class dictionary.')
        return []

    thing_to_be_researched = research_string_to_class[thing_to_be_researched]

    return ['research', building, thing_to_be_researched]
