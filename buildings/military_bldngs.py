# This includes all buildings that produce military units

from buildings.bldng_class import Building
from resources import Resources, Wood
from units import Pikeman, Swordsman, Archer
from research_classes import BronzeShields, BronzeSwords
from command_handling.insert_commands import insert_move_later_command
from command_handling.commands import MoveCmd

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
            # is called in in the command_handling.py module (in the function
            # insert_build_unit_command)
            return

        if unit_type == Pikeman.kind:
            # The unit's initial position may be changed later in this function
            new_unit = Pikeman(self.build_position, player)
        else:
            # The unit's initial position may be changed later in this function
            new_unit = Swordsman(self.build_position, player)

        # If self.build_position is too far away, then the unit will not start
        # its existence that far away.
        set_unit_position_and_movement(self, new_unit, player, distance=6)


def set_unit_position_and_movement(building, new_unit, player, distance):
    """If the new_unit also requires to be initialized with a move command, then
    this function handles that too."""
    delta = building.build_position - building.position
    if delta.magnitude > 6:
        delta1, delta2 = delta.beginning_plus_the_rest(distance_in_one_turn=distance)
        build_position = building.position + delta1
        new_unit.position = build_position
        command = MoveCmd()
        command.add_unit_with_delta(new_unit, delta2)
        insert_move_later_command(player, command)


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
            return

        new_archer = Archer(self.build_position, player)
        set_unit_position_and_movement(self, new_archer, player, distance=6)


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
