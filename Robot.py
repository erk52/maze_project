# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 15:25:04 2017

@author: EKish
"""
from collections import Counter
import random

class Robot(object):
    '''A simulated micromouse robot'''
    

    left_turn = {'up': 'left', 'left': 'down', 'down': 'right', 'right': 'up'}
    right_turn = {'up': 'right', 'right': 'down', 'down': 'left', 'left': 'up'}
    dir_move = {'u': [0, 1], 'r': [1, 0], 'd': [0, -1], 'l': [-1, 0],
                    'up': [0, 1], 'right': [1, 0], 'down': [0, -1], 'left': [-1, 0]}
    
    def __init__(self, maze_dim, explore_frac=0.66):
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
        self.explore_frac = explore_frac
        self.path = []                  #Prior to second run, we determine the
                                        #optimal path

    def make_connection(self, square_1, square_2):
        '''Makes a connection in the graph maze_map between square_1 and square_2'''
        self.maze_map[square_1] = self.maze_map.get(square_1, set()).union([square_2])
        self.maze_map[square_2] = self.maze_map.get(square_2, set()).union([square_1])
    
    def look_around(self, sensors):
        '''Given sensor input data, find out what squares the robot can move to
        by checking wall distances to the left, center and right'''
        
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
        self.location = list(choice)
        if r == 90:
            self.heading = Robot.right_turn[self.heading]
        elif r == -90:
            self.heading = Robot.left_turn[self.heading]
        return r,d
        
    def calc_move(self, target):
        '''Determines rotation and distance to get to target space.  Takes a 
        position as a tuple, returns a rotation angle and distance.'''
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
    
    def next_move(self, sensors):
        '''Takes sensor reading, and returns movement command of rotation
        and distance.'''
        
        #If exploring, look around to generate map.
        if self.explore:
            self.visited[tuple(self.location)] += 1
            self.look_around(sensors)
            
            total_sq = self.maze_dim**2
            l, h = self.goal_bounds
            if (len(self.visited) >= self.explore_frac*total_sq) and self.at_goal():
                #We've explored enough.  Reset, and generate path to goal.
                print(self.location, self.goal_bounds)
                print("sending reset signal.  Robot thinks it is at ", self.location)
                self.location = (0,0)
                self.heading = 'up'
                self.explore = False
                self.path = self.gen_path()[1:]
                return 'Reset', 'Reset'
            
            #Otherwise, pick a space and move there.
            return self.explore_move()
        else:
            l, h = self.goal_bounds
            if self.at_goal():
                #Victory condition!
                print(self.location, self.goal_bounds)
                print("sending reset signal.  Robot thinks it is at ", self.location)
                return 'Reset', 'Reset'
            
            if not self.path:           #If something strange happened, regen
                self.path = self.gen_path()[1:]
            
            #Move to the next square in the path list
            target = self.path.pop(0)
            r,d = self.calc_move(target)
            #print('At ', self.location, " ", self.heading  ,' moving to ', target, ' with orders ', r, d)
            self.location = target
            if r == 90:
                self.heading = Robot.right_turn[self.heading]
            elif r == -90:
                self.heading = Robot.left_turn[self.heading]
            return r,d
            
    def gen_path(self):
        '''Breadth first search algorithm to find ending'''        
        
        start = tuple(self.location)
        l, h = self.goal_bounds
        end = None
        for e in [(l,l), (l, h), (h, l), (h,h)]:
            if self.maze_map.get(e, None):
                end = e
                break
        if not end:     #If we can't find the end, something bad happened
            raise Exception("End not in map")
        
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
        