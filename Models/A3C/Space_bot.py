import random
import math
import players
from pynput.keyboard import Key, Controller

#Neuron class that contains a weight for each neuron in the previous layer and a bias for this neuron
#Weights are a multiplier to the value of the neuron in the previous layer
#Bias is a constant that is added to the sum of the weights that acts as a threshold for when the neuron fires
class Neuron():
    def __init__(self, my_upstream):
        self.upstream = my_upstream
        self.weights = []
        if self.upstream is not None:
            self.weights = [random.uniform(-2.0, 2.0) for _ in range(len(my_upstream.layer))]
        self.value = 0.0
        self.bias = random.uniform(-2.0, 2.0)

    def get_upstream(self):
        return self.upstream

    def set_upstream(self, upstream):
        self.upstream = upstream

    def get_weights(self):
        return self.weights

    def set_weights(self, weights):
        self.weights = weights

    def get_weight_at(self, index):
        return self.weights[index]

    def set_weight_at(self, index, value):
        self.weights[index] = value
#Each upper neuron is multiplied by its corresponding weight and then adds the bias
#The value is then smooshed by the sigmoid function back between 0 and 1
    def calc_value(self):
        self.value = sigmoid(
            (sum(self.weights[i] * self.upstream.layer[i].value for i in range(len(self.weights)))+ self.bias)/len(self.weights))


#Sigmoid function is a mathematical function that smooshes any number between 0 and 1
# 0 becomes 0.5, -1 becomes 0.27, 1 becomes 0.73, -2 becomes 0.12, 2 becomes 0.88,  etc.

def sigmoid(x):
    if x >= 0:
        z = math.exp(-x)
        return 1 / (1 + z)
    else:
        z = math.exp(x)
        return z / (1 + z)
#Wrapper class for the neurons

class NeuronLayer:
    def __init__(self, neuron_count, upstream):
        self.layer = [None] * neuron_count
        for i in range(neuron_count):
            self.layer[i] = Neuron(upstream)

    def calc_layer(self):
        for neuron in self.layer:
            neuron.calc_value()


    def get_values(self):
        return [neuron.value for neuron in self.layer]

#Space_bot is the class that contains the neural network and the methods to train it
class Space_bot:
    def __init__(self, layer_count, my_neuron_count, subject):
        self.observer = players(subject)
        self.neuron_count = my_neuron_count
#The input layer is the layer that listens to in game variables
        self.input_layer = None
#The hidden layers are the layers that are in between the input and output layers
        self.hidden_layers = [layer_count]
#The output layer is the layer that outputs a decision and presses the corresponding keys
        self.output_layer = None
        self.choice = 0
#Learning rate is the flat random range amount that each weight and bias is changed by
        self.learning_rate = 0.1
#Initializes the input neurons
    def set_inputs(self, input_vars):
        if self.input_layer is None:
            self.input_layer = NeuronLayer(len(input_vars), None)

        for i in range(len(input_vars) - 1):
            self.input_layer.layer[i].value = input_vars[i]
        return self.input_layer.layer
#Ininitalizes the hidden layers and output layer
    def set_layers(self):
        self.hidden_layers[0] = NeuronLayer(self.neuron_count, self.input_layer)
        for i in range(len(self.hidden_layers) - 1):
            self.hidden_layers[i + 1] = NeuronLayer(self.neuron_count, self.hidden_layers[i])
        self.output_layer = NeuronLayer(4, self.hidden_layers[len(self.hidden_layers) - 1])
    def add_score(self, score):
        self.round += 1
        self.total_score += score
        return self.total_score
    def in_out(self):
        s = ""
        for i in range(len(self.input_layer.layer)):
            s+=" "+str(self.input_layer.layer[i].value)
        print(s)
        s = ""
        for i in range(len(self.hidden_layers[0].layer)):
            s+=" "+str(self.hidden_layers[0].layer[i].value)
        print(s)
#Prints the weights of the current neural network
    def draw_network(self):
        for i in range(len(self.hidden_layers)):
            lay = ""
            for j in range(len(self.hidden_layers[i].layer)):
                s = ""
                for k in range(len(self.hidden_layers[i].layer[j].weights)):
                    s += str(round(self.hidden_layers[i].layer[j].get_weight_at(k) * 100) / 100) + " "
                lay += ("(" + str(i) + "_" + str(j) + "): " + s)
            print(lay)
        o = "out :"
        for i in range(len(self.output_layer.layer)):
            s = ""
            for j in range(len(self.output_layer.layer[i].weights)):
                s += str(round(self.output_layer.layer[i].get_weight_at(j) * 100) / 100) + " "
            o += ("(" + str(i) + "): " + s)
        print(o)
#Takes in the inputs, caluculates each neuron's value, and then chooses the move with the highest value
#Rather than {Left, Right, Shoot}, I switched to having {Left and Shoot, Right and Shoot, Right and don't Shoot, Left and don't Shoot}
    def choose_move(self, inputs):
        for inp in inputs:
            self.input_layer.layer[inputs.index(inp)].value = inp
        keyboard = Controller()
        for hiddenLayer in self.hidden_layers:
            hiddenLayer.calc_layer()
        c_max = 0.0

        i = 0
        for output in self.output_layer.layer:
            output.calc_value()
            if output.value > c_max:
                c_max = output.value
                self.choice = i
            i += 1

        if not self.training:
            keyboard.release(Key.left)
            keyboard.release(Key.right)
            keyboard.release(Key.space)
            if self.choice == 0:
                keyboard.press(Key.left)
                keyboard.press(Key.space)
            elif self.choice == 1:
                keyboard.press(Key.right)
                keyboard.press(Key.space)
            elif self.choice == 2:
                keyboard.press(Key.right)
            elif self.choice == 3:
                keyboard.press(Key.left)
    
    #Takes the bot and creates a child copy of it with slight mutations to each weight and bias
    def split_bot(self):
        copy = Space_bot(len(self.hidden_layers), self.neuron_count)
        copy.set_inputs([0.0]*12)
        copy.set_layers()
        for i in range(len(self.hidden_layers)):
            for j in range(len(self.hidden_layers[i].layer)):
                for k in range(len(self.hidden_layers[i].layer[j].weights)):
                    copy.hidden_layers[i].layer[j].set_weight_at(k, self.hidden_layers[i].layer[j].get_weight_at(k)+random.uniform(-learning_rate, learning_rate))
                    copy.hidden_layers[i].layer[j].bias = self.hidden_layers[i].layer[j].bias + random.uniform(-learning_rate, learning_rate)
        for i in range(len(self.output_layer.layer)):
            for j in range(len(self.output_layer.layer[i].weights)):
                copy.output_layer.layer[i].set_weight_at(j, self.output_layer.layer[i].get_weight_at(j)+random.uniform(-learning_rate, learning_rate))
                copy.output_layer.layer[i].bias = self.output_layer.layer[i].bias + random.uniform(-learning_rate, learning_rate)
        return copy
