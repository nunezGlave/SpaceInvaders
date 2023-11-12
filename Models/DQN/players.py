import numpy as np
import tensorflow as tf
from tf_agents.agents.dqn import dqn_agent
from tf_agents.networks import q_network
from tf_agents.utils import common
from tf_agents.environments import tf_py_environment
from tf_agents.environments import wrappers
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.policies import random_tf_policy


class DQNAgent:
    def __init__(self, game_instance, train_env, eval_env):
        self.game_instance = game_instance

        self.train_env = tf_py_environment.TFPyEnvironment(train_env)
        self.eval_env = tf_py_environment.TFPyEnvironment(eval_env)

        self.q_net = q_network.QNetwork(
            self.train_env.observation_spec(),
            self.train_env.action_spec(),
            fc_layer_params=(100,))

        self.optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=1e-3)

        self.agent = dqn_agent.DqnAgent(
            self.train_env.time_step_spec(),
            self.train_env.action_spec(),
            q_network=self.q_net,
            optimizer=self.optimizer,
            td_errors_loss_fn=common.element_wise_squared_loss,
            train_step_counter=tf.Variable(0))

        self.agent.initialize()

        self.eval_policy = self.agent.policy
        self.collect_policy = self.agent.collect_policy
        self.random_policy = random_tf_policy.RandomTFPolicy(
            self.train_env.time_step_spec(),
            self.train_env.action_spec())

        self.replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
            data_spec=self.agent.collect_data_spec,
            batch_size=self.train_env.batch_size,
            max_length=100000)

    def send_command(self, command):
        self.game_instance.command(command)

    def update(self, player_x, enemies, bullets):
        time_step = self.train_env.current_time_step()
        action_step = self.collect_policy.action(time_step)

        if action_step.action == 0:
            self.send_command("left")
        elif action_step.action == 1:
            self.send_command("right")
        elif action_step.action == 2:
            self.send_command("shoot")
