"""
A module which provides a learning environment for blokus agents.
"""
from game.blokus import BlokusGame
from termcolor import colored

class BlokusEnvironment:
    """
    A class which provides a learning environment for blokus agents.
    """
    def __init__(self):
        self.session = BlokusGame()

        self.prev_actions = {"red": None, "blue": None}

    def execute_turn(self, red_agent, blue_agent):
        """
        Executes a cycle of play-learn for red/blue agents

        Returns a boolean value indicating if the game has terminated.
        """
        is_game_continued = False

        for agent in [red_agent, blue_agent]:
            agent_color = "red" if agent is red_agent else "blue"
            opponent_color = "red" if agent_color is "blue" else "blue"

            action_space = self.session.get_all_possible_placements()

            # skip the turn if there's nothing to be done.
            if len(action_space) is 0:
                self.session.change_turn()
                continue

            # execute learning cycle
            if self.prev_actions[agent_color] is not None:
                reward = 0
                agent.learn(reward, self.session, False)

            is_game_continued = True

            agent_action = agent.get_action(self.session, action_space)

            # execute the agent's action
            self.session.place(agent_action, check=False)
            self.session.change_turn()

            # update the action cache
            self.prev_actions[agent_color] = agent_action

        return is_game_continued

    def render_console(self):
        """
        Renders the game progress to the console.
        """

        print("Game status: ")

        # display next player
        print("Next       : ", end="")
        if self.session.is_red_next:
            print("Red")
        else:
            print("Blue")

        # display cell count information
        count = self.session.get_cell_counts()
        print("Red cells  : " + str(count[0]))
        print("Blue cells : " + str(count[1]))
        print("")

        # print the board
        board = self.session.get_board()
        size = board.get_size()
        for row in range(size):
            for column in range(size):
                cell_data = board.get_data_at((column, row))
                if cell_data.is_red():
                    print(colored("R", "red"), end="")
                elif cell_data.is_blue():
                    print(colored("B", "blue"), end="")
                else:
                    print("-", end="")
            print()
