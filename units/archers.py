from units.unit_and_villager import Unit


class Archer(Unit):
    kind = 'archers'
    letter_abbreviation = 'a'


class ChampionArcher(Archer):
    # Can only be built after researching level 3 archers
    pass
