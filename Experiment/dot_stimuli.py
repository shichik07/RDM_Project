# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:20:31 2020

@author: juliu
"""

%reset
import random
import numpy as np


class RDM_kinematogram(object):
    """ Functions to implement a random dot kinematogram in Psychopy. Two 
    algorithms are implemented. The Movshon-Newsome algorithm and the Brownian-Motion
    algorithm for randomly moving dots with different coherence levels. For a 
    more thorough overview of advantages and disadvantages see Pilly and Seitz
    2009"""
    def __init__(self, alg='MN', dot_speed = 5, coherence = 0.4, 
                 direction = 'left', dot_density = 0.167, num_dot = 180, 
                 radius = 200):
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
        self.speed = dot_speed # dot displacement
        self.n_dot = num_dot # numer of dots
        self.num_coh = int(coherence*(num_dot/3)) #  coherently moving dots each frame
        self.dim = radius # display dimensions
        if direction == 'left':
            self.direct = - 1
        elif direction == 'right':
            self.direct = 1
        
        
    def create_dots(self):
        # first we create three sequences by creating a three dimensional array
        self.ind = np.arange(0,self.n_dot,1).reshape(3,self.n_dot//3)
        # randomly assign indexes to sequence
        np.random.shuffle(self.ind)
        # Then we set the coordinates for all dots (one array x, the other y)
        self.dot_cart = np.array([self.randomize_coord(self.n_dot), 
                      self.randomize_coord(self.n_dot)])
        # noticed the input format for psychopy are lists are pairwise lists
        out_list = self.dot_cart.T
        return out_list.tolist()
    
        
    def update_dots(self, frame):
        # indexes of coherently moving dots
        coh_ind = np.random.choice(self.ind[[frame%3],...].flat, 
                                   self.num_coh, replace = False)
        # update the relevant indexes for coherent dots; self.direct negative 
        # for leftward motion
        self.dot_cart[1,coh_ind] +=  self.speed*self.direct 
        # if any dot exceeds the limit of our circle, randomly redraw it
        # took this strategy from Arkady Zgonnikov's implementation:
        # "https://github.com/cherepaha/Gamble_RDK/blob/master/ui/rdk_mn.py"
        if any(np.abs(self.dot_cart[1,coh_ind]) > self.dim):
            # find the relevant items outside 
            redraw = np.abs(self.dot_cart[1,coh_ind]) > self.dim
            redraw = coh_ind[redraw]
            # randomize x and y coordinates for the abarrant coherent dots
            self.dot_cart[...,redraw] = np.array([self.randomize_coord(redraw.size),
                    self.randomize_coord(redraw.size)])
        # update the noise dots and if exist the redraw coordinates
        noise = np.isin(self.ind[[frame%3],...], coh_ind, invert=True)
        noise = self.ind[[frame%3],noise.flat]
         # randomize x and y coordinates for the noise dots
        self.dot_cart[...,noise] = np.array([self.randomize_coord(noise.size),
                    self.randomize_coord(noise.size)])
        # noticed the input format for psychopy are lists are pairwise lists
        out_list = self.dot_cart.T
        return  out_list.tolist()
    
    
    def randomize_coord(self, x):
        # with this function we update noise dot locations randomly 
        ''' Note to self: in the final implementation including the BM 
        algorithm we need to distinguish here with updates of random speed
        and random direction for the MN algorithm and only random direction
        for the MN algorithm '''
        rand_loc = np.random.randint(-self.dim, self.dim, x)
        return rand_loc


"""
Playground
"""

x = RDM_kinematogram(direction='right')

some_pos = x.randomize_coord(20)
position = x.create_dots()
print(position)
for i in range(120):
    position2 = x.update_dots(i)
print(position2)



"""
Slow Version
"""

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
                
                    
                
                
                