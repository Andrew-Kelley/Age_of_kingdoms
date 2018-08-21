# This includes all buildings that produce military units

from buildings.bldng_class import Building
from resources import Resources, Wood
from units import Pikeman, Swordsman, Archer
from command_handling import insert_move_later_command

class Barracks(Building):
    cost = Resources({Wood: 150})
    size = (3, 3)
    letter_abbreviation = 'B'
    kind = 'barracks'
    time_to_build = 50

    def units_which_can_be_built(self, player):
        ls = ['pikemen']
        if player.age in ('bronze age', 'iron age'):
            pass
            # if <player has researched bronze shields and bronze swords>:
            #     ls.append('swordsmen')
        return ls

    def build_unit(self, player, unit_type):
        # TODO: Update this function so as to include where newly built units must go.
        if unit_type not in self.units_which_can_be_built(player):
            # This should never happen because the function units_which_can_be_built is called
            # in in the command_handling.py module (in the function insert_build_unit_command)
            return

        unit_number = len(player.units[unit_type])
        if unit_type == 'pikemen':
            # The unit's initial position may be changed later in this function
            new_unit = Pikeman(unit_number, self.build_position)
            player.resources -= Pikeman.cost
        else:
            # The unit's initial position may be changed later in this function
            new_unit = Swordsman(unit_number, self.build_position)
            player.resources -= Swordsman.cost

        # The following changes (possibly) the build position of new_unit
        #
        # I don't want this to be a Building method because to do so, the bldng_class.py module
        # would have to import insert_move_later_command from the command_handling.py module,
        # but I cannot do this since command_handling.py already imports the Building class.
        delta = self.build_position - self.position
        if delta.magnitude > 6:
            delta1, delta2 = delta.beginning_plus_the_rest(distance_in_one_turn=6)
            build_position = self.position + delta1
            new_unit.position = build_position
            command = ['move', [new_unit], delta2]
            insert_move_later_command(player, command)

        player.units[unit_type].append(new_unit)



class ArcheryRange(Building):
    cost = Resources({Wood: 150})
    size = (5, 3)
    letter_abbreviation = 'A'
    kind = 'archeryrange'
    time_to_build = 50

    def units_which_can_be_built(self, player):
        return ['archers']

    def build_unit(self, player, unit_type):
        if unit_type != 'archers':
            # This should never happen.
            return

        unit_number = len(player.units[unit_type])
        new_archer = Archer(unit_number, self.build_position)
        player.units[unit_type].append(new_archer)
        player.resources -= Archer.cost


class Stable(Building):
    cost = Resources({Wood: 150})
    size = (3, 3)
    letter_abbreviation = 'S'
    kind = 'stable'
    time_to_build = 50

    def units_which_can_be_built(self, player):
        return []


class SiegeWorks(Building):
    cost = Resources({Wood: 150})
    size = (3, 3)
    letter_abbreviation = 'W'
    kind = 'siegeworks'
    time_to_build = 50

    def units_which_can_be_built(self, player):
        return []
