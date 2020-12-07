# To see which files contain which buildings, see directory_structure.txt

from resources import Resources, Wood, Stone, Bronze
from research_classes import BronzeAge, IronAge
from map_etc.colors import Color

stone_age_buildings = {'house', 'lumbercamp', 'stonequarry', 'miningcamp',
                       'woodwall', 'barracks'}

bronze_age_buildings = {'farm', 'stonewall', 'wallfortification', 'tower',
                        'archeryrange', 'siegeworks', 'blacksmith', 'market'}

iron_age_buildings = {'towncenter', 'castle', 'stable', 'library', 'wonder'}

buildings = stone_age_buildings.union(bronze_age_buildings).union(iron_age_buildings)


class Building:
    # Have a method to handle when a building is being attacked. Also
    # have a method to handle building destruction.
    # Perhaps have a method to handle
    # the buildings which are defensible (i.e. which shoot arrows at attackers
    # if there are units garrisoned in it.
    kind = 'building'
    # The following five attributes should never be accessed.
    size = (2, 2)
    letter_abbreviation = '?'
    cost = Resources({Wood: 1000, Stone: 1000, Bronze: 1000})
    time_to_build = 1000
    # When a building is being built, it links to a BuildingUnderConstruction
    # instance.
    construction_alias = None
    currently_researching_something = False

    def __init__(self, number, position, player):
        """For each player, the first of each building is numbered 1.
        Further buildings built (of the same type) are consecutively numbered.

        position is the south-west (i.e. bottom left) corner of the building."""
        self.player = player
        self.number = number
        self.position = position
        # The following is only relevant for unit-producing buildings. It sets
        # the default position where units are produced as the south-west corner
        # of the building. Even though such units are technically "in" the
        # building, they are not counted as garrisoned.
        self.build_position = position
        # The following is used when villagers build a building:
        self.progress_to_construction = 0
        self.insert_into_building_position_pairs()

    def insert_into_building_position_pairs(self):
        player = self.player
        player.building_position_pairs[self.position] = self

    def __str__(self):
        kind = self.kind.capitalize()
        return '{} {} at position {}'.format(kind, self.number, self.position)

    def units_which_can_be_built(self):
        # This function needs to be re-implemented for every building which
        # produces units.
        return []

    def things_which_can_be_researched(self):
        """Returns a list of strings. This needs to be overridden by
        subclasses."""
        return []

    def research(self, thing_to_be_researched):
        thing = thing_to_be_researched
        player = self.player

        thing.make_progress()

        if thing.progress_to_completion >= thing.num_turns_to_completion:
            if thing.name in player.things_researched:
                # This should never happen.
                return
            thing.research_completed(player)
            if isinstance(thing, BronzeAge) or isinstance(thing, IronAge):
                # Then the special message is handled in the module research_classes.py
                pass
            else:
                player.messages += 'Research completed: {}\n'.format(thing.name)

            # The following condition should always hold:
            if thing.name in player.things_being_currently_researched:
                player.things_being_currently_researched.remove(thing.name)
            else:
                print('Error! Developer message: In the Building method called research'
                      'thing.name was not in player.things_being_currently_researched.')

    def build_unit(self, unit_type):
        """This function (in the Building class) should NEVER be called."""
        print("ERROR! You are trying to build a unit from a building that does not "
              "yet have a build_unit method defined.")
        return

    def change_build_position_to(self, new_position, game_map):
        """Only relevant for unit-producing buildings.
        This function specifies a new position for
        where units built by the building self should begin their existence."""
        # delta = new_position - self.position
        # if delta.magnitude > 15:
        #     # Then newly built units are given a command to move, once they are built
        #     return
        if not new_position.is_on_the_map(game_map):
            print("You must pick a position that is on the map.")
            return
        # TODO: Check that there are no enemy walls between the building's
        # position and the proposed build position
        self.build_position = new_position

    def can_build_on_map(self, position, game_map):
        """Returns True if the building can be built at stated position.

        Recall this from manual.txt: The position of a building is the position
        of its lower right (i.e. south east) corner."""
        x_init, y_init = position.value
        length, height = self.size

        # First check if the building will be placed within the boundaries of the  map:
        if x_init - (length - 1) < 0:
            print('Sorry, building placement too far west.')
            return False
        if x_init  >= game_map.width:
            print('Sorry, building placement too far east.')
            return False
        if y_init < 0:
            print('Sorry, building placement too far south.')
            return False
        if y_init + (height - 1) >= game_map.height:
            print('Sorry, building placement too far north.')
            return False

        # Next, check that there are no obstructions. Buildings are allowed to be built
        # only where there are blank spaces or wood.
        x_final = x_init - length
        y_final = y_init + height
        for x in range(x_init, x_final, -1):
            for y in range(y_init, y_final):
                thing_on_map = game_map.bldngs_n_rsrcs[y][x]
                if thing_on_map != ' ' and not isinstance(thing_on_map, Wood):
                    print('Sorry, there is {} occupying part of '
                          'that space.'.format(thing_on_map))
                    return False
        return True

    def build_on_map(self, position, game_map):
        """This function is called when construction starts
        (so before construction is complete)."""
        x_init, y_init = position.value
        x_final = x_init - self.size[0]
        y_final = y_init + self.size[1]

        # The Color.ENDC is so that the rest of the map isn't also printed in
        # the color player.color
        player = self.player
        letter_in_color = player.color + self.letter_abbreviation + Color.ENDC
        for x in range(x_init, x_final, -1):
            for y in range(y_init, y_final):
                game_map.bldngs_n_rsrcs[y][x] = letter_in_color

    def build_by(self, villager_who_is_building):
        """This function is called multiple times to construct the building."""
        player = self.player
        if self.progress_to_construction >= self.time_to_build:
            # Then another villager already finished building this building.
            return
        villager = villager_who_is_building
        amount = villager.build_amount_per_turn
        self.progress_to_construction += amount
        alias = self.construction_alias
        if isinstance(alias, BuildingUnderConstruction):
            alias.progress_to_construction += amount
        else:
            print("Error! This building under construction has no alias.")
            print("Building:", self)

        if self.progress_to_construction >= self.time_to_build:
            player.buildings[self.kind][self.number] = self
            self.construction_alias = None
            # player.buildings[self.kind].append(self)
            player.messages += 'New building: {}\n'.format(self)

    def compare_to(self, other):
        """For use in testing only."""
        there_is_an_error = False
        if self.position != other.position:
            print("Error: these building's positions don't match.")
            print(self, self.position)
            print(other, other.position)
            there_is_an_error = True
        if self.build_position != other.build_position:
            print("Error: these building's build positions don't match.")
            print(self, self.build_position)
            print(other, other.build_position)
            there_is_an_error = True
        return there_is_an_error


class BuildingUnderConstruction(Building):
    """This is a placeholder to be used until a building is completely built."""

    def __init__(self, bldng_class, number, position, player):
        self.player = player
        self.number = number
        self.position = position
        self.progress_to_construction = 0
        self.time_to_build = bldng_class.time_to_build
        self.kind = bldng_class.kind

    def __str__(self):
        kind = self.kind.capitalize()
        message = '{} {} at position {}'.format(kind, self.number, self.position)
        progress = self.progress_to_construction
        total = self.time_to_build
        message += " under construction with progress {}/{}".format(progress, total)
        return message


if __name__ == '__main__':
    from player import Player
    from map_etc.position import Position


    p1 = Player(1, Position(80, 80), is_human=True)

    bldng = Building(1, Position(70, 80), p1)
    print("Ok folks...printing...")
    print(bldng.letter_abbreviation)
    print("Finished printing.")
