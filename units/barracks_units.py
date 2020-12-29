from units.unit_and_villager import Unit


# Unless pikemen are significantly weaker than Swordsman, I think that the cost
# difference between Pikeman and Swordsman will result in many more
# Pikeman being built at the beginning of the game.
# I think that this is OK.
# I intend Pikeman to only be somewhat weaker than Swordsman
class Pikeman(Unit):
    """A man with a spear and a shield"""
    kind = 'pikemen'
    letter_abbreviation = 'p'


class Swordsman(Unit):
    # After reaching the Bronze Age, before being able to train Swordsman,
    # two things must first be researched at the Blacksmith:
    # (a) bronze shields, and (b) bronze swords.
    # The first of these also benefits Pikeman (by upgrading their
    # armor to bronze).
    kind = 'swordsmen'
    letter_abbreviation = 's'


class ChampionSwordsman(Swordsman):
    # Can only be built after researching level 3 swordsman
    pass
