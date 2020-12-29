from units.mltry_unit_clss import MilitaryUnit


class Knight(MilitaryUnit):
    kind = 'knights'
    letter_abbreviation = 'k'


class ChampionKnight(Knight):
    # Can only be built after researching level 3 knight
    pass
