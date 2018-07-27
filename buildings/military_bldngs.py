# This includes all buildings that produce military units

from buildings.bldng_class import Building
from resources import Resources

class Barracks(Building):
    cost = Resources({'wood':150})
    size = (3, 3)
    letter_abbreviation = 'B'
    kind = 'barracks'


class ArcheryRange(Building):
    cost = Resources({'wood':150})
    size = (5, 3)
    letter_abbreviation = 'A'
    kind = 'archeryranges'

class Stable(Building):
    cost = Resources({'wood':150})
    size = (3, 3)
    letter_abbreviation = 'S'
    kind = 'stables'

class SiegeWorks(Building):
    cost = Resources({'wood':150})
    size = (3, 3)
    letter_abbreviation = 'W'
    kind = 'siegeworks'