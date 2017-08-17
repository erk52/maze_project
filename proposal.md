# Machine Learning Engineer Nanodegree
## Capstone Proposal
Edward Kish
August 18th, 2017

## Proposal
### Domain Background
_(approx. 1-2 paragraphs)_

In this section, provide brief details on the background information of the domain from which the project is proposed. Historical information relevant to the project should be included. It should be clear how or why a problem in the domain can or should be solved. Related academic research should be appropriately cited in this section, including why that research is relevant. Additionally, a discussion of your personal motivation for investigating a particular problem in the domain is encouraged but not required.

### Problem Statement
_(approx. 1 paragraph)_

In this section, clearly describe the problem that is to be solved. The problem described should be well defined and should have at least one relevant potential solution. Additionally, describe the problem thoroughly such that it is clear that the problem is quantifiable (the problem can be expressed in mathematical or logical terms) , measurable (the problem can be measured by some metric and clearly observed), and replicable (the problem can be reproduced and occurs more than once).

The problem here is to implement an algorithm that will allow the simulated micromouse robot to solve the maze as quickly as possible.  The robot gets two runs: one in which to explore the maze and determine an optimal route, and a second run in which to move from the starting location to the goal in the shortest number of steps.  The score will be the number of steps required to reach the goal in the second run plus 1/30th of the number of steps used to explore the maze in the first run.  

### Datasets and Inputs
_(approx. 2-3 paragraphs)_

In this section, the dataset(s) and/or input(s) being considered for the project should be thoroughly described, such as how they relate to the problem and why they should be used. Information such as how the dataset or input is (was) obtained, and the characteristics of the dataset or input, should be included with relevant references and citations as necessary It should be clear how the dataset(s) or input(s) will be used in the project and whether their use is appropriate given the context of the problem.

The input data for this project takes the form of a maze.  In micromouse competitions, mazes are 16x16 squares in size.  The test mazes provided here are 12x12 and 16x16 in size, but mazes of any arbitrary size are possible.  It will be desirable to generate more testing mazes with specific features to test the performance of the simulated robot.  

At each step, the micromouse receives sensory input.  It can sense the distance to the nearest wall in three directions.  From this, it is possible to determine which other squares can be accessed from the current square.  After receiving the sensory input, the robot can execute a movement command consisting of a rotation and a movement distance.  The micromouse can turn 90 degrees left or right, and move up to three spaces forward or backward.  In this way, the mouse can move from one square to another.  The robot has no way to measure its absolute position in the maze.  Instead, we must rely on 'dead-reckoning' and keep track of the position based on previous movement commands.  If a command is invalid, or the robot bumps into a wall, this could result in the robot losing track of its position.  

### Solution Statement
_(approx. 1 paragraph)_

In this section, clearly describe a solution to the problem. The solution should be applicable to the project domain and appropriate for the dataset(s) or input(s) given. Additionally, describe the solution thoroughly such that it is clear that the solution is quantifiable (the solution can be expressed in mathematical or logical terms) , measurable (the solution can be measured by some metric and clearly observed), and replicable (the solution can be reproduced and occurs more than once).

The first run must be used to explore the maze and use the sensory inputs to build a map.  At each step, the sensory inputs can be used to see which other squares can be accessed from the current square.  Once the maze has been mapped, finding the optimal path from the start to the goal is simple.  Since the movement cost to move between one square and another is uniform (one time step), we can find the shortest path with a simple breadth first search.  The mazes are on the order of 15x15, so the running time of BFS should not be a concern.   

### Benchmark Model
_(approximately 1-2 paragraphs)_

In this section, provide the details for a benchmark model or result that relates to the domain, problem statement, and intended solution. Ideally, the benchmark model or result contextualizes existing methods or known information in the domain and problem given, which could then be objectively compared to the solution. Describe how the benchmark model or result is measurable (can be measured by some metric and clearly observed) with thorough detail.

A simple benchmark robot would simply choose a random, valid direction to move.  The number of steps it takes for a completely random walk to reach the goal should serve as a bare minimum standard of performance.  If a robot cannot beat a random walk through the maze, then the algorithm is very poor indeed.  The goal will be to minimize the score calculated from the length of the two runs through the maze.  Although the length of the second run is most heavily weighted by the scoring metric, it is the first run that needs to be most heavily optimized.  Once the maze is mapped out, there is one optimal path length and that will be simple to find.  The real challenge is to find a way to most efficiently explore the maze.

### Evaluation Metrics
_(approx. 1-2 paragraphs)_

In this section, propose at least one evaluation metric that can be used to quantify the performance of both the benchmark model and the solution model. The evaluation metric(s) you propose should be appropriate given the context of the data, the problem statement, and the intended solution. Describe how the evaluation metric(s) are derived and provide an example of their mathematical representations (if applicable). Complex evaluation metrics should be clearly defined and quantifiable (can be expressed in mathematical or logical terms).

The scoring metric for this project is defined as follows: _On each maze, the robot must complete two runs. In the first run, the robot is allowed to freely roam the maze to build a map of the maze. It must enter the goal room at some point during its exploration, but is free to continue exploring the maze after finding the goal. After entering the goal room, the robot may choose to end its exploration at any time. The robot is then moved back to the starting position and orientation for its second run. Its objective now is to go from the start position to the goal room in the fastest time possible. The robot’s score for the maze is equal to the number of time steps required to execute the second run, plus one thirtieth the number of time steps required to execute the first run. A maximum of one thousand time steps are allotted to complete both runs for a single maze._

This is a simple and objective measurement of the robot's performance.  If the robot's behavior is at all random or stochastic, then it will be desirable to find an average score over many runs of the same maze to get a more accurate assessment.  There are three test mazes provided, and these will be used to score the simulated micromouse robot.  But it will also be possible, and desirable, to generate additional test mazes.

### Project Design
_(approx. 1 page)_

In this final section, summarize a theoretical workflow for approaching a solution given the problem. Provide thorough discussion for what strategies you may consider employing, what analysis of the data might be required before being used, or which algorithms will be considered for your implementation. The workflow and discussion that you provide should align with the qualities of the previous sections. Additionally, you are encouraged to include small visualizations, pseudocode, or diagrams to aid in describing the project design, but it is not required. The discussion should clearly outline your intended workflow of the capstone project.

This project can be broken down into to several parts.  The goal is to simulate  a micromouse robot that can efficiently solve a maze.  This simulation will have to do several things.
-Take sensor input
-Convert sensor input into a map of the maze
-Decide how to explore the maze
-Build a complete map based on sensor data as it explores
-Convert a planned movement into a rotation and distance command
-Deicde when to reset and begin the second run
-Plan and follow the shortest possible path to the goal

The final product will be a python class that implements all this functionality.  In addition, it will be useful to visualize both the maze, and the path of the robot as it explores and then solves the maze.  

So far, the basic structure of the robot has been described.  The real challenge of the project will be determining the algorithm that most efficiently explores and solves the maze.  

-----------

**Before submitting your proposal, ask yourself. . .**

- Does the proposal you have written follow a well-organized structure similar to that of the project template?
- Is each section (particularly **Solution Statement** and **Project Design**) written in a clear, concise and specific fashion? Are there any ambiguous terms or phrases that need clarification?
- Would the intended audience of your project be able to understand your proposal?
- Have you properly proofread your proposal to assure there are minimal grammatical and spelling mistakes?
- Are all the resources used for this project correctly cited and referenced?
