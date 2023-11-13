''' Created by Clark '''
import random
import math

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
    bot_count = 0
    space_bots = [None]*4
    generation = 0
    def __init__(self, layer_count, my_neuron_count, subject):
        self.observer = subject
        self.neuron_count = my_neuron_count
#The input layer is the layer that listens to in game variables
        self.input_layer = None
#The hidden layers are the layers that are in between the input and output layers
        self.hidden_layers = [layer_count]
#The output layer is the layer that outputs a decision and presses the corresponding keys
        self.output_layer = None
        self.choice = 0
#Learning rate is the flat random range amount that each weight and bias is changed by
        self.learning_rate = 0.2
        self.score = 0
        self.index = Space_bot.bot_count
        Space_bot.space_bots[self.index] = self
        Space_bot.bot_count += 1
        self.playing = True

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
        if self.choice == 0:
            self.observer.send_command("left")
            self.observer.send_command("shoot")
        elif self.choice == 1:
            self.observer.send_command("right")
            self.observer.send_command("shoot")
        elif self.choice == 2:
            self.observer.send_command("right")
        elif self.choice == 3:
            self.observer.send_command("left")
    
    #Takes the bot and creates a child copy of it with slight mutations to each weight and bias
    def split_bot(self, observer):
        self.learning_rate = abs(2000-self.score/2000)
        copy = Space_bot(len(self.hidden_layers), self.neuron_count, observer)
        copy.set_inputs([0.0]*3)
        copy.set_layers()
        for i in range(len(self.hidden_layers)):
            for j in range(len(self.hidden_layers[i].layer)):
                for k in range(len(self.hidden_layers[i].layer[j].weights)):
                    copy.hidden_layers[i].layer[j].set_weight_at(k, self.hidden_layers[i].layer[j].get_weight_at(k)+random.uniform(-self.learning_rate, self.learning_rate))
                    copy.hidden_layers[i].layer[j].bias = self.hidden_layers[i].layer[j].bias + random.uniform(-self.learning_rate, self.learning_rate)
        for i in range(len(self.output_layer.layer)):
            for j in range(len(self.output_layer.layer[i].weights)):
                copy.output_layer.layer[i].set_weight_at(j, self.output_layer.layer[i].get_weight_at(j)+random.uniform(-self.learning_rate, self.learning_rate))
                copy.output_layer.layer[i].bias = self.output_layer.layer[i].bias + random.uniform(-self.learning_rate, self.learning_rate)
        return copy
    def end_game(self,score):
        self.playing = False
        gameOver = True
        for bot in Space_bot.space_bots:
            if bot.playing:
                gameOver = False
        if gameOver:
            highest_score = 0
            winner = self
            for bot in Space_bot.space_bots:
                if bot.score > highest_score:
                    highest_score = bot.score
                    winner = bot
            print("Gen ["+str(Space_bot.generation)+"] Winner: " + str(winner.index)+ " Score: " + str(winner.score))
            Space_bot.generation += 1
            Old_bots = Space_bot.space_bots
            Space_bot.space_bots = [None] * 4
            Space_bot.bot_count = 0
            for bot in Old_bots:
                bot.observer.space_bot = winner.split_bot(bot.observer)
                bot.observer.space_bot.index = bot.index
                Space_bot.space_bots[bot.index] = bot.observer.space_bot
            self.observer.send_command("reset")


