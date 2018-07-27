from buildings.bldng_class import Building

class Farm(Building):
    cost = {'wood':100, 'food':20}
    size = (2, 2)
    letter_abbreviation = 'F'
    kind = 'farms'

class LumberCamp(Building):
    cost = {'wood':100}
    size = (2, 2)
    letter_abbreviation = 'L'
    kind = 'lumbercamps'

class StoneQuarry(Building):
    cost = {'wood':100}
    size = (2, 2)
    letter_abbreviation = 'Q'
    kind = 'stonequarries'

class MiningCamp(Building):
    cost = {'wood':100}
    size = (2, 2)
    letter_abbreviation = 'M'
    kind = 'miningcamps'