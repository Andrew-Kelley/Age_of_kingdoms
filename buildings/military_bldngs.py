# This includes all buildings that produce military units

from buildings.bldng_class import Building

class Barracks(Building):
    size = (3, 3)
    letter_abbreviation = 'B'


class ArcheryRange(Building):
    size = (5, 3)
    letter_abbreviation = 'A'

class Stable(Building):
    size = (3, 3)
    letter_abbreviation = 'S'

class SiegeWorks(Building):
    size = (3, 3)
    letter_abbreviation = 'W'