from dqn_agent import BlokusAgent
from blokus_env import BlokusEnvironment

NUM_EPISODES = 10000


def main():
    """
    Main process of dqn learning
    Returns educated agent.
    """
    red_agent = BlokusAgent()
    blue_agent = BlokusAgent()

    for _ in range(NUM_EPISODES):
        environment = BlokusEnvironment(red_agent, blue_agent)
        while environment.execute_turn():
            environment.render_console()

        red_agent.learn_finalize(environment.session)
    return


if __name__ == "__main__":
    main()
