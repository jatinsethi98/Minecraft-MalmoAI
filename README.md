## Welcome to GitHub Pages

You can use the [editor on GitHub](https://github.com/DaanyaAnandUCI/CS175/edit/master/README.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/DaanyaAnandUCI/CS175/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.

Daanya Anand, Jatin Sethi, Ryan Feigenbaum
CS 175, Project Proposal
Summary of the Project In a paragraph mention the main idea behind your project. Focus on the problem setup, not the solution, i.e. what is your goal? At the very least, you should have a sentence that clearly explains the input/output semantics of your project, i.e. what information will it take as input, and what will it produce. Mention any applications, if any, for your project.
For our project this quarter, we will be choosing option 1, Malmo Minecraft. Our problem for the AI to solve will be to locate, find a path to, and obtain the diamond on the map. It must then make its way back to the starting location. In its way will be obstacles such as fences, enemy mobs, and doors. This project can be changed and adapted to different goal states, in that we could set the goal to be a variety of different things, such as going through a nether portal, or finding gold instead of diamonds.
Evaluation Plan Mention how you will evaluate the success of your project. In a paragraph, focus on the quantitative evaluation: what are the metrics, what are the baselines, by how much you expect your approach to improve the metric, what data will you evaluate on, etc. In another paragraph, describe what qualitative analysis you will show to verify the project works, such as what are the sanity cases for the approach, how will you visualize the internals of the algorithm to verify it works, what’s your moonshot case, i.e. it’ll be awesome and impressive if you get there. Note that these are not promises, we’re not going to hold you to what you say here, but we want to see if you are able to think about evaluation of your project in a critical manner.
Our success is based on our AI reaching the diamond with lives to spare. Our AI will dynamically choose between an offensive approach and a defensive approach depending on the time/lives it has left. We plan to add several monsters and obstructions in our world for our AI to make complex decisions. 

The algorithm will be measured in the following way: the AI will start off with 100% health and in its first life. Each movement and/or attack will have a percentage of “energy loss” associated with it, and the AI’s goal will be to maximize its energy level by the end of its course to the diamond. As mentioned below, our stretch goal is to implement multiple lives, so once we get to that stage, an added metric will be the amount of lives lost as well. Another metric we can consider using is time, to measure how long the AI takes to complete its mission and return to its starting point. 

Our moonshot case is that the AI will reach the diamond in the most efficient way, i.e. It will adapt to the current environment and if need be, avoid some monsters to reach the diamond in the least time. Efficiency will be measured by the amount of health left at the end of its journey.

Goals Next pick 3 goals. The first goal is the minimum goal. This is the minimum your project should achieve to pass the course. The second goal is the realistic goal, this is a goal you will likely achieve during the course and should provide some interesting results. The third goal is the ambitious one, this would provide you awesome results but would be difficult to achieve. For reference think of how goals are described in crowdfunding projects like Kickstarter.
Break down the minimum goal into 2 milestones, the first one of which should be achieved by February 7. For the realistic goal also define 2 milestones. For the ambitious goal define 1 milestone. The milestones have to be verifiable based on what you define in your evaluation plan section. List the 5 milestones (in total) as 5 bullets breaking down the 3 goals.

Goal 1) Our minimum goal is to get our AI to be able to find a randomly-placed diamond without any obstruction in its path. The diamond can be placed anywhere on the map, and our AI will have to find the most efficient path to the diamond.
Milestone 1) Create Minecraft kingdom where diamond is randomly placed on the map. The AI must be able to perceive the diamond and get to it.
Milestone 2) The AI must now be able to identify the most efficient path to the diamond and take that route to the diamond. The AI must also be able to get back to its initial location.

Goal 2) Our realistic goal is to create an AI that can fight off monsters, get past fences, open doors, and more to reach the diamond and retreat back to its starting point. 
Milestone 3) The AI must be able to identify the difference between a fence and door and appropriately handle the obstruction. 
Milestone 4) The AI must now be able to handle moving monsters and attack them before the monster reaches the AI.

Goal 3) Our stretch goal is to create an AI that can detect multiple diamonds and retrieve all of them, without losing all 3 lives. The obstructions the AI will need to pass will have varying effects on the AI, and the algorithm will have to choose the path that causes the least damage to its score.
Milestone 5) Now we must implement the AI having multiple lives. The AI needs to identify the path with least obstruction and, on occasion, choose to lose one life if that maximizes its score at the end. This will require the AI to look ahead of its current stage and anticipate how to best maximize its score.

