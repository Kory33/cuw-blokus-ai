"""
A module which provides varieties of dqn agents.
"""

from abc import ABCMeta, abstractmethod

import random


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
    def __init__(self):
        super(DQNBlokusAgent, self).__init__()

    def get_action(self, game_state, action_space):
        # TODO implementation
        return

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
