from units.mltry_unit_clss import MilitaryUnit


class Archer(MilitaryUnit):
    kind = 'archers'
    letter_abbreviation = 'a'


class ChampionArcher(Archer):
    # Can only be built after researching level 3 archers
    pass
