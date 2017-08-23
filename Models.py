# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 15:56:01 2017

@author: EKish
"""
from Robot import Robot
import random

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
            
        
class CautiousBot(Robot):
    '''
    First attempt at a heuristic looks for an adjacent square that hasn't been
    explored yet.  If there isn't one, it looks for an adjacent square that
    has been visited the fewest times.
    '''
    def __init__(self, maze_dim,explore_frac=0.0):
        '''
        explore_frac is what percentage of maze squares should be explored
        before starting on the second run.        
        '''
        super().__init__(maze_dim)
        if 'explore_frac' not in self.__dict__:
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
            

class FrontierBot(Robot):
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
            
class ManhattanBot(FrontierBot):
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
            self.potential[self.location] *= 2
        
        choice = min([loc for loc in self.maze_map[self.location]], key=lambda x: self.potential[x])
        
        r, d = self.calc_move(choice)
        self.location = choice
        if r == 90:
            self.heading = Robot.right_turn[self.heading]
        elif r == -90:
            self.heading = Robot.left_turn[self.heading]
        return r,d