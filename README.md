In order to use our code, just have a working malmo server, and run our agent with python project.py.




## Malmo Minecraft Project Proposal

The website presents group 21's project proposal using Malmo Minecraft.
Team Members: Daanya Anand, Jatin Sethi, Ryan Feigenbaum

### Summary

```markdown
For our project this quarter, we will be choosing 
option 1, Malmo Minecraft. Our problem for the 
AI to solve will be to locate, find a path to, and 
obtain the diamond on the map. It must then make 
its way back to the starting location. In its way 
will be obstacles such as fences, enemy mobs, and 
doors. This project can be changed and adapted to 
different goal states, in that we could set the goal 
to be a variety of different things, such as going 
through a nether portal, or finding gold instead 
of diamonds.
```

### Evaluation Plan

```markdown
The algorithm will be measured in the following way: 
the AI will start off with 100% health and in its first 
life. Each movement and/or attack will have a percentage 
of “energy loss” associated with it, and the AI’s goal 
will be to maximize its energy level by the end of 
its course to the diamond. As mentioned below, our 
stretch goal is to implement multiple lives, so once 
we get to that stage, an added metric will be the amount 
of lives lost as well. Another metric we can consider 
using is time, to measure how long the AI takes to 
complete its mission and return to its starting point.

Our moonshot case is that the AI will reach the diamond
in the most efficient way, i.e. It will adapt to the 
current environment and if need be, avoid some monsters
to reach the diamond in the least time. Efficiency 
will be measured by the amount of health left at the 
end of its journey.
```

### Goals and Milestones

```markdown
#### Goal 1) 
Our minimum goal is to get our AI to be able 
to find a randomly-placed diamond without any 
obstruction in its path. The diamond can be placed 
anywhere on the map, and our AI will have to find the 
most efficient path to the diamond.
#### Milestone 1) 
Create Minecraft kingdom where diamond is randomly 
placed on the map. The AI must be able to perceive 
the diamond and get to it.
#### Milestone 2) 
The AI must now be able to identify the most efficient 
path to the diamond and take that route to the diamond. 
The AI must also be able to get back to its initial 
location.

#### Goal 2) 
Our realistic goal is to create an AI that can fight 
off monsters, get past fences, open doors, and more 
to reach the diamond and retreat back to its starting 
point. 
#### Milestone 3) 
The AI must be able to identify the difference
between a fence and door and appropriately handle the 
obstruction. 
#### Milestone 4) 
The AI must now be able to handle moving monsters and
attack them before the monster reaches the AI.

#### Goal 3) 
Our stretch goal is to create an AI that can 
detect multiple diamonds and retrieve all of them, without 
losing all lives. The obstructions the AI will need to 
pass will have varying effects on the AI, and the algorithm
will have to choose the path that causes the least damage 
to its score.
#### Milestone 5) 
Now we must implement the AI having multiple lives. The 
AI needs to identify the path with least obstruction 
and, on occasion, choose to lose one life if that maximizes
its score at the end. This will require the AI to look 
ahead of its current stage and anticipate how to best 
maximize its score.

```
