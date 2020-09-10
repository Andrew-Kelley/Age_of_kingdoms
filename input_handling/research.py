from input_handling.select_an_object import SelectedBuilding
from buildings.bldng_class import Building
from research_classes import research_string_to_class, stone_age_research, bronze_age_research


def research_something(player, inpt_as_ls, selected_obj=None):
    """To not return [], inpt_as_ls must be of the following format:
    ['research','word1', <optional> 'word2'], and
    'word1 word2' must be something that can be researched from the selected building.

    Returns [] or
    ['research', building, thing_to_be_researched], where thing_to_be_researched is a
    subclass of ResearchObject and building is a Building instance that is not currently
    researching anything."""
    if not isinstance(selected_obj, SelectedBuilding):
        print('You must first select a building to research something.')
        return []

    building = selected_obj.building
    if not isinstance(building, Building):
        print('The selected object was not a building.')
        print('You must first select a building to research something.')
        return []

    if building in player.commands['now']['research']:
        print('The selected building is already researching something.', end = '\n\n')
        yes_or_no = input('Would you like the building to research '
                          'this afterwards? ').lower().strip()
        if yes_or_no.startswith('y'):
            # Then the rest of this function will still run.
            player.log_command("Yes, add to research queue.")
        else:
            print('Ok, the building will not research it.')
            player.log_command("No, do not add to research queue.")
            return []

    thing_to_be_researched = ' '.join(inpt_as_ls[1:])
    what_can_be_researched = building.things_which_can_be_researched()
    if thing_to_be_researched not in what_can_be_researched:
        print('Sorry, a {} cannot research {}.'.format(building.kind, thing_to_be_researched))
        return []

    if player.age == 'stone age':
        if thing_to_be_researched not in stone_age_research:
            print('Sorry,', thing_to_be_researched, 'cannot be researched in the stone age.')
            return []
    elif player.age == 'bronze age':
        if thing_to_be_researched not in bronze_age_research:
            print('Sorry,', thing_to_be_researched, 'cannot be researched in the bronze age.')
            return []

    if thing_to_be_researched not in research_string_to_class:
        print('Error. This game is still unfinished, and researching',
              thing_to_be_researched, 'has not yet been enabled.',
              'Developer note: specifically,', thing_to_be_researched,
              'has not yet been added to the research_string_to_class dictionary.')
        return []

    if thing_to_be_researched in player.things_being_currently_researched:
        print('You are already researching ', thing_to_be_researched)
        print('Command rejected.')
        return []
    elif thing_to_be_researched in player.things_researched:
        print('You already researched', thing_to_be_researched)
        print('Command rejected.')
        return []

    player.things_being_currently_researched.add(thing_to_be_researched)

    research_object_class = research_string_to_class[thing_to_be_researched]
    thing_to_be_researched = research_object_class()

    return ['research', building, thing_to_be_researched]

