"""
A module which provides a learning environment for blokus agents.
"""
from game.blokus import BlokusGame

class BlokusEnvironment:
    """
    A class which provides a learning environment for blokus agents.
    """
    def __init__(self, red_agent, blue_agent):
        self.session = BlokusGame()
        self.red_agent = red_agent
        self.blue_agent = blue_agent

        self.prev_red_action = None
        self.prev_blue_action = None

    def execute_turn(self):
        """
        Executes a cycle of play-learn for red/blue agents

        Returns a boolean value indicating if the game has terminated.
        """
        is_terminated = False

        if self.session.is_red_next:
            agent_action = self.red_agent.get_action(self.session)
            is_terminated = self.session.place(agent_action)
            self.prev_red_action = agent_action
            self.blue_agent.learn(self.prev_blue_action, len(agent_action), is_terminated)

        if not self.session.is_red_next:
            agent_action = self.blue_agent.get_action(self.session)
            self.session.place(agent_action)
            self.prev_blue_action = agent_action
            self.red_agent.learn(self.prev_blue_action, len(agent_action), is_terminated)

        return is_terminated

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
                    print("R", end="")
                elif cell_data.is_blue():
                    print("B", end="")
                else:
                    print("-")
            print()
