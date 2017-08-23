# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 08:34:14 2017

@author: EKish
"""
import random
import matplotlib.pyplot as plt

def prim(size):
    '''Generate random maze using a verison of Prim's minimum spanning tree
    algorithm.  Returns a dict of adjacency lists.
    '''
    graph = {}
    in_maze = [(0,0)]
    not_in_maze = []
    for i in range(size):
        for j in range(size):
            graph[(i,j)] = set()
            if (i,j) != (0,0):
                not_in_maze.append((i,j))
                
    while not_in_maze:
        options = []
        for s in in_maze:
            neigh = [(s[0]+1,s[1]),(s[0]-1,s[1]),(s[0],s[1]+1),(s[0],s[1]-1)]
            for n in neigh:
                if n[0] in range(size) and n[1] in range(size) and n not in in_maze:
                    options.append((s,n))
        s1, s2 = random.choice(options)
        graph[s1].add(s2)
        graph[s2].add(s1)
        not_in_maze.remove(s2)
        in_maze.append(s2)
    lo, hi = size//2 - 1, size // 2  
    goal_sq = [(lo,lo), (lo,hi), (hi,lo), (hi,hi)]
    for i in range(4):
        for g in goal_sq[:i] + goal_sq[i+1:]:
            graph[goal_sq[i]].add(g)
    
 
    return graph
    
def print_maze(G):
    '''Generates maze visualization via matplotlib.  Returns figure object.'''
    fig, ax = plt.subplots()
    for sq in G.keys():
        x,y = sq
        if (x+1, y) not in G[sq]:
            ax.plot([x+0.5, x+0.5], [y-0.5, y+0.5], 'k-')
        if (x-1, y) not in G[sq]:
            ax.plot([x-0.5, x-0.5], [y-0.5, y+0.5], 'k-')
        if (x, y+1) not in G[sq]:
            ax.plot([x-0.5, x+0.5], [y+0.5, y+0.5], 'k-')
        if (x, y-1) not in G[sq]:
            ax.plot([x-0.5, x+0.5], [y-0.5, y-0.5], 'k-')
            
    return fig
    
def save_maze(G, file_name):
    '''Takes dict of adjacency lists as argument.  For each squares, checks
    for neighbors to calculate binary number.  Saves output to filename.'''
    sz = int(len(G)**0.5)
    outline = [str(sz)]
    for i in range(sz):
        line = []
        for j in range(sz):
            x,y = i,j
            string = [(x-1, y) in G[(i,j)], (x, y-1) in G[(i,j)], 
             (x+1, y) in G[(i,j)], (x, y+1) in G[(i,j)]]
            string = ''.join([str(int(z)) for z in string])
            num = int(string, 2)
            line.append(num)
        outline.append(','.join([str(a) for a in line]))
    
    f = open(file_name, 'w')
    f.write('\n'.join(outline))
    f.close()    
    
    return outline
    
def open_maze(maze_dim):
    '''Generates and saves totally open maze of any size'''
    output = [str(maze_dim)]
    output.append('3,' + '7,'*(maze_dim-2) + '6')
    for row in range(maze_dim-2):
        output.append('11,' + '15,'*(maze_dim-2) + '14')
    output.append('9,'+'13,'*(maze_dim-2)+'12')
    
    filename = 'open_maze_'+str(maze_dim)+'.txt'
    f = open(filename, 'w')
    f.write('\n'.join(output))
    f.close()