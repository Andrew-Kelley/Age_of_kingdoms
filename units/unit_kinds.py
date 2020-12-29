unit_kinds = ['villagers', 'pikemen', 'swordsmen', 'archers', 'knights',
              'batteringrams', 'catapults', 'trebuchets', 'merchants']

unit_kinds_singular = ['villager', 'pikeman', 'swordsman',
                       'archer', 'knight', 'batteringram',
                       'catapult', 'trebuchet', 'merchant']

unit_kind_to_singular = {'villagers': 'villager',
                         'pikemen': 'pikeman',
                         'swordsmen': 'swordsman',
                         'archers': 'archer',
                         'knights': 'knight',
                         'batteringrams': 'batteringram',
                         'catapults': 'catapult',
                         'trebuchets': 'trebuchet',
                         'units': 'unit',
                         'merchants': 'merchant'}

# In case I change units or unit_kinds and forget to change the other:
assert len(unit_kinds_singular) == len(unit_kinds)

unit_singular_to_plural = dict((s, p) for s, p in zip(unit_kinds_singular, unit_kinds))
