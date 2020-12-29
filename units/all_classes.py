from units.unit_and_villager import Villager
from units.barracks_units import Pikeman, Swordsman
from units.archers import Archer
from units.knights import Knight
from units.merchant import Merchant
from units.siege_units import Catapult, BatteringRam, Trebuchet

from units.unit_kinds import unit_kinds

unit_classes = [Villager, Pikeman, Swordsman, Archer, Knight, BatteringRam,
                Catapult, Trebuchet, Merchant]

assert len(unit_kinds) == len(unit_classes)

unit_kind_to_class = dict((k, c) for k, c in zip(unit_kinds, unit_classes))
