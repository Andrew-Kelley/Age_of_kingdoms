from buildings.bldng_class import Building
from resources import Resources, Wood, Food


class Farm(Building):
    cost = Resources({Wood: 100, Food: 20})
    size = (2, 2)
    letter_abbreviation = 'F'
    kind = 'farm'
    time_to_build = 20


class LumberCamp(Building):
    cost = Resources({Wood: 100})
    size = (2, 2)
    letter_abbreviation = 'L'
    kind = 'lumbercamp'
    time_to_build = 30


class StoneQuarry(Building):
    cost = Resources({Wood: 100})
    size = (2, 2)
    letter_abbreviation = 'Q'
    kind = 'stonequarry'
    time_to_build = 30


class MiningCamp(Building):
    cost = Resources({Wood: 100})
    size = (2, 2)
    letter_abbreviation = 'M'
    kind = 'miningcamp'
    time_to_build = 30
