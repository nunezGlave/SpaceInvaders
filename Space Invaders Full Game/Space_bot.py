import random
import math
from pynput.keyboard import Key, Controller

def sigmoid(x):
    if x >= 0:
        z = math.exp(-x)
        return 1 / (1 + z)
    else:
        z = math.exp(x)
        return z / (1 + z)
class Space_bot:
    def __init__(self, layer_count, my_neuron_count):
        self.neuron_count = my_neuron_count
        self.input_layer = None
        self.hidden_layers = [layer_count]
        self.output_layer = None
        self.round = 0
        self.total_score = 0
        self.choice = 0
        self.learning_rate = 0.01
        self.training = False
        self.net = None
        self.rate = 0.0
        self.right = 0
    def set_rate(self, chosen):
        self.round += 1
        if self.choice == chosen:
            self.right += 1
        self.rate = self.right/self.round
        print(self.rate)
    def set_inputs(self, input_vars):
        if self.input_layer is None:
            self.input_layer = NeuronLayer(len(input_vars), None)

        for i in range(len(input_vars) - 1):
            self.input_layer.layer[i].value = input_vars[i]

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
       # self.in_out()
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
    def split_bot(self):
        copy = Space_bot(len(self.hidden_layers), self.neuron_count)
        copy.set_inputs([0.0]*12)
        copy.set_layers()
        for i in range(len(self.hidden_layers)):
            for j in range(len(self.hidden_layers[i].layer)):
                for k in range(len(self.hidden_layers[i].layer[j].weights)):
                    copy.hidden_layers[i].layer[j].set_weight_at(k, self.hidden_layers[i].layer[j].get_weight_at(k)+random.uniform(-.1, .1))
                    copy.hidden_layers[i].layer[j].bias = self.hidden_layers[i].layer[j].bias + random.uniform(-.1, .1)
        for i in range(len(self.output_layer.layer)):
            for j in range(len(self.output_layer.layer[i].weights)):
                copy.output_layer.layer[i].set_weight_at(j, self.output_layer.layer[i].get_weight_at(j)+random.uniform(-.1, .1))
                copy.output_layer.layer[i].bias = self.output_layer.layer[i].bias + random.uniform(-.1, .1)
       # copy.draw_network()
        return copy
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


class Neuron():
    def __init__(self, my_upstream):
        self.rect = self.image.get_rect(topleft=(375, 540))
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

    def calc_value(self):
      #  print(self.value)
        self.value = sigmoid(
            (sum(self.weights[i] * self.upstream.layer[i].value for i in range(len(self.weights)))+ self.bias)/len(self.weights))
      #  print(self.value)
    def update(self):
        self.rect.x = 375
        self.rect.y = 540
