# This includes all buildings that produce military units

from buildings.bldng_class import Building
from resources import Resources, Wood


class Barracks(Building):
    cost = Resources({Wood: 150})
    size = (3, 3)
    letter_abbreviation = 'B'
    kind = 'barracks'

    def units_which_can_be_built(self, player):
        ls = ['pikemen']
        if player.age in ('Bronze Age', 'Iron Age'):
            pass
            # if <player has researched bronze shields and bronze swords>:
            #     ls.append('swordsmen')
        return ls


class ArcheryRange(Building):
    cost = Resources({Wood: 150})
    size = (5, 3)
    letter_abbreviation = 'A'
    kind = 'archeryrange'

    def units_which_can_be_built(self, player):
        return ['archers']


class Stable(Building):
    cost = Resources({Wood: 150})
    size = (3, 3)
    letter_abbreviation = 'S'
    kind = 'stable'

    def units_which_can_be_built(self, player):
        return []


class SiegeWorks(Building):
    cost = Resources({Wood: 150})
    size = (3, 3)
    letter_abbreviation = 'W'
    kind = 'siegeworks'

    def units_which_can_be_built(self, player):
        return []
