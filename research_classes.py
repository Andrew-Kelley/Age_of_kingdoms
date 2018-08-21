from copy import copy
from resources import Resources, Food, Wood, Stone, Bronze, Gold, Iron


# Whenever a player begins researching something at some building, an instance of a subclass of
# ResearchObject is created.
class ResearchObject:
    # The following should always be overridden by each subclass
    num_turns_to_completion = 30 # might be changed to time_to_completion
    cost = Resources({Wood: 1000, Stone: 1000, Bronze: 1000, Gold: 1000, Iron: 1000})
    name = 'Class ResearchObject'

    def __init__(self):
        self.progress_to_completion = 0

    def make_progress(self):
        self.progress_to_completion += 1

    def research_completed(self, player):
        # This should always be overridden by each subclass
        print('ERROR! (This message is for developers of this game only.)',
              'The research_completed method of the class ResearchObject was called',
              'when self was ', self)


############################################## Researched at a TownCenter:
class BronzeAge(ResearchObject):
    num_turns_to_completion = 8
    cost = Resources({Food: 100, Wood: 500, Stone: 200})
    name = 'bronze age'

    def research_completed(self, player):
        player.age = 'bronze age'
        player.things_researched.add(self.name)


class IronAge(ResearchObject):
    num_turns_to_completion = 8
    cost = Resources({Food: 500, Gold: 300, Bronze: 300})
    name = 'iron age'

    def research_completed(self, player):
        player.age = 'iron age'
        player.things_researched.add(self.name)

# class WheelBarrow(ResearchObject):
#     num_turns_to_completion = 3
#     cost = Resources({Wood: 100, Bronze: 200})
#
#     def research_completed(self, player):
#         pass


############################################## Researched at a Blacksmith:
class BronzeTippedSpears(ResearchObject):
    num_turns_to_completion = 3
    cost = Resources({Bronze: 100, Gold: 50})
    name = 'bronze tipped spears'

    def research_completed(self, player):
        pass


class BronzeSwords(ResearchObject):
    num_turns_to_completion = 3
    cost = Resources({Bronze: 140, Gold: 55})
    name = 'bronze swords'

    def research_completed(self, player):
        pass


# Maybe the following is too broad. I should perhaps have different research armor items for
# archers than for the rest.
# class BronzeArmor(ResearchObject):
#     pass


class BronzeShields(ResearchObject):
    num_turns_to_completion = 3
    cost = Resources({Bronze: 150, Gold: 60})
    name = 'bronze shields'

    def research_completed(self, player):
        pass


class BronzeAxes(ResearchObject):
    num_turns_to_completion = 2
    cost = Resources({Bronze: 130, Gold: 20})
    name = 'bronze axes'

    def research_completed(self, player):
        pass


class BronzePicks(ResearchObject):
    num_turns_to_completion = 2
    cost = Resources({Bronze: 130, Gold: 20})
    name = 'bronze picks'

    def research_completed(self, player):
        pass


####################################

stone_age_research = {BronzeAge.name}

bronze_age_research = copy(stone_age_research)
for research_obj in (IronAge, BronzeTippedSpears, BronzeSwords, BronzeShields, BronzeAxes, BronzePicks):
    bronze_age_research.add(research_obj.name)

iron_age_research = copy(bronze_age_research)
# Add an iron version for every bronze research at the blacksmith.

research_string_to_class = {'bronze age': BronzeAge, 'iron age': IronAge,
                            'bronze tipped spears': BronzeTippedSpears, 'bronze swords': BronzeSwords,
                            'bronze shields': BronzeShields, 'bronze axes': BronzeAxes,
                            'bronze picks': BronzePicks}


for name in research_string_to_class:
    research_obj = research_string_to_class[name]
    assert name == research_obj.name

