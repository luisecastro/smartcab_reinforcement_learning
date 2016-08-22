# -*- coding: utf-8 -*-
import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator


class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.qtable = list()               # List that will contain all the visited states
        self.action_reward = list()        # List that will contain total reward, # of times (state,action), mean reward 
        self.epsilon = 1.                  # Exploration-Explotiation trade-off parameter, subject to change with time
        self.total_reward = 0              # Cumulative reward of all runs 
        self.time = 0.                     # Timestep of all runs


    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        print self.total_reward                                                                                       # Print total reward until last run
                                    

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()                                                             # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = {'light':inputs['light'],'left':inputs['left'],'oncoming':inputs['oncoming'],'right':inputs['right'],'next':self.next_waypoint}
        
        # TODO: Select action according to your policy

        if self.state not in self.qtable:                                                                             # If current state is not yet in the qtable then
            index = -1                                                                                                # Indicates that it will operate in the last index of the lists
            self.qtable.append(self.state)                                                                            # Adding the missing state to the qtable
            action = random.choice(Environment.valid_actions)                                                         # Since the agent hasn't been yet in this state, take random action and explore   
            self.action_reward.append({'None':[13.,0],'forward':[13.,0],'left':[13.,0],'right':[13.,0]})              # Add to the action_reward list, the agent is optimist to the unknown 
                                                                                                                      # [13.] Optimist reward so it will be chosen later, [0] times the agent has been in this state-action, [0.] weighted reward 
        else:                                                                                                         # State is in qtable
            index = self.qtable.index(self.state)                                                                     # Find index of state in qtable
            key_holder = list()                                                                                       
            if self.epsilon > random.random():                                                                        # Check if either exploit or explore
                for key in self.action_reward[index]:                                                                 # If explore, check for unvisted action in current state
                    if self.action_reward[index][key][1] == 0.:                                                       # Unvisited action are added to a holder list and will be randomly chosen
                        key_holder.append(key)                                                                        
                if len(key_holder) == 0:                                                                              # If all state/actions have been visited at least once, randomly choose 
                    key_holder = Environment.valid_actions                                                            

            else:
                min = -99.                                                                                            # A helping variable to be the floor to compare
                for key in self.action_reward[index]:                                                                 # Search all action within the current state
                    if self.action_reward[index][key][0] > min:                                                       # If current state-action is bigger than current min, assign weighted reward to min 
                        key_holder = [key]                                                                            # and replace current key (action)
                        min = self.action_reward[index][key][0]
                    elif self.action_reward[index][key][0] == min:                                                    # If current min is equal to current state-action, add key (action) to key holder
                        key_holder.append(key)

            action = random.choice(key_holder)                                                                        # Randomly choose, if there was only one unvisited action, or only one current state-action
        
                                                                                                                      # maximum, it with randomly choose them with probability = 1
        # Execute action and get reward
        if action == 'None':                                                                                          # Since None was taken from the dictionaries, change if needed for the reward function
            action = None

        reward = self.env.act(self, action)
        self.total_reward += reward                                                                                   # Get current reward for state-action and add to the score keeper total reward

        if reward > 8:                                                                                                # In this case, the agent shouldn't be rewarded for arriving with a valid but not optimal
            reward -= 10                                                                                              # action to the goal, and receiving a goal reward with such action can make it 
                                                                                                                      # prefer them
        # TODO: Learn policy based on state, action, reward     
        self.action_reward[index][str(action)][1] += 1
        alpha = self.action_reward[index][str(action)][1]**-1                                                          # Alpha determines how the agent upgrades the rewards it receives for states-actions
        self.action_reward[index][str(action)][0] = (1-alpha)*self.action_reward[index][str(action)][0]+alpha*reward  # Currently Alpha = 1/# of times visited this state-action pair

        self.time += .01
        self.epsilon *= 1./(1+self.time)                                                                              # Play with epsilon for best exploitation-exploration balance
        print "state-action-reward: {},{},{},{},{},{},{},{}".format(self.state['light'],self.state['left'],self.state['oncoming'],self.state['right'],self.state['next'],action,self.action_reward[index][str(action)][0],self.action_reward[index][str(action)][1])



def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.001, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
