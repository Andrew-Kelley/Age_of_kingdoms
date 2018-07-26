# This includes all buildings that produce military units

from buildings.bldng_class import Building

class Barracks(Building):
    size = (3, 3)
    letter_abbreviation = 'B'
    kind = 'barracks'


class ArcheryRange(Building):
    size = (5, 3)
    letter_abbreviation = 'A'
    kind = 'archeryranges'

class Stable(Building):
    size = (3, 3)
    letter_abbreviation = 'S'
    kind = 'stables'

class SiegeWorks(Building):
    size = (3, 3)
    letter_abbreviation = 'W'
    kind = 'siegeworks'