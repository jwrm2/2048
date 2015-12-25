import game
from numpy import where
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import FullConnection
from pybrain.structure import LinearLayer, SigmoidLayer
import random


class Controller(object):
    """A neural net for deciding which step to take next."""

    def __init__(self, grid_size, hidden_list):
        """Sets up the neural network.

        @param grid_size: the size of the grid, for specifying the input layer.
        @param hidden_list: a list containing the number of nodes in each hidden layer.
        """
        self.net = FeedForwardNetwork()

        in_layer = LinearLayer(grid_size*grid_size)
        self.net.addInputModule(in_layer)
        out_layer = LinearLayer(4)
        self.net.addOutputModule(out_layer)

        hidden_layers = []
        for i in hidden_list:
            hidden_layer = SigmoidLayer(i)
            hidden_layers.append(hidden_layer)
            self.net.addModule(hidden_layer)

        self.net.addConnection(FullConnection(in_layer, hidden_layers[0]))
        if len(hidden_layers) > 1:
            for i in range(1, len(hidden_layers) - 1):
                self.net.addConnection(FullConnection(hidden_layers[i], hidden_layers[i+1]))
        self.net.addConnection(FullConnection(hidden_layers[-1], out_layer))

        self.net.sortModules()

    def get_fitness(self, number):
        """
        Runs several games to get an average score for the fitness.

        @param number: number of games to average over
        @return fitness: the average score
        """
        fitness = 0
        for i in range(number):
            fitness += self.run_game()
        fitness /= number
        return fitness

    def mutate(self, drift):
        """Performs a mutation by randomly altering each parameter in the net.

        @param drift scales the size of mutation to apply
        """
        for i in range(self.net.params.size):
            self.net.params[i] += (random.random() - 1) * drift

    def run_game(self):
        """Runs a game and returns the score.

        @return the score of the game
        """
        g = game.Game()

        while g.get_playing():
            input_list = [item for sub in g.grid for item in sub]
            decision = self.net.activate(input_list)
            for i in range(4):
                direction = where(decision == max(decision))[0][0]
                if g.test_move(game.moves[direction]):
                    g.make_move(game.moves[direction])
                    break
                else:
                    decision[direction] = -100000

        return g.get_score()

