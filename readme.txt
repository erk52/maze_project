This project was coded in Python 3.

The only external library it makes use of is matplotlib for generating visualizations of mazes.

The Robot.py file contains the parent class Robot, which implements much of the generic robot functionality, such as taking sensor data and using that to build and save a map, finding the shortest path to a point using breadth first search, and performing test runs of a given maze.

Models.py contains several child classes of Robot, which implement the various exploration algorithms discussed in this report.

Maze.py is unchanged from the provided version, and contains the implementation of the Maze class.

maze_generator.py contains a few utility functions for generating, displaying, and saving custom mazes.

The following text files contain maze data:
test_maze_01.txt
test_maze_02.txt
test_maze_03.txt
open_maze_12.txt
custom_maze_02.txt
custom_maze_03.txt

The approved proposal and the final report are included as pdf files.

Micromouse Simulation Summary.ipynb is an IPython notebook containing much of the same information as the final report.  This was helpful during the writing process and to generate visualizations.