from RandomPlayer import RandomPlayer
from EdgePlayer import EdgePlayer
from data_structures.types import GameState
from fortune_algorithm import Voronoi


def main():
    # Instantiate the game state
    state = GameState(m=10, n=5)

    # Initialize a concrete class for player 1 and run the place_points method
    player1 = RandomPlayer(1, state)
    state = player1.place_points

    # Initialize a concrete class for player 2 and run the place_points method
    player2 = RandomPlayer(2, state)
    state = player2.place_points

    # Visualize the result
    voronoi = Voronoi()
    v_diagram = voronoi.create_diagram(state.points)