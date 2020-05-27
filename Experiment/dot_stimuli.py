# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:20:31 2020

@author: juliu
"""
import random
import numpy as np


# Define Experimental parameter
frames = 60
direction = "left"
n_dots = 200
trgt_size = 30
dot_xys = []
coh_dot = random.sample(range(n_dots),  trgt_size) 
dot_speed = 5
print(coh_dot)
a = 0

class RDM_kinematogram(object):
    """ Functions to implement a random dot kinematogram in Psychopy. Two 
    algorithms are implemented. The Movshon-Newsome algorithm and the Brownian-Motion
    algorithm for randomly moving dots with different coherence levels. For a 
    more thorough overview of advantages and disadvantages see Pilly and Seitz
    2009"""
    def __init__(self, alg='MN', dot_speed = 5):
        """ Initialize with algorithm choice """
        if alg == 'MN':
            # Movshon Newsome
            self.rdm_alg = 'MN'
        elif alg == 'BM':
            self.rdm_alg = 'BM'
        else:
            raise ValueError('The RDM algorithm you requested does not exist. '
                             'Please specify either "MN" for the Movshon-Newsome '
                             'algorithm, or "BM" for the Brownian motion algorithm'
                    )
        self.speed = dot_speed
        
    def create_dots(self, dot_num):
        dot_num = 180
        # first we create three sequences by creating a three dimensional array
        ind = np.arange(0,dot_num,1).reshape(3,dot_num//3)
        # randomly assign indexes to sequence
        np.random.shuffle(ind)
        
        # Then we set the coordinates for all dots (one array x, the other y)
        dot_cart = np.array([np.random.randint(-200,200, 200), 
                      np.random.randint(-200,200, 180)])
        
        return dot_cart, ind
        
    def update_dots(self, frame, coherence):
        frame = 17
        # determine which sequence is updated
        frame%3
        

for frame in range(frames):
    for dot in range(n_dots):
        if frame == 0: # randomly assign initial position
            dot_x = random.uniform(-200,200)
            dot_y = random.uniform(-200,200)
            dot_xys.append([dot_x,dot_y])
        else:
            if coh_dot.count(dot) == 1: # determine if dot is in target group via count function
                if dot_xys[dot][0] + dot_speed < 200: # if the dot is still within the window
                    dot_xys[dot][0] = dot_xys[dot][0] + dot_speed
                    dot_xys[dot][1] = dot_xys[dot][1] + random.randint(-dot_speed, dot_speed)
                else: # if the dot would move beyond
                    dot_xys[dot][0] = dot_xys[dot][0] + dot_speed - 400
                    dot_xys[dot][1] = dot_xys[dot][1] + random.randint(-dot_speed, dot_speed)
            else: # update the remaining dots
                dot_xys[dot][0] = dot_xys[dot][0] + random.randint(-dot_speed, dot_speed)
                dot_xys[dot][1] = dot_xys[dot][1] + random.randint(-dot_speed, dot_speed)
                if dot_xys[dot][0] > 200:
                    dot_xys[dot][0] = dot_xys[dot][0] - 400
                elif dot_xys[dot][0] < -200:
                    dot_xys[dot][0] = dot_xys[dot][0] + 400
                elif dot_xys[dot][1] > 200:
                    dot_xys[dot][1] = dot_xys[dot][1] - 400
                elif dot_xys[dot][1] < -200:
                    dot_xys[dot][1] = dot_xys[dot][1] + 400
                else:
                    pass
    print(dot_xys[17][0])
                
                    
                
                
                