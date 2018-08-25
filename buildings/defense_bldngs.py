from buildings.bldng_class import Building
from resources import Resources, Wood, Stone

class WoodWall(Building):
    size = (1, 1)
    letter_abbreviation = '.'

class WoodGate(Building):
    letter_abbreviation = 'G'

class WoodGateEastWest(WoodGate):
    size = (1, 4)

class WoodGateNorthSouth(WoodGate):
    size = (4, 1)

class StoneWall(Building):
    size = (1, 1)
    letter_abbreviation = '*'

class StoneGate(Building):
    letter_abbreviation = 'G'

class StoneGateEastWest(StoneGate):
    size = (1, 4)

class StoneGateNorthSouth(StoneGate):
    size = (4, 1)

class WallFortification(Building):
    letter_abbreviation = 'F'

class WallFortificationEastWest(WallFortification):
    size = (1, 3)

class WallFortificationNorthSouth(WallFortification):
    size = (3, 1)

class Tower(Building):
    cost = Resources({Wood: 30, Stone: 130})
    size = (2, 2)
    letter_abbreviation = 'T'
    kind = 'tower'
    time_to_build = 50

class Castle(Building):
    cost = Resources({Wood: 150, Stone: 700})
    size = (5, 5)
    letter_abbreviation = 'C'
    kind = 'castle'
    time_to_build = 250