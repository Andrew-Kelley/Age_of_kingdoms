from units.mltry_unit_clss import MilitaryUnit


class SiegeUnit(MilitaryUnit):
    pass


class BatteringRam(SiegeUnit):
    kind = 'batteringrams'
    letter_abbreviation = 'r'


class Catapult(SiegeUnit):
    kind = 'catapults'
    letter_abbreviation = 'c'


class Trebuchet(SiegeUnit):
    kind = 'trebuchets'
    letter_abbreviation = 't'
