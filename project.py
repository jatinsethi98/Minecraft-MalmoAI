from __future__ import print_function
from builtins import range
import MalmoPython
import os
import sys
import time
import uuid
import json
import malmoutils
import math
import random
import functools
import builtins
#import gym

builtins.print = functools.partial(print, flush=True)

#env = gym.make("")


class TabQAgent(object):
    """Tabular Q-learning agent for discrete state/action spaces."""

    def __init__(self, actions=[], epsilon=0.2, alpha=0.1, gamma=1.0, debug=True):
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.training = True

        self.actions = actions
        self.q_table = {}

        self.rep = 0

    def loadModel(self, model_file):
        """load q table from model_file"""
        with open(model_file) as f:
            self.q_table = json.load(f)

    def training(self):
        """switch to training mode"""
        self.training = True

    def evaluate(self):
        """switch to evaluation mode (no training)"""
        self.training = False

    def act(self, world_state, agent_host, current_r):
        """take 1 action in response to the current world state"""

        def world_observations():
            obs_text = world_state.observations[-1].text
            obs = json.loads(obs_text)  # most recent observation
            return obs

        obs = world_observations()
        surrondings = obs['floor3x3']
        around_me = [surrondings[1], surrondings[7], surrondings[3], surrondings[5]]  # FRONT LEFT RIGHT BACK -> BACK FRONT LEFT RIGHT

        if not u'XPos' in obs or not u'ZPos' in obs:  # Incomplete observation received
            return 0

        def add_currentLoaction_to_qtable():  # q table dictionary with current position as key and list of actions as value, all set to 0
            current_s = "%d:%d" % (int(obs[u'XPos']), int(obs[u'ZPos']))  # string of current position

            if current_s not in self.q_table:  # if the current postion is not in q table
                self.q_table[current_s] = ([0] * len(
                    self.actions))  # Add that to q table dictionary with current position as value and set of actions as key, all set to 0
            for i in range(len(around_me)):
                if around_me[i] == 'lava' or around_me[i] == 'stone':
                    self.q_table[current_s][i] = -100
            return current_s

        current_s = add_currentLoaction_to_qtable()

        def updateQtable():  # Update q table, Formula to update qtable in the function
            # update Q values                                                          
            if self.training and self.prev_s is not None and self.prev_a is not None:  # we update q_table for previous action here
                old_q = self.q_table[self.prev_s][self.prev_a]  # prev_a is previous action and prev_s is previous location
                self.q_table[self.prev_s][self.prev_a] = old_q + self.alpha * (current_r + self.gamma * max(self.q_table[current_s]) - old_q)

        updateQtable()

        def select_random_action():
            # select the next action
            rnd = random.random()
            if rnd < self.epsilon:

                m = self.q_table[current_s].copy()
                ll = list()
                for i in range(len(around_me)):
                    if around_me[i] == 'lava' or around_me[i] == 'stone':
                        ll.append(i)

                for i in sorted(ll, reverse=True):
                    del m[i]

                m = max(m)
                l = list()
                for x in range(0, len(self.actions)):
                    if self.q_table[current_s][x] == m:
                        l.append(x)
                y = random.randint(0, len(l) - 1)
                a = l[y]


                #a = random.randint(0, len(self.actions) - 1)
            else:  # Random selection between the max value of actions for current position
                m = self.q_table[current_s].copy()
                ll = list()
                for i in range(len(around_me)):
                    if around_me[i] == 'lava' or around_me[i] == 'stone':
                        ll.append(i)

                # movenorth 1", "movesouth 1", "movewest 1", "moveeast 1
                if self.prev_a == 0 and 1 not in ll and len(ll) != len(m) -1:
                    ll.append(1)
                elif self.prev_a == 1 and 0 not in ll and len(ll) != len(m) -1:
                    ll.append(0)
                elif self.prev_a == 2 and 3 not in ll and len(ll) != len(m) -1:
                    ll.append(3)
                elif self.prev_a == 3 and 2 not in ll and len(ll) != len(m) -1:
                    ll.append(2)

                for i in sorted(ll, reverse=True):
                    del m[i]

                m = max(m)
                l = list()
                for x in range(0, len(self.actions)):
                    if self.q_table[current_s][x] == m:
                        l.append(x)
                y = random.randint(0, len(l) - 1)
                a = l[y]
            return a

        a = select_random_action()

        # send the selected action
        agent_host.sendCommand(self.actions[a])
        self.prev_s = current_s
        self.prev_a = a

        return current_r

    def run(self, agent_host):
        """run the agent on the world"""

        total_reward = 0
        current_r = 0
        tol = 0.01

        self.prev_s = None
        self.prev_a = None

        # wait for a valid observation
        world_state = agent_host.peekWorldState()
        while world_state.is_mission_running and all(e.text == '{}' for e in world_state.observations):
            world_state = agent_host.peekWorldState()
        # wait for a frame to arrive after that
        num_frames_seen = world_state.number_of_video_frames_since_last_state
        while world_state.is_mission_running and world_state.number_of_video_frames_since_last_state == num_frames_seen:
            world_state = agent_host.peekWorldState()
        world_state = agent_host.getWorldState()
        for err in world_state.errors:
            print(err)

        if not world_state.is_mission_running:
            return 0  # mission already ended

        assert len(world_state.video_frames) > 0, 'No video frames!?'

        obs = json.loads(world_state.observations[-1].text)
        prev_x = obs[u'XPos']
        prev_z = obs[u'ZPos']
        print('Initial position:', prev_x, ',', prev_z)

        # take first action
        total_reward += self.act(world_state, agent_host, current_r)

        require_move = True
        check_expected_position = False

        # main loop:
        while world_state.is_mission_running:

            # wait for the position to have changed and a reward received
            print('Waiting for data...', end=' ')
            while True:
                world_state = agent_host.peekWorldState()
                if not world_state.is_mission_running:
                    print('mission ended.')
                    break
                if len(world_state.rewards) > 0 and not all(e.text == '{}' for e in world_state.observations):
                    obs = json.loads(world_state.observations[-1].text)
                    curr_x = obs[u'XPos']
                    curr_z = obs[u'ZPos']
                    if require_move:
                        if math.hypot(curr_x - prev_x, curr_z - prev_z) > tol:
                            print('received.')
                            break
                    else:
                        print('received.')
                        break
            # wait for a frame to arrive after that
            num_frames_seen = world_state.number_of_video_frames_since_last_state
            while world_state.is_mission_running and world_state.number_of_video_frames_since_last_state == num_frames_seen:
                world_state = agent_host.peekWorldState()

            num_frames_before_get = len(world_state.video_frames)

            world_state = agent_host.getWorldState()
            for err in world_state.errors:
                print(err)
            current_r = sum(r.getValue() for r in world_state.rewards)

            if world_state.is_mission_running:
                assert len(world_state.video_frames) > 0, 'No video frames!?'
                num_frames_after_get = len(world_state.video_frames)
                assert num_frames_after_get >= num_frames_before_get, 'Fewer frames after getWorldState!?'
                frame = world_state.video_frames[-1]
                obs = json.loads(world_state.observations[-1].text)
                curr_x = obs[u'XPos']
                curr_z = obs[u'ZPos']
                print('New position from observation:', curr_x, ',', curr_z, 'after action:', self.actions[self.prev_a],
                      end=' ')  # NSWE    
                print()
                prev_x = curr_x
                prev_z = curr_z
                # act
                total_reward += self.act(world_state, agent_host, current_r)

        # process final reward
        total_reward += current_r

        # update Q values
        if self.training and self.prev_s is not None and self.prev_a is not None:
            old_q = self.q_table[self.prev_s][self.prev_a]
            self.q_table[self.prev_s][self.prev_a] = old_q + self.alpha * (current_r - old_q)

        return total_reward


