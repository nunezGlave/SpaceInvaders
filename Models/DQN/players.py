import random
import numpy as np
from collections import deque
import torch
import torch.nn as nn
import torch.optim as optim
import pygame


class Human:
    def __init__(self, game_instance):
        self.game_instance = game_instance


    def update(self, player_x, enemies, bullets):
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_LEFT]:
            self.send_command("left")
        if self.keys[pygame.K_RIGHT]:
            self.send_command("right")
        if self.keys[pygame.K_SPACE]:
            self.send_command("shoot")


    def send_command(self, command):
        self.game_instance.command(command)

class DQNNetwork(nn.Module):
    def __init__(self, input_shape, action_space):
        super(DQNNetwork, self).__init__()
        self.fc1 = nn.Linear(input_shape, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, action_space)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)


class DQNAgent:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.state_size = 1  # Define the size of the state
        self.action_size = 3  # "left", "right", "shoot"
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # discount factor
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = DQNNetwork(self.state_size, self.action_size)
        self.optimizer = optim.Adam(
            self.model.parameters(), lr=self.learning_rate)

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        state = torch.tensor(state, dtype=torch.float).unsqueeze(0)
        act_values = self.model(state)
        return torch.argmax(act_values[0]).item()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size=32):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                next_state = torch.tensor(
                    next_state, dtype=torch.float).unsqueeze(0)
                target = (reward + self.gamma *
                          torch.max(self.model(next_state).detach()).item())
            target_f = self.model(torch.tensor(
                state, dtype=torch.float).unsqueeze(0))
            target_f[0][action] = target
            self.optimizer.zero_grad()
            loss = nn.MSELoss()(target_f, self.model(
                torch.tensor(state, dtype=torch.float).unsqueeze(0)))
            loss.backward()
            self.optimizer.step()
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def send_command(self, command):
        if command == "left":
            self.game_instance.move_player_left()
        elif command == "right":
            self.game_instance.move_player_right()
        elif command == "shoot":
            self.game_instance.player_shoot()
