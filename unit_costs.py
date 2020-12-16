from resources import Resources, Food, Wood, Gold, Bronze, Iron
from unit_kinds import unit_kinds

unit_costs = dict()

# The following two lines are just a place holder and should be deleted once I decide
# what each unit will cost.
for kind in unit_kinds:
    unit_costs[kind] = Resources({Food: 400, Wood: 400, Gold: 400, Bronze: 400})

unit_costs['villagers'] = Resources({Food: 50})

unit_costs['pikemen'] = Resources({Food: 40, Wood: 20})

unit_costs['swordsmen'] = Resources({Food: 40, Gold: 25, Bronze: 15})

unit_costs['archers'] = Resources({Wood: 40, Gold: 20, Bronze: 10})
