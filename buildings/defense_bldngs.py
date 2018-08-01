from buildings.bldng_class import Building

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
    size = (2, 2)
    letter_abbreviation = 'T'
    kind = 'tower'

class Castle(Building):
    size = (5, 5)
    letter_abbreviation = 'C'
    kind = 'castle'