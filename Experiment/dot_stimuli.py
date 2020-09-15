# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:20:31 2020

@author: juliu
"""

%reset
import random
import numpy as np
from numpy.matlib import repmat



class RDM_kinematogram(object):
    """ Functions to implement a random dot kinematogram in Psychopy. Two 
    algorithms are implemented. The Movshon-Newsome algorithm and the Brownian-Motion
    algorithm for randomly moving dots with different coherence levels. For a 
    more thorough overview of advantages and disadvantages see Pilly and Seitz
    2009"""
    def __init__(self, alg='MN', dot_speed = 5, coherence = 0.4, 
                 direction = 'left', dot_density = 0.167, num_dot = 180, 
                 radius = 200, groups = 2, rgbs = [[ -1,0,1],[ 1,0,1]]):
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
            
        """ Check Number of dots """
        if groups == 2:
            if num_dot%6 == 0:
                self.n_dot = num_dot # numer of dots
            else:
                raise ValueError('Because you want to display two distinct dot_populations'
                                 ' with three distinct presentation sequences, the total'
                                 ' number of dots must be divisible by 6.')
        elif groups == 1:
            if num_dot%3 == 0:
                self.n_dot = num_dot # numer of dots
            else:
                raise ValueError('Because you want to display one dot_population'
                                 ' with three distinct presentation sequences, the total'
                                 ' number of dots must be divisible by 3.')
        else:
             raise ValueError('You must specify the groups parameter to the number of'
                              ' dot populations that you would like to display.' 
                              ' At present either one or teo dot populations can be 
                              displayed.')
             
        self.speed = dot_speed # dot displacement
        self.n_dot = num_dot # numer of dots
        self.num_coh = int(coherence*(num_dot/3)) #  coherently moving dots each frame
        self.dim = radius # display dimensions
        if direction == 'left':
            self.direct = - 1
        elif direction == 'right':
            self.direct = 1
            
        def create_dots(self):
        ''' Outputs a matrix that contains information of each dot by column: 
        indices, population-membership, one column for each respective RGB value 
        and x,y coordinates of each dot'''
        # first we create three sequences by creating a three dimensional array
        self.ind = np.arange(0,self.n_dot,1)
        # add a grouping variable and color codes
        if self.groups == 2:
            # group
            self.ind =  np.column_stack((self.ind, repmat(np.array([1,2]), 1, int(self.n_dot/2)).T))
            # add rgb color codes
            self.ind =  np.column_stack((self.ind, repmat(self.rgbs, int(self.n_dot/2), 1)))
        else:
            self.ind =  np.column_stack((self.ind, repmat(np.array([1]), 1, self.n_dot).T))
            # add rgb color codes
            self.ind =  np.column_stack((self.ind, repmat(np.array(self.rgbs), self.n_dot, 1)))
        # Then we set the coordinates for all dots (one array x, the other y)
        dot_cart = np.array([randomize_coord(self.dim, self.n_dot), 
                      randomize_coord(self.dim, self.n_dot)]).T
        ## add the random coordinates to our matrix
        self.ind =  np.column_stack((self.ind, dot_cart))
        # create three sequences by creating a three dimensional array. In only do 
        # bthis because it helps me to visualize and keep track of the different 
        # frame populations. A two dimensional frame would do fine as well.
        self.ind = np.vsplit(self.ind, 3)
        # noticed the input format for psychopy are lists are pairwise lists
        colors = self.ind[0][:,range(2,5)]
        pos = self.ind[0][:,range(5,7)]
        return colors.tolist(), pos.tolist()
            
#    def double_check_decorator(func):
#        def function_wrapper(self, frame):
#            pop_1 = self.dot_cart[...,self.ind[[0],...].flat].T.tolist()
#            pop_2 = self.dot_cart[...,self.ind[[1],...].flat].T.tolist()
#            pop_3 = self.dot_cart[...,self.ind[[2],...].flat].T.tolist()
#            print('Coordinates have been saved.')
#            out_list = func(self, frame)
#            if pop_1 ==  self.dot_cart[...,self.ind[[0],...].flat].T.tolist():
#                print('Population one did not change.')
#            else: 
#                print('Population one did change.')
#                
#            if pop_2 ==  self.dot_cart[...,self.ind[[1],...].flat].T.tolist():
#                print('Population two did not change.')
#            else: 
#                print('Population two did change.')
#                
#            if pop_3 ==  self.dot_cart[...,self.ind[[2],...].flat].T.tolist():
#                print('Population three did not change.')
#            else: 
#                print('Population three did change.')
#            return out_list
#        return function_wrapper
        
    
#    @double_check_decorator    
    def update_dots(self, frame):
        # All indexes in this frame
        all_ind = self.ind[frame%3][].flat
        # indexes of coherently moving dots
        coh_ind = np.random.choice(self.ind[[frame%3],...].flat, 
                                   self.num_coh, replace = False)
        # update the relevant indexes for coherent dots; self.direct negative 
        # for leftward motion
        self.dot_cart[0,coh_ind] +=  self.speed*self.direct 
        # if any dot exceeds the limit of our circle, randomly redraw it
        # took this strategy from Arkady Zgonnikov's implementation:
        # "https://github.com/cherepaha/Gamble_RDK/blob/master/ui/rdk_mn.py"
        if any(np.abs(self.dot_cart[0,coh_ind]) > self.dim):
            # find the relevant items outside 
            redraw = np.abs(self.dot_cart[0,coh_ind]) > self.dim
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
        out_list = self.dot_cart[...,all_ind].T
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
coord =np.array([
        [ 1, 0],
        [ 1, 0]]).tolist()

x = RDM_kinematogram(direction='right')


position = x.create_dots()
print(len(position[0:60]))
for i in range(120):
    position2 = x.update_dots(2)
    position3 = x.update_dots(i)
    position2 == position3
    print(position2)




dim = 200
n_dot = 180
groups = 2
def randomize_coord(dim, x):
    # with this function we update noise dot locations randomly 
    ''' Note to self: in the final implementation including the BM 
    algorithm we need to distinguish here with updates of random speed
    and random direction for the MN algorithm and only random direction
    for the MN algorithm '''
    rand_loc = np.random.randint(-dim, dim, x)
    return rand_loc

def create_dots(dim, n_dot):
    ''' Outputs a matrix that contains information of each dot by column: 
    indices, population-membership, one column for each respective RGB value 
    and x,y coordinates of each dot'''
    # first we create three sequences by creating a three dimensional array
    ind = np.arange(0,n_dot,1)
    # add a grouping variable and color codes
    if groups == 2:
        # group
        ind =  np.column_stack((ind, repmat(np.array([1,2]), 1, int(n_dot/2)).T))
        # add rgb color codes
        ind =  np.column_stack((ind, repmat(rgbs, int(n_dot/2), 1)))
    else:
        ind =  np.column_stack((ind, repmat(np.array([1]), 1, n_dot).T))
        # add rgb color codes
        ind =  np.column_stack((ind, repmat(np.array(rgbs), n_dot, 1)))
    # Then we set the coordinates for all dots (one array x, the other y)
    dot_cart = np.array([randomize_coord(dim, n_dot), 
                  randomize_coord(dim, n_dot)]).T
    ## add the random coordinates to our matrix
    ind =  np.column_stack((ind, dot_cart))
    
    # create three sequences by creating a three dimensional array. In only do 
    # bthis because it helps me to visualize and keep track of the different 
    # frame populations. A two dimensional frame would do fine as well.
    ind = np.vsplit(ind, 3)
    #randomly select one of the lists as output and return a color and coordinate
    # matrix
    ret = random.randint(0,2)
    # noticed the input format for psychopy are lists are pairwise lists
    colors = ind[ret][:,range(2,5)]
    pos = colors = ind[ret][:,range(5,7)]
    return colors.tolist(), pos.tolist()

rgbs = [1,2,3]
rgbs = [[ -1,0,1],[ 1,0,1]]
rgbs[0][0]

a0 = repmat(np.array([1,2]), int(n_dot/2), 1)
repmat(a0, 2, 3)

a = create_dots(dim, n_dot)
ind = np.arange(0,n_dot,1)
print(ind)
        # randomly assign indexes to sequence
np.random.shuffle(ind)
        # create three sequences by creating a three dimensional array
ind = ind.reshape(3,n_dot//3)
print(ind)
np.random.shuffle(ind)
print(ind)
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
                
                    
                
                
                