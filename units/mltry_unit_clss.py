from units.unit_and_villager import Unit
from units.aggression_level import DEFEND


class MilitaryUnit(Unit):
    def __init__(self, building, player, position=None):
        Unit.__init__(self, building, player, position)
        self.aggression_lvl = DEFEND
