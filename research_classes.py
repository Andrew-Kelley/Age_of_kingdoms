from resources import Resources, Food, Wood, Stone, Bronze, Gold, Iron


# Whenever a player begins researching something at some building, an instance of a subclass of
# ResearchObject is created.
class ResearchObject:
    # The following should always be overridden by each subclass
    num_turns_to_completion = 30
    cost = Resources({Wood: 1000, Stone: 1000, Bronze: 1000, Gold: 1000, Iron: 1000})

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

    def research_completed(self, player):
        player.age = 'bronze age'
        player.things_researched.add(BronzeAge)


class IronAge(ResearchObject):
    num_turns_to_completion = 8
    cost = Resources({Food: 500, Gold: 300, Bronze: 300})

    def research_completed(self, player):
        player.age = 'iron age'
        player.things_researched.add(IronAge)

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

    def research_completed(self, player):
        pass


class BronzeSwords(ResearchObject):
    num_turns_to_completion = 3
    cost = Resources({Bronze: 140, Gold: 55})

    def research_completed(self, player):
        pass


# Maybe the following is too broad. I should perhaps have different research armor items for
# archers than for the rest.
# class BronzeArmor(ResearchObject):
#     pass


class BronzeShields(ResearchObject):
    num_turns_to_completion = 3
    cost = Resources({Bronze: 150, Gold: 60})

    def research_completed(self, player):
        pass


class BronzeAxes(ResearchObject):
    num_turns_to_completion = 2
    cost = Resources({Bronze: 130, Gold: 20})

    def research_completed(self, player):
        pass


class BronzePicks(ResearchObject):
    num_turns_to_completion = 2
    cost = Resources({Bronze: 130, Gold: 20})

    def research_completed(self, player):
        pass


####################################

research_string_to_class = {'bronze age': BronzeAge, 'iron age': IronAge,
                            'bronze tipped spears': BronzeTippedSpears, 'bronze swords': BronzeSwords,
                            'bronze shields': BronzeShields, 'bronze axes': BronzeAxes,
                            'bronze picks': BronzePicks}
