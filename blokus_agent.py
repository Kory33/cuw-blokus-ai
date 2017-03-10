"""
A module which provides varieties of dqn agents.
"""

from abc import ABCMeta, abstractmethod

from collections import deque
from itertools import chain

import random

import tensorflow as tf
import numpy as np


class BlokusAgent(object):
    """
    A class which provides common interfaces of blokus game agent.

    Two methods to be implemented by child classes are:
     - get_action(self, game_state, action_space)
     - learn(self, reward, state, is_terminal)
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_action(self, game_state, action_space):
        """
        Get an action, from the given state of the environment,
        that the agent plans to execute next.
        """
        raise NotImplementedError()

    @abstractmethod
    def learn(self, reward, state, is_terminal):
        """
        Update the internal policy using the given state and reward.
        This method is called when the board is ready for the agent.

        reward is the amount of reward given from the environment
        by the previous action of the agent.

        state is the game state after the agent took the previous action.

        is_terminal is a boolean value, True if the game is terminated.
        """
        raise NotImplementedError()

class DQNBlokusAgent(BlokusAgent):
    """
    A class representing an agent which aims to learn the game through DQN(Deep Q Network).
    """

    # hyper values for epsilon-greedy method
    INITIAL_EPSILON = 1.0
    FINAL_EPSILON = 0.1
    EXPLORATION_EPISODES = 1000000

    REPLAY_MEMORY_MAX = 300000
    REPLAY_MEMORY_MIN = 20000

    TARGET_UPDATE_INTERVAL = 1000

    def __init__(self, board_size=12):
        super(DQNBlokusAgent, self).__init__()

        self._board_size = board_size

        # initialization of epsilon parameters
        self.epsilon = self.INITIAL_EPSILON
        self.epsilon_delta = self.FINAL_EPSILON - self.epsilon / self.EXPLORATION_EPISODES

        self.replay_memory = deque()

        # construct Q-network
        self.state_input_layer, self.q_values, q_network = self._construct_network()

        # construct target network
        self.state_target_input_layer, self.target_q_values, target_network = self._construct_network()

        # construct process to copy the weights from Q to target network
        target_network_weights = target_network.trainable_weights
        self.update_target_network = []
        for i in range(len(target_network_weights)):
            target_weight = target_network_weights[i]
            self.update_target_network.append(target_weight.assign(q_network.trainable_weights[i]))

        self.action, self.supervisory_sig, self.loss, self.grad_update = self._build_training_op(q_network.trainable_weights)

        self.session = tf.InteractiveSession()

        # initialize the entire network
        self.session.run(tf.initialize_all_variables())
        self.session.run(self.update_target_network)

    def _construct_network(self):
        # TODO implementation
        return None, None, None

    def _build_training_op(self, q_network_weights):
        return None, None, None, None

    def _update_epsilon(self):
        if self.epsilon > self.FINAL_EPSILON:
            self.epsilon -= self.epsilon_delta

    def _save_replay(self, action):
        self.replay_memory.append(action)
        if len(self.replay_memory) > self.REPLAY_MEMORY_MAX:
            self.replay_memory.popleft()

    def _preprocess_action(self, action):
        board_state = [[0] * self._board_size for _ in range(self._board_size)]
        for cell in action:
            board_state[cell[0]][cell[1]] = 1
        return list(chain.from_iterable(board_state))

    def _preprocess_board_state(self, session):
        """
        returns a tuple, containing
        "flattened" board states of player and then enemy.
        """
        board = session.get_board()

        red_board = [[0] * self._board_size for _ in range(board.get_size())]
        blue_board = [[0] * self._board_size for _ in range(board.get_size())]
        for column in range(board.get_size()):
            for row in range(board.get_size()):
                cell_data = board.get_data_at((column, row))

                if cell_data.is_red():
                    red_board[column][row] = 1
                elif cell_data.is_blue():
                    blue_board[column][row] = 1

        red_flattened = list(chain.from_iterable(red_board))
        blue_flattened = list(chain.from_iterable(blue_board))

        if session.is_red_next:
            return (red_flattened, blue_flattened)
        else:
            return (blue_flattened, red_flattened)

    def _evaluate_action_q(self, player_board, enemy_board, action):
        # TODO implementation
        return 0

    def get_action(self, game_state, action_space):
        self._update_epsilon()

        action_list = list(action_space)

        if self.epsilon >= random.random():
            action = random.choice(action_list)
        else:
            player_board, enemy_board = self._preprocess_board_state(game_state)
            action_q_values = []
            for action in action_list:
                action_q_values.append(self._evaluate_action_q(player_board, enemy_board, action))
            action = action_list[np.argmax(action_q_values)]

        self._save_replay(action)
        return action

    def learn(self, reward, state, is_terminal):
        # TODO implementation
        return

class RandomBlokusAgent(BlokusAgent):
    """
    A class representing an agent that chooses the action randomly.
    """
    def __init__(self):
        super(RandomBlokusAgent, self).__init__()

    def get_action(self, game_state, action_space):
        return random.sample(action_space, 1)[0]

    def learn(self, reward, state, is_terminal):
        pass
