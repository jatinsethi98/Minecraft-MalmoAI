In order to use our code, just have a working malmo server, and run our agent with python project.py.

I highly encourage you to look at our Wiki for a detailed report.

## Abstract

This project’s final aim is to create an artificial intelligence agent to navigate through a Minecraft world successfully. Success is defined by finding and obtaining either one or multiple diamonds placed in the world while overcoming obstacles such as lava and monsters. The agent will also maximize its reward score by avoiding obstacles when possible to complete its journey.
To accomplish this, we created two separate agents: one for finding diamonds in a maze and one for fighting off monsters. For the first, we have created a 20x28 maze that has multiple diamonds placed throughout the maze. The agent navigates this maze by perceiving the blocks directly adjacent to it, creating a 3x3 block observation that the AI can base decisions off. It avoids dying in the lava and is able to find multiple diamonds, while updating the Q-learning table with reward values. Additionally, we created a second agent that is able to perceive monsters around it using video recognition, identify the monsters, and kill them with a provided sword. The maze for the second agent is also 20x28, and the agent uses computer vision and a neural network to fight off the monsters in the world.


## Problem Statement
The problem we were addressing in the duration of this project centered around two overarching goals: 
1) creating an AI agent to travel through a Minecraft world to retrieve diamonds, navigate obstacles, and fight monsters, and
2) experimenting with machine learning techniques to implement reinforcement learning using tabular Q learning and then moving into deep reinforcement learning.
Halfway through our project, our biggest problem we needed to focus on was creating an AI agent that uses a deep reinforcement learning algorithm instead of one that uses a tabular Q learning method. This was difficult at the time, because we realized that shifting from tabular Q with the environment that we had set up to deep Q learning would require a lot of restructuring, which our time constraints did not allow for. We also still needed to achieve our goal of fighting off monsters, since up to that point our agent could only retrieve diamonds and avoid obstacles. This led us to creating an entirely new AI, which is how we ended up with two agents with two different environments.
As of the halfway-point, since the Q learning method could choose to act randomly because of the exploration rate, it did not have a strict policy function. In order to make the agent smarter and more capable of completing our goal successfully, we needed to transition to an algorithm that used policy-focused reinforcement learning, such as one using neural networks.

In the environments we have built, both of which are 20x28, we have achieved our initial goals. For the first, Q learning works fine, and the environment is a simple maze with lava lining the edges of the maze. However, as we built a more complex world for the agent to survive in and added monsters, the need for a maze evaporated and we just have an empty box, with zombies in the box. The reward signal in the first is movement, and finding diamonds. As the first agent navigates around the world, it perceives 3x3 blocks and associates -100 reward with lava. It also associates -1 with any movement, to encourage the AI to make as few moves as possible. It associates +100 with finding a diamond, and +10 with finding the gold that we laid out in the paths towards finding multiple diamonds. For the second, we were able to reach our goal of using deep reinforcement learning by implementing a neural network along with Q-learning. Our agent starts off with no data. As monsters begin to attack the AI and the agent dies, it associates negative reward with being attacked by a monster. As the algorithm goes on and the agent learns, the agent makes better decisions from its neural network and fights off the monsters, associating positive reward to killing a zombie.

## Method
The solution we have involves two AIs. 
1. The first program is the one we had at the halfway point: tabular Q learning algorithm with a positive reward for finding gold and diamonds and negative reward for falling into the lava. We tuned the exploration rate hyperparameter by testing with different rates 0.0-0.6 and picking the one with the best result, meaning that once the agent found a diamond once, the agent balanced refinding the diamond in successive runs and exploring new areas so it can discover other diamonds.

2. Our second AI uses deep reinforcement learning through a neural network, using Keras and Ten- sorflow. This was really interesting to explore because there were a lot of factors to consider when deciding the layers and nodes in the network. We did some research into Ray, which is a scalable reinforcement learning framework, and OpenAI Gym, which would help our algorithm learn faster, but decided that Keras and TensorFlow were better to work with for our specific project since we were more familiar with them. Our neural network has a total of 5 layers, with 3 convolution layers and 2 fully-connected layers. We reached these numbers after intensive testing with different amounts of layers, capping the number of convolutional layers at 4, and watching how our agent interacts with the environment.

## Detailed Flow of Monster-Fighting Program

For our monster fighting AI, we use computer vision and a neural network.

1. Our algorithm sets up our Sequential model in Keras. Model details are provided in the table below
2. We also setup a replay array for recording
3. After receiving the image frames from Malmo we pre-process them before feeding them into the neural network
4. We reduce the size of the image to 84x84 and convert to grayscale
5. The reward does not just depend on the current state, rather on the sequence of states before the reward. Thus, we need information from previous states as well to make an appropriate action. Therefore, we combine a set of most recent 3 frames and combine them into an array of 84x84x3.
6. Our program works on a depreciating epsilon policy. That is, we start with an epsilon of 1.0 and reduce it to 0.03 over 50,000 runs. This is necessary since our agent needs to explore the state space. Over time, as our Deep RL learns the epsilon is reduced and the moves to be made are processed by the neural network
7. We save 4-tuple of <currentState, action, reward, newState> in our replay array
8. After every 200 frames we randomly batch 32 sets of tuples from the replay array and train our model on them.
9. The AI learns over the course of the program, eventually identifying and killing the zombie. This happens because it starts associating higher q values to images with a monster in the center and lower q values to empty spaces.

