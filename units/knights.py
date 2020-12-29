from units.unit_and_villager import Unit


class Knight(Unit):
    kind = 'knights'
    letter_abbreviation = 'k'


class ChampionKnight(Knight):
    # Can only be built after researching level 3 knight
    pass
