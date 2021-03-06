from input_handling.get_input import input_number_of_players
from player import Player, initial_position_of_player
from map_etc.make_map import game_map

# Only from index 1 and on will players contain the actual players
players = [None]

def initialize_players():
    global players
    # For now, there will be no computer players:
    num_hmn_plyrs = input_number_of_players(human=True)
    num_cmptr_plyrs = 0  # = input_number_of_players(human=False)
    print("Starting a game with {} human player(s) and {} "
          "computer player(s).".format(num_hmn_plyrs, num_cmptr_plyrs))

    # The actual players are listed starting at index 1.
    # Thus players[i] == player number i.
    for i in range(1, num_hmn_plyrs + 1):
        initial_position = initial_position_of_player(i, game_map)
        players.append(Player(number=i, position=initial_position, is_human=True))
    for i in range(num_hmn_plyrs + 1, num_hmn_plyrs + num_cmptr_plyrs + 1):
        initial_position = initial_position_of_player(i, game_map)
        players.append(Player(number=i, position=initial_position, is_human=False))

    for player in players[1:]:
        print("Is player number {} human? {}".format(player.number, player.is_human))


if __name__ == '__main__':
    # Testing the neighbors method of the Position class
    from map_etc.position import Position

    def print_neighbors_of(position):
        for neighbor in position.neighbors(game_map):
            print(neighbor)

    position = Position(80, 79)
    print("Before any buildings are built, here are neighbors of")
    print("position ", position)
    print_neighbors_of(position)

    initialize_players()
    print("After initializing the players, here are the neighbors:")
    print_neighbors_of(position)

    P = Position
    for position in (P(76, 79), P(77,79), P(76, 84), P(81, 82), P(78, 84)):
        print("The neighbors of ", position, " are ")
        print_neighbors_of(position)
        print()