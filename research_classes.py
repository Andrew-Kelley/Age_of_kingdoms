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
        player.messages += 'You have advanced to the Bronze Age!\n'
        player.things_researched.add(self.name)


class IronAge(ResearchObject):
    num_turns_to_completion = 8
    cost = Resources({Food: 500, Gold: 300, Bronze: 300})
    name = 'iron age'

    def research_completed(self, player):
        player.age = 'iron age'
        player.messages += 'You have advanced to the Iron Age!\n'
        player.things_researched.add(self.name)


# class WheelBarrow(ResearchObject):
#     num_turns_to_completion = 3
#     cost = Resources({Wood: 100, Bronze: 200})
#     name = 'wheel barrow'
#
#     def research_completed(self, player):
#         pass


############################################## Researched at a Blacksmith:
# Benefits pikemen:
class BronzeTippedSpears(ResearchObject):
    num_turns_to_completion = 3
    cost = Resources({Bronze: 100, Gold: 50})
    name = 'bronze tipped spears'

    def research_completed(self, player):
        player.things_researched.add(self.name)

# Required to build swordsmen or knights:
class BronzeSwords(ResearchObject):
    num_turns_to_completion = 3
    cost = Resources({Bronze: 140, Gold: 55})
    name = 'bronze swords'

    def research_completed(self, player):
        player.things_researched.add(self.name)


# Helps pikemen and swordsmen. Necessary for knights. (Does not benefit archers.)
class BronzeArmorPlates(ResearchObject):
    num_turns_to_completion = 3
    cost = Resources({Bronze: 150, Gold: 60})
    name = 'bronze armor plates'

    def research_completed(self, player):
        player.things_researched.add(self.name)


# Benefits archers:
class BronzeChainMailArmor(ResearchObject):
    num_turns_to_completion = 4
    cost = Resources({Bronze: 150, Gold: 60})
    name = 'bronze chainmail armor'

    def research_completed(self, player):
        player.things_researched.add(self.name)


# Necessary for swordsmen and knights:
class BronzeShields(ResearchObject):
    num_turns_to_completion = 3
    cost = Resources({Bronze: 150, Gold: 60})
    name = 'bronze shields'

    def research_completed(self, player):
        player.things_researched.add(self.name)


# Benefits villagers chopping wood:
class BronzeAxes(ResearchObject):
    num_turns_to_completion = 2
    cost = Resources({Bronze: 130, Gold: 20})
    name = 'bronze axes'

    def research_completed(self, player):
        player.collecting_capacity[Wood] += 2
        player.things_researched.add(self.name)


# Benefits villagers collecting stone, gold, bronze, or iron
class BronzePicks(ResearchObject):
    num_turns_to_completion = 2
    cost = Resources({Bronze: 130, Gold: 20})
    name = 'bronze picks'

    def research_completed(self, player):
        for resource in (Stone, Gold, Bronze):
            player.collecting_capacity[resource] += 2
        # Before the following line is run, we have that
        # player.collecting_capacity[Iron] == 2
        player.collecting_capacity[Iron] += 4
        player.things_researched.add(self.name)


# Benefits farmers:
class BronzeTippedPlows(ResearchObject):
    num_turns_to_completion = 2
    cost = Resources({Bronze: 130, Gold: 20})
    name = 'bronze tipped plows'

    def research_completed(self, player):
        for villager in player.units['villagers'][1:]:
            villager.food_from_farming_per_turn = 12
        player.things_researched.add(self.name)


blacksmith_bronze_age_research = {BronzeTippedSpears, BronzeSwords, BronzeArmorPlates,
                                  BronzeShields, BronzeAxes, BronzePicks, BronzeTippedPlows,
                                  BronzeChainMailArmor}


# NOTE: The corresponding bronze research must be completed in order to research
# the iron equivalent.

# Benefits pikemen:
class IronTippedSpears(ResearchObject):
    num_turns_to_completion = 3
    cost = Resources({Iron: 100, Gold: 50})
    name = 'iron tipped spears'

    def research_completed(self, player):
        player.things_researched.add(self.name)


class IronSwords(ResearchObject):
    num_turns_to_completion = 3
    cost = Resources({Iron: 140, Gold: 55})
    name = 'iron swords'

    def research_completed(self, player):
        player.things_researched.add(self.name)


# Helps pikemen and swordsmen. (Does not benefit archers.)
class IronArmorPlates(ResearchObject):
    num_turns_to_completion = 3
    cost = Resources({Iron: 150, Gold: 60})
    name = 'iron armor plates'

    def research_completed(self, player):
        player.things_researched.add(self.name)


# Benefits archers:
class IronChainMailArmor(ResearchObject):
    num_turns_to_completion = 4
    cost = Resources({Iron: 150, Gold: 60})
    name = 'iron chainmail armor'

    def research_completed(self, player):
        player.things_researched.add(self.name)


# Benefits swordsmen and knights:
class IronShields(ResearchObject):
    num_turns_to_completion = 3
    cost = Resources({Iron: 150, Gold: 60})
    name = 'iron shields'

    def research_completed(self, player):
        player.things_researched.add(self.name)


# Benefits villagers chopping wood:
class IronAxes(ResearchObject):
    num_turns_to_completion = 2
    cost = Resources({Iron: 130, Gold: 20})
    name = 'iron axes'

    def research_completed(self, player):
        player.collecting_capacity[Wood] += 2
        player.things_researched.add(self.name)


# Benefits villagers collecting stone, gold, bronze, or iron
class IronPicks(ResearchObject):
    num_turns_to_completion = 2
    cost = Resources({Iron: 130, Gold: 20})
    name = 'iron picks'

    def research_completed(self, player):
        for resource in (Stone, Gold, Bronze):
            player.collecting_capacity[resource] += 2
        # Before the following line is run, we have that
        # player.collecting_capacity[Iron] == 2
        player.collecting_capacity[Iron] += 2
        player.things_researched.add(self.name)


# I don't think I should have a ResearchObject for IronTippedPlows. Villagers already
# collect food from farms fast enough with BronzeTippedPlows.

blacksmith_iron_age_research = {IronTippedSpears, IronSwords, IronArmorPlates, IronChainMailArmor,
                                IronShields, IronAxes, IronPicks}

bronze_to_iron_research_str = {'bronze tipped spears': 'iron tipped spears',
                               'bronze swords': 'iron swords',
                               'bronze armor plates': 'iron armor plates',
                               'bronze chainmail armor': 'iron chainmail armor',
                               'bronze shields': 'iron shields',  'bronze axes': 'iron axes',
                               'bronze picks': 'iron picks'}
####################################

# The following are first sets of classes, to be used to create research_string_to_class
stone_age_research = {BronzeAge}
bronze_age_research = copy(stone_age_research).union({IronAge})
bronze_age_research = bronze_age_research.union(blacksmith_bronze_age_research)

iron_age_research = copy(bronze_age_research).union(blacksmith_iron_age_research)
# Add an iron version for every bronze research at the blacksmith.

research_string_to_class = dict((r.name, r) for r in iron_age_research)

# The module input_handling/research.py needs sets of strings though
stone_age_research = set(r.name for r in stone_age_research)
bronze_age_research = set(r.name for r in bronze_age_research)
iron_age_research = set(r.name for r in iron_age_research)


for name in research_string_to_class:
    research_obj = research_string_to_class[name]
    assert name == research_obj.name