# Create default Malmo objects:

agent_host = MalmoPython.AgentHost()

agent_host.addOptionalFlag('load_model', 'Load initial model from model_file.')
agent_host.addOptionalStringArgument('model_file', 'Path to the initial model file', '')
agent_host.addOptionalFlag('debug', 'Turn on debugging.')
agent_host.addOptionalStringArgument("recording_dir,r", "Path to location for saving mission recordings", "")
agent_host.addOptionalFlag("record_video,v", "Record video stream")

try:
    agent_host.parse(sys.argv)
except RuntimeError as e:
    print('ERROR:', e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)

# -- set up the python-side drawing -- #

if agent_host.receivedArgument("test"):
    num_maps = 1
else:
    num_maps = 1


rewards_per_ep = []

for imap in range(num_maps):

    # -- set up the agent -- #
    actionSet = ["movenorth 1", "movesouth 1", "movewest 1", "moveeast 1"]

    agent = TabQAgent(
        actions=actionSet,
        epsilon=0.03,#Exploration rate of the Q-learning agent
        alpha=0.2,#Learning rate of the Q-learning agent
        gamma=1.0, #Discount factor
        debug=agent_host.receivedArgument("debug"))

    with open('maze.xml', 'r') as f:
        print("Loading mission from maze.xml")
        mission_xml = f.read()
        my_mission = MalmoPython.MissionSpec(mission_xml, True)
    # my_mission = MalmoPython.MissionSpec(missionXML, True)

    my_mission.removeAllCommandHandlers()
    my_mission.allowAllDiscreteMovementCommands()
    my_mission.requestVideo(700, 700)
    my_mission.setViewpoint(1)

    my_clients = MalmoPython.ClientPool()
    my_clients.add(MalmoPython.ClientInfo('127.0.0.1', 10000))  # add Minecraft machines here as available

    # Attempt to start a mission:
    max_retries = 3
    agentID = 0
    expID = 'tabular_q_learning'

    num_repeats = 50
    cumulative_rewards = []

    for i in range(num_repeats):

        print("\nMap %d - Mission %d of %d:" % (imap, i + 1, num_repeats))
        my_mission_record = malmoutils.get_default_recording_object(agent_host,
                                                                    "./save_%s-map%d-rep%d" % (expID, imap, i))

        for retry in range(max_retries):
            try:
                agent_host.startMission(my_mission, my_clients, my_mission_record, agentID, "%s-%d" % (expID, i))
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print("Error starting mission:", e)
                    exit(1)
                else:
                    time.sleep(2)

        # Loop until mission starts:
        print("Waiting for the mission to start", end=' ')
        world_state = agent_host.getWorldState()
        while not world_state.has_mission_begun:
            print(".", end="")
            time.sleep(0.1)
            world_state = agent_host.getWorldState()
            for error in world_state.errors:
                print("Error:", error.text)

        print()

        print("Mission running ", end=' ')
        # -- run the agent in the world -- #
        cumulative_reward = agent.run(agent_host)
        print('Cumulative reward: %d' % cumulative_reward)
        cumulative_rewards += [cumulative_reward]

        # -- clean up -- #
        time.sleep(0.5)  # (let the Mod reset)

    print("Done.")

    print()
    print("Cumulative rewards for all %d runs:" % num_repeats)
    print(cumulative_rewards)

    rewards_per_ep.append(cumulative_rewards)

"""
#agent_host.sendCommand("pitch 0.2")
# Loop until mission ends:
len = 4
while world_state.is_mission_running:
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)
    if world_state.number_of_observations_since_last_state > 0:
        msg = world_state.observations[-1].text
        observations = json.loads(msg)
        grid = observations.get(u'floor3x3', 0)
        print(grid)        
   # agent_host.sendCommand("move 1")     
   # agent_host.sendCommand("strafe -1") 
   # agent_host.sendCommand("strafe -1") 
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)
"""
print()
print(rewards_per_ep)
print("Mission ended")
# Mission has ended.
