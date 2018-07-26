from buildings.bldng_class import Building

class Farm(Building):
    size = (2, 2)
    letter_abbreviation = 'F'
    kind = 'farms'

class LumberCamp(Building):
    size = (2, 2)
    letter_abbreviation = 'L'
    kind = 'lumbercamps'

class StoneQuarry(Building):
    size = (2, 2)
    letter_abbreviation = 'Q'
    kind = 'stonequarries'

class MiningCamp(Building):
    size = (2, 2)
    letter_abbreviation = 'M'
    kind = 'miningcamps'