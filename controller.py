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

    def mutate(self, drift):
        """Performs a mutation by randomly altering each parameter in the net.

        @param drift scales the size of mutation to apply
        """
        for i in range(self.net.params.size):
            self.net.params[i] += (random.random() - 1) * drift


def run_game(cont):
    """Runs a game and returns the score.

    @param cont: the controller to test
    @return the score of the game
    """
    g = game.Game()

    while g.get_playing():
        input_list = [item for sub in g.grid for item in sub]
        decision = cont.net.activate(input_list)
        for i in range(4):
            direction = where(decision == max(decision))[0][0]
            if g.test_move(game.moves[direction]):
                g.make_move(game.moves[direction])
                break
            else:
                decision[direction] = -100000

    return g.get_score()


def get_fitness(cont):
    """
    Runs several games to get an average score for the fitness.

    @param cont: the controller to test
    @return fitness: the average score
    """
    if get_num() == 0:
        raise ValueError("The number of games to average fitness over has not been set.")
    fitness = 0
    for i in range(get_num()):
        fitness += run_game(cont)
    fitness /= get_num()
    return fitness

num = 0


def set_num(n):
    """
    Sets the number of games to average fitness over.

    @param n: the number of games
    """
    global num
    num = n


def get_num():
    """
    Returns the number of games to average fitness over.
    @return: the number of games
    """
    return num
