# Machine Learning Engineer Nanodegree
## Capstone Proposal
Joe Udacity  
December 31st, 2050

## Proposal
### Domain Background
_(approx. 1-2 paragraphs)_

In this section, provide brief details on the background information of the domain from which the project is proposed. Historical information relevant to the project should be included. It should be clear how or why a problem in the domain can or should be solved. Related academic research should be appropriately cited in this section, including why that research is relevant. Additionally, a discussion of your personal motivation for investigating a particular problem in the domain is encouraged but not required.

### Problem Statement
_(approx. 1 paragraph)_

_In this section, clearly describe the problem that is to be solved. The problem described should be well defined and should have at least one relevant potential solution. Additionally, describe the problem thoroughly such that it is clear that the problem is quantifiable (the problem can be expressed in mathematical or logical terms) , measurable (the problem can be measured by some metric and clearly observed), and replicable (the problem can be reproduced and occurs more than once)._

The problem here is to implement an algorithm that will allow the simulated micromouse robot to solve the maze as quickly as possible.  The robot gets two runs: one in which to explore the maze and determine an optimal route, and a second run in which to move from the starting location to the goal in the shortest number of steps.  The score will be the number of steps required to reach the goal in the second run plus 1/30th of the number of steps used to explore the maze in the first run.  

### Datasets and Inputs
_(approx. 2-3 paragraphs)_

_In this section, the dataset(s) and/or input(s) being considered for the project should be thoroughly described, such as how they relate to the problem and why they should be used. Information such as how the dataset or input is (was) obtained, and the characteristics of the dataset or input, should be included with relevant references and citations as necessary It should be clear how the dataset(s) or input(s) will be used in the project and whether their use is appropriate given the context of the problem._

At each step, the micromouse receives sensory input.  It can sense the distance to the wall in three directions.  From this, it is possible to determine which other squares can be accessed from the current square.  

After receiving the sensory input, the robot can execute a movement command consisting of a rotation and a movement distance.  The micromouse can turn 90 degrees left or right, and move up to three spaces forward or backward.  In this way, the mouse can move from one square to another.  

The robot has no way to measure its absolute position in the maze.  Instead, we must rely on 'dead-reckoning' and keep track of the position based on previous movement commands.  If a command is invalid, or the robot bumps into a wall, this could result in the robot losing track of its position.  

### Solution Statement
_(approx. 1 paragraph)_

_In this section, clearly describe a solution to the problem. The solution should be applicable to the project domain and appropriate for the dataset(s) or input(s) given. Additionally, describe the solution thoroughly such that it is clear that the solution is quantifiable (the solution can be expressed in mathematical or logical terms) , measurable (the solution can be measured by some metric and clearly observed), and replicable (the solution can be reproduced and occurs more than once)._

The first run must be used to explore the maze and use the sensory inputs to build a map.  At each step, the sensory inputs can be used to see which other squares can be accessed from the current square.

Once the maze has been mapped, finding the optimal path from the start to the goal is simple.  Since the movement cost to move between one square and another is uniform (one time step), we can find the shortest path with a simple breadth first search.  The mazes are on the order of 15x15, so the running time of BFS should not be a concern.

### Benchmark Model
_(approximately 1-2 paragraphs)_

_In this section, provide the details for a benchmark model or result that relates to the domain, problem statement, and intended solution. Ideally, the benchmark model or result contextualizes existing methods or known information in the domain and problem given, which could then be objectively compared to the solution. Describe how the benchmark model or result is measurable (can be measured by some metric and clearly observed) with thorough detail._

A simple benchmark robot would simply choose a random direction to move.  The number of steps it takes for a completely random walk to reach the goal can be simulated.  

### Evaluation Metrics
_(approx. 1-2 paragraphs)_

_In this section, propose at least one evaluation metric that can be used to quantify the performance of both the benchmark model and the solution model. The evaluation metric(s) you propose should be appropriate given the context of the data, the problem statement, and the intended solution. Describe how the evaluation metric(s) are derived and provide an example of their mathematical representations (if applicable). Complex evaluation metrics should be clearly defined and quantifiable (can be expressed in mathematical or logical terms)._

### Project Design
_(approx. 1 page)_

_In this final section, summarize a theoretical workflow for approaching a solution given the problem. Provide thorough discussion for what strategies you may consider employing, what analysis of the data might be required before being used, or which algorithms will be considered for your implementation. The workflow and discussion that you provide should align with the qualities of the previous sections. Additionally, you are encouraged to include small visualizations, pseudocode, or diagrams to aid in describing the project design, but it is not required. The discussion should clearly outline your intended workflow of the capstone project._

This project can be broken down into to main parts.  The exploratory run, and the optimal path.  As stated above, finding the optimal path is simple once the maze is mapped.  

-----------

**Before submitting your proposal, ask yourself. . .**

- Does the proposal you have written follow a well-organized structure similar to that of the project template?
- Is each section (particularly **Solution Statement** and **Project Design**) written in a clear, concise and specific fashion? Are there any ambiguous terms or phrases that need clarification?
- Would the intended audience of your project be able to understand your proposal?
- Have you properly proofread your proposal to assure there are minimal grammatical and spelling mistakes?
- Are all the resources used for this project correctly cited and referenced?
