# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 08:51:13 2017

@author: EKish
"""

from collections import Counter
import random
from Maze import Maze
import matplotlib.pyplot as plt

class Robot(object):
    '''A simulated micromouse robot.
    This is a general parent class containing attrivbutes and methods for all
    bots, regardless of strategy'''
    
    left_turn = {'up': 'left', 'left': 'down', 'down': 'right', 'right': 'up'}
    right_turn = {'up': 'right', 'right': 'down', 'down': 'left', 'left': 'up'}
    dir_move = {'u': [0, 1], 'r': [1, 0], 'd': [0, -1], 'l': [-1, 0],
                    'up': [0, 1], 'right': [1, 0], 'down': [0, -1], 'left': [-1, 0]}
    
    def __init__(self, maze_dim):
        '''
        Arguments: 
        -maze_dim: size of maze, used to calculate location of the goal
        -explore_frac: minimum fraction of maze spaces to explore before 
         beginning second run
        '''
        self.location = (0, 0)
        self.heading = 'up'
        self.maze_dim = maze_dim
        self.maze_map = {}              #a dictionary mapping each 
                                        #space seen to other spaces 
                                        #the robot can move to
        self.visited = Counter()        #keeps track of spaces already seen
        self.visited[self.location] += 1
        
        self.goal_bounds = (self.maze_dim//2 - 1, self.maze_dim//2)

        self.explore = True             #During the first run, we explore
        self.path = []                  #Prior to second run, we determine the
                                        #optimal path

    def make_connection(self, square_1, square_2):
        '''Makes a connection in the graph maze_map between square_1 and square_2'''
        self.maze_map[square_1] = self.maze_map.get(square_1, set()).union([square_2])
        self.maze_map[square_2] = self.maze_map.get(square_2, set()).union([square_1])
    
    def look_around(self, sensors):
        '''Given sensor input data, find out what squares the robot can move to
        by checking wall distances to the left, center and right.
        Then update the maze_map accordingly.'''
        
        deltas = [Robot.dir_move[Robot.left_turn[self.heading]], 
                  Robot.dir_move[self.heading], Robot.dir_move[Robot.right_turn[self.heading]]]
        for delta, wall_dist in zip(deltas, sensors):
            if not wall_dist:
                continue
            for start in range(0, wall_dist):
                for end in range(start+1, min(start+4, wall_dist+1)):
                    sq1 = tuple([self.location[i] + start*delta[i] for i in range(2)])
                    sq2 = tuple([self.location[i] + end*delta[i] for i in range(2)])
                    self.make_connection(sq1, sq2)
        
    def calc_move(self, target):
        '''Determines rotation and distance to get to target space.  Takes a 
        target position as a tuple, returns a rotation angle and distance.'''
        if self.location == target:
            return 0,0
        delta = [target[i] - self.location[i] for i in range(2)]
        if delta[0] == 0:
            if delta[1] > 0:
                dist = delta[1]
                if self.heading == 'up':
                    rot = 0
                elif self.heading == 'left':
                    rot = 90
                elif self.heading == 'right':
                    rot = -90
                else:
                    dist = -dist
                    rot = 0
            else:
                dist = -delta[1]
                if self.heading == 'up':
                    rot = 0
                    dist = -dist
                elif self.heading == 'left':
                    rot = -90
                elif self.heading == 'right':
                    rot = 90
                else:
                    rot = 0
        else:
            if delta[0] > 0:
                dist = delta[0]
                if self.heading == 'right':
                    rot = 0
                elif self.heading == 'up':
                    rot = 90
                elif self.heading == 'down':
                    rot = -90
                else:
                    dist = -dist
                    rot = 0
            else:
                dist = -delta[0]
                if self.heading == 'right':
                    rot = 0
                    dist = -dist
                elif self.heading == 'up':
                    rot = -90
                elif self.heading == 'down':
                    rot = 90
                else:
                    rot = 0
                    
        return rot, dist
        
    def at_goal(self):
        '''Are we at the goal?'''
        l, h = self.goal_bounds
        return tuple(self.location) in [(l,l), (l, h), (h, l), (h,h)]
        
    def found_goal(self):
        '''Have we visited the goal?
        Note: by rules of tester, seeing the goal space is not enough.
        The robot needs to actually visit a square in the goal area before it
        can reset and start the second run.
        '''
        l, h = self.goal_bounds     
        return any(self.visited[loc] > 0 for loc in [(l,l), (l,h), (h,l), (h,h)])
    
    def path_move(self):
        '''Moves to the next square on the path generated by gen_path()'''
        if not self.path:   #Generate path if we haven't already
            self.path = self.gen_path()[1:]
            
        target = self.path.pop(0)
        r,d = self.calc_move(target)
        self.location = target
        if r == 90:
            self.heading = Robot.right_turn[self.heading]
        elif r == -90:
            self.heading = Robot.left_turn[self.heading]
        return r,d
            
    def gen_path(self, target=None):
        '''Breadth first search algorithm to find path to target.
        If no target given, it looks for a square in the goal bounds'''        
        
        start = tuple(self.location)
        end = target
        if not target:  #if no target given, path to goal
            l, h = self.goal_bounds
            end = None
            #Look for a goal space in our map
            for e in [(l,l), (l, h), (h, l), (h,h)]:
                if self.maze_map.get(e, None):
                    end = e
                    break
        if not end:     #If we can't find the end, something bad happened
            raise Exception("Can't path to a target not in maze_map")
        
        pred = {start: None}
        queue = [start]
        cur = start
        while queue:
            cur = queue.pop(0)
            for node in self.maze_map[cur]:
                if node not in pred.keys():
                    queue.append(node)
                    pred[node] = cur
        pathway = [end]
        cur = pred[end]
        while cur:
            pathway.append(cur)
            cur = pred[cur]
        return pathway[::-1]
        
    def run_maze(self, mazefile, verbose=True, showplot=True):
        '''runs the bot through a given maze file.
        Slightly modified version of tester.py given with project.
        verbose=True will print out scores and information during run
        showplot=True will dispaly maze, explored spaces, and final route
            via a matplotlib figure.
        '''
        
        dir_sensors = {'u': ['l', 'u', 'r'], 'r': ['u', 'r', 'd'],
                       'd': ['r', 'd', 'l'], 'l': ['d', 'l', 'u'],
                       'up': ['l', 'u', 'r'], 'right': ['u', 'r', 'd'],
                       'down': ['r', 'd', 'l'], 'left': ['d', 'l', 'u']}
        dir_move = {'u': [0, 1], 'r': [1, 0], 'd': [0, -1], 'l': [-1, 0],
                    'up': [0, 1], 'right': [1, 0], 'down': [0, -1], 'left': [-1, 0]}
        dir_reverse = {'u': 'd', 'r': 'l', 'd': 'u', 'l': 'r',
                       'up': 'd', 'right': 'l', 'down': 'u', 'left': 'r'}
    
        # test and score parameters
        max_time = 1000
        train_score_mult = 1/30.
    
        # Create a maze based on input argument on command line.
        testmaze = Maze( mazefile )
        # Intitialize a robot; robot receives info about maze dimensions.
        testrobot = self
        self.__init__(testmaze.dim)
        Xex, Yex = [],[]
        Xrn, Yrn = [],[]
        # Record robot performance over two runs.
        runtimes = []
        total_time = 0
        for run in range(2):
            if verbose: print("Starting run {}.".format(run))
    
            # Set the robot in the start position. Note that robot position
            # parameters are independent of the robot itself.
            robot_pos = {'location': [0, 0], 'heading': 'up'}
            run_active = True
            hit_goal = False
            while run_active:
                # check for end of time
                total_time += 1
                if total_time > max_time:
                    run_active = False
                    if not runtimes:
                        runtimes.append(total_time)
                    if verbose: print("Allotted time exceeded.")
                    break
                if run == 0:
                    Xex.append(robot_pos['location'][0])
                    Yex.append(robot_pos['location'][1])
                else:
                    Xrn.append(robot_pos['location'][0])
                    Yrn.append(robot_pos['location'][1])
                # provide robot with sensor information, get actions
                sensing = [testmaze.dist_to_wall(robot_pos['location'], heading)
                           for heading in dir_sensors[robot_pos['heading']]]
                rotation, movement = testrobot.next_move(sensing)
    
                # check for a reset
                if (rotation, movement) == ('Reset', 'Reset'):
                    if verbose: print("reset recieved.  Robot actually at ", robot_pos['location'])
                    if run == 0 and hit_goal:
                        run_active = False
                        runtimes.append(total_time)
                        if verbose: print("Ending first run. Starting next run.")
                        break
                    elif run == 0 and not hit_goal:
                        if verbose: print("Cannot reset - robot has not hit goal yet.")
                        continue
                    else:
                        if verbose: print("Cannot reset on runs after the first.")
                        continue
    
                # perform rotation
                if rotation == -90:
                    robot_pos['heading'] = dir_sensors[robot_pos['heading']][0]
                elif rotation == 90:
                    robot_pos['heading'] = dir_sensors[robot_pos['heading']][2]
                elif rotation == 0:
                    pass
                else:
                    if verbose: print("Invalid rotation value, no rotation performed.")
    
                # perform movement
                if abs(movement) > 3:
                    if verbose: print("Movement limited to three squares in a turn.")
                movement = max(min(int(movement), 3), -3) # fix to range [-3, 3]
                while movement:
                    if movement > 0:
                        if testmaze.is_permissible(robot_pos['location'], robot_pos['heading']):
                            robot_pos['location'][0] += dir_move[robot_pos['heading']][0]
                            robot_pos['location'][1] += dir_move[robot_pos['heading']][1]
                            movement -= 1
                        else:
                            if verbose:
                                print("Movement stopped by wall. Robot at {0},{1} But thinks it is as {2},{3}".format(robot_pos['location'][0], robot_pos['location'][1],
                                      testrobot.location[0], testrobot.location[1]))
                            movement = 0
                    else:
                        rev_heading = dir_reverse[robot_pos['heading']]
                        if testmaze.is_permissible(robot_pos['location'], rev_heading):
                            robot_pos['location'][0] += dir_move[rev_heading][0]
                            robot_pos['location'][1] += dir_move[rev_heading][1]
                            movement += 1
                        else:
                            if verbose:
                                print("Movement stopped by wall. Robot at {0},{1} But thinks it is as {2},{3}".format(robot_pos['location'][0], robot_pos['location'][1],
                                      testrobot.location[0], testrobot.location[1]))
                            movement = 0
    
                # check for goal entered
                goal_bounds = [testmaze.dim/2 - 1, testmaze.dim/2]
                if robot_pos['location'][0] in goal_bounds and robot_pos['location'][1] in goal_bounds:
                    hit_goal = True
                    if run != 0:
                        runtimes.append(total_time - sum(runtimes))
                        run_active = False
                        if verbose: print("Goal found; run {} completed!".format(run))
    
        # Report score if robot is successful.
        if run == 0:
            Xex.append(robot_pos['location'][0])
            Yex.append(robot_pos['location'][1])
        else:
            Xrn.append(robot_pos['location'][0])
            Yrn.append(robot_pos['location'][1])
        if len(runtimes) == 2:
            if verbose: print("Task complete! Score: {:4.3f}".format(runtimes[1] + train_score_mult*runtimes[0]))
            if verbose: print("First run: {0}, second run: {1}".format(runtimes[0], runtimes[1]))
        else:
            runtimes.append(total_time)
            if verbose: print("Robot failed to complete maze")
        if showplot:
            plt.figure(figsize=(12,12))
            for x in range(testmaze.dim):
                for y in range(testmaze.dim):
                    if not testmaze.is_permissible([x,y], 'up'):
                        plt.plot([x-0.5, x+0.5], [y+0.5, y+0.5], 'k-', linewidth=3)
                    if not testmaze.is_permissible([x,y], 'down'):
                        plt.plot([x-0.5, x+0.5], [y-0.5, y-0.5], 'k-', linewidth=3)
                    if not testmaze.is_permissible([x,y], 'right'):
                        plt.plot([x+0.5, x+0.5], [y-0.5, y+0.5], 'k-', linewidth=3)
                    if not testmaze.is_permissible([x,y], 'left'):
                        plt.plot([x-0.5, x-0.5], [y-0.5, y+0.5], 'k-', linewidth=3)
        
            plt.plot(Xex,Yex, 'rs', markersize=16, alpha=0.25)
            plt.plot(Xrn, Yrn, 'b-', linewidth=6)
            plt.xlim(-1, testmaze.dim)
            plt.ylim(-1,testmaze.dim)
        
        return runtimes[1] + train_score_mult*runtimes[0]
        
    def test(self, trials=10, maze_list=None):
        '''
        Prints average score of bot through test mazes
        trials: number of trials to average over
        maze_list: list of maze files to run the bot through,
        defaults to the given test_maze_0x files
        '''
        if not maze_list:
            maze_list = ['test_maze_01.txt', 'test_maze_02.txt',
                         'test_maze_03.txt']
        output = {}
        for m in maze_list:
            score = sum([self.run_maze(m, verbose=False, showplot=False) for t in range(trials)]) / trials
            print("{0}: {1:.2f}".format(m, score))
            output[m] = score
        return output
        
class BenchmarkBot(Robot):
    '''
    Benchmark robot moves randomly at all times.
    Inherits from Robot class
    '''
    def next_move(self, sensors):
        '''Takes sensor reading, and returns movement command of rotation
        and distance.'''
        self.look_around(sensors)
        self.visited[tuple(self.location)] += 1
        
        #The robot is required to explore until it finds the goal
        if self.found_goal() and self.explore:
            self.location = (0,0)
            self.heading = 'up'
            self.explore = False
            return 'Reset', 'Reset'
            
        #The random bot just picks a random valid move, and moves there
        target = random.choice([space for space in self.maze_map[self.location]])
        r,d = self.calc_move(target)
        if r == -90: self.heading = Robot.left_turn[self.heading]
        elif r == 90: self.heading = Robot.right_turn[self.heading]
        self.location = target
        return r,d
        
class BetterBenchmarkBot(Robot):
    '''
    A better benchmark robot moves randomly to explore the maze, but then
    takes shortest path once goal is found.
    Inherits from Robot class
    '''
    def explore_move(self):
        '''Pick a random valid move to explore'''
        target = random.choice([space for space in self.maze_map[self.location]])
        r,d = self.calc_move(target)
        if r == -90: self.heading = Robot.left_turn[self.heading]
        elif r == 90: self.heading = Robot.right_turn[self.heading]
        self.location = target
        return r,d
        
    def next_move(self, sensors):
        '''Takes sensor reading, and returns movement command of rotation
        and distance.'''
        self.look_around(sensors)
        self.visited[tuple(self.location)] += 1
        
        #The robot is required to explore until it finds the goal
        if self.found_goal() and self.explore:
            self.location = (0,0)
            self.heading = 'up'
            self.explore = False
            return 'Reset', 'Reset'
            
        if self.explore:
            return self.explore_move()
        else:
            return self.path_move()
            
        
class HeuristicOne(Robot):
    '''
    First attempt at a heuristic looks for an adjacent square that hasn't been
    explored yet.  If there isn't one, it looks for an adjacent square that
    has been visited the fewest times.
    '''
    def __init__(self, maze_dim,explore_frac=0.5):
        '''
        explore_frac is what percentage of maze squares should be explored
        before starting on the second run.        
        '''
        super().__init__(maze_dim)
        self.explore_frac = explore_frac
        
    def explore_move(self):
        '''Picks a nearby space to move to randomly, with unexplored spaces 
        favored.  While exploring, we only move one space at a time to prevent
        backtracking as much as possible.  Returns rotation and distance'''
        options = []
        #First, look for un-visited spaces
        for n in [(self.location[0]+1, self.location[1]),(self.location[0], self.location[1]+1),
                  (self.location[0]-1, self.location[1]),(self.location[0], self.location[1]-1)]:
            if n in self.maze_map[tuple(self.location)] and n not in self.visited:
                    options.append(n)
        #if there are none, randomly pick from those we have visited the fewest number of times
        if not options:
            options = [min([x for x in self.maze_map[tuple(self.location)]], key=lambda z: self.visited[z])]
        choice = random.choice(options)
        
        r, d = self.calc_move(choice)
        self.location = choice
        if r == 90:
            self.heading = Robot.right_turn[self.heading]
        elif r == -90:
            self.heading = Robot.left_turn[self.heading]
        return r,d

    def next_move(self, sensors):
        self.look_around(sensors)
        self.visited[tuple(self.location)] += 1
        total_sq = self.maze_dim**2
        if self.explore:
            if self.found_goal() and (len(self.visited) >= self.explore_frac*total_sq):
                self.location = (0,0)
                self.heading = 'up'
                self.explore = False
                return 'Reset', 'Reset'
            else:
                return self.explore_move()
        else:
            return self.path_move()
            

class HeuristicTwo(Robot):
    '''
    Second idea for a heuristic picks the closest space we haven't visited yet
    and finds the shortest path to it.
    '''
    def __init__(self, maze_dim):
        super().__init__(maze_dim)
        self.explore_path = [] #Where we store a temporary path to the next
                               #unexplored space
        
    def explore_move(self):
        '''Finds the nearest un-visited space and paths towards it'''            
        if not self.explore_path:
            unvisited = [loc for loc in self.maze_map.keys() if not self.visited[loc]]
            paths = {loc: self.gen_path(target=loc)[1:] for loc in unvisited}
            closest = min(unvisited, key=lambda z: len(paths[z]))
            self.explore_path = paths[closest]
        choice = self.explore_path.pop(0)
        
        r, d = self.calc_move(choice)
        self.location = choice
        if r == 90:
            self.heading = Robot.right_turn[self.heading]
        elif r == -90:
            self.heading = Robot.left_turn[self.heading]
        return r,d

    def next_move(self, sensors):
        self.look_around(sensors)
        self.visited[tuple(self.location)] += 1
        
        if self.explore:
            if self.found_goal():
                self.location = (0,0)
                self.heading = 'up'
                self.explore = False
                return 'Reset', 'Reset'
            else:
                return self.explore_move()
        else:
            return self.path_move()
            
class ManhattanBot(HeuristicTwo):
    '''
    Instead of finding the closest unexplored space to the robot,
    ManhattanBot paths to the unexplored space closest to the goal, based
    on the Manhattan distance function.
    '''
    def explore_move(self):
        '''Finds the nearest un-visited space which is closest to
        the goal area and paths towards it'''
        def manhattan(x):
            return abs(x[0] - self.goal_bounds[0]+0.5) + abs(x[1] - self.goal_bounds[0]+0.5)
            
        if not self.explore_path:
            unvisited = [loc for loc in self.maze_map.keys() if not self.visited[loc]]
            paths = {loc: self.gen_path(target=loc)[1:] for loc in unvisited}
            closest = min(unvisited, key=lambda z: manhattan(z))
            self.explore_path = paths[closest]
        choice = self.explore_path.pop(0)
        
        r, d = self.calc_move(choice)
        self.location = choice
        if r == 90:
            self.heading = Robot.right_turn[self.heading]
        elif r == -90:
            self.heading = Robot.left_turn[self.heading]
        return r,d
        
class PotentialBot(Robot):
    def __init__(self, maze_dim):
        super().__init__(maze_dim)
        self.Vmax = 2 * maze_dim
        self.potential = {}
        l, h = self.goal_bounds
        for i in range(maze_dim):
            for j in range(maze_dim):
                x = min(abs(i-l), abs(i-h))
                y = min(abs(j-l), abs(j-h))
                self.potential[(i,j)] = x + y
                
    def next_move(self, sensors):
        '''Takes sensor reading, and returns movement command of rotation
        and distance.'''
        self.look_around(sensors)
        self.visited[tuple(self.location)] += 1
        
        #The robot is required to explore until it finds the goal
        if self.found_goal() and self.explore:
            self.location = (0,0)
            self.heading = 'up'
            self.explore = False
            return 'Reset', 'Reset'
            
        if self.explore:
            if sensors == [0,0,0]:
                self.potential[self.location] = self.Vmax
            return self.explore_move()
        else:
            return self.path_move()
    
    
    def explore_move(self):
        options = len(self.maze_map[self.location])
        if options > 1:
            self.potential[self.location] *= 2#+= options
        
        choice = min([loc for loc in self.maze_map[self.location]], key=lambda x: self.potential[x])
        
        r, d = self.calc_move(choice)
        self.location = choice
        if r == 90:
            self.heading = Robot.right_turn[self.heading]
        elif r == -90:
            self.heading = Robot.left_turn[self.heading]
        return r,d