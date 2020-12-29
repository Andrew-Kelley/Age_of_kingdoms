# This includes all buildings that produce military units

from buildings.bldng_class import Building
from resources import Resources, Wood
from units.barracks_units import Pikeman, Swordsman
from units.archers import Archer
from research_classes import BronzeShields, BronzeSwords

class Barracks(Building):
    cost = Resources({Wood: 150})
    size = (3, 3)
    letter_abbreviation = 'B'
    kind = 'barracks'
    time_to_build = 50

    def units_which_can_be_built(self):
        """Returns a list of unit kind strings."""
        what_can_be_built = [Pikeman.kind]
        player = self.player
        if player.age in ('bronze age', 'iron age'):
            shields = BronzeShields
            swords = BronzeSwords
            if all(s.name in player.things_researched for s in (shields, swords)):
                what_can_be_built.append(Swordsman.kind)
        return what_can_be_built

    def build_unit(self, unit_type):
        player = self.player
        if unit_type not in self.units_which_can_be_built():
            # This should never happen because the function units_which_can_be_built
            # is called in in the command_handling/insert_commands.py (in the
            # function insert_build_unit_command)
            print("Error! unit_type is not in self.units_which_can_be_built()")
            return

        if unit_type == Pikeman.kind:
            Pikeman(self, player)
        else:
            Swordsman(self, player)


class ArcheryRange(Building):
    cost = Resources({Wood: 150})
    size = (5, 3)
    letter_abbreviation = 'A'
    kind = 'archeryrange'
    time_to_build = 50

    def units_which_can_be_built(self):
        return ['archers']

    def build_unit(self, unit_type):
        player = self.player
        if unit_type != 'archers':
            # This should never happen.
            print("Error! An ArcheryRange is trying to build a non-archer.")
            return

        Archer(self.build_position, player)


class Stable(Building):
    cost = Resources({Wood: 150})
    size = (3, 3)
    letter_abbreviation = 'S'
    kind = 'stable'
    time_to_build = 50

    def units_which_can_be_built(self):
        return []


class SiegeWorks(Building):
    cost = Resources({Wood: 150})
    size = (3, 3)
    letter_abbreviation = 'W'
    kind = 'siegeworks'
    time_to_build = 50

    def units_which_can_be_built(self):
        return []
