# Smart cab reinforcement learning
## Udacity Machine Learning Nanodegree Project 4

The project simulates a city environment where an agent "smart cab" needs to navigate from a start point towards towards a goal, to do so, it needs to know the different states it could be, which are identified by signals of the environment (trafic lights, incoming trafic) and needs to have an action that maximizes the rewards for each state.

The files are:
- project.pdf: Here is a complete guide through the project, the results of runing it randomly and using Q learning as well as the statistics for each run. It explains the mathematicals tools used and the posible outcomes of variations in the program.

- smartcab/agent.py: The file that defines the agent. Here the agent interprets inputs, creates a table of the states and chooses among the valid actions. The agent first uses random actions to explore the environment then chooses highest reward actions according to what it learned to reach to maximize reward.

- smartcab/planner.py: It generates the next_point for the agent, that is, the next direction it must follow to reach the goal.

- smartcab/environment.py: Generates the inputs that the agent will asses to understand how to navigate in the environment.

- smartcab/simulator.py: The simulator can have an output using pygame to visualize how the smartcab and the environment behaves.

Along this, a couple of text files are included. These are the logs of the random run and of the trained agent. The statistics provided where extracted from here.
