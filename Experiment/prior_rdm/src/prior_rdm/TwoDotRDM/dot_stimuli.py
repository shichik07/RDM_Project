

# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:20:31 2020

@author: juliu
"""

#%reset
import random
import numpy as np
from numpy.matlib import repmat
from prior_rdm.params import * # import fixed parameter 



class RDM_kinematogram(object):
    '''
        Functions to implement a random dot kinematogram in Psychopy using the 
    elementarray function. Two algorithms are implemented. The Movshon-Newsome 
    algorithm and the Brownian-Motion algorithm for randomly moving dots with 
    different coherence levels. For a more thorough overview of advantages and 
    disadvantages see Pilly and Seitz 2009
        ----------
    '''
    
    def __init__(self, 
                 alg=ALG, 
                 dot_speed = DOT_SPEED,  
                 dot_density = DOT_DENSITY, 
                 fieldsize = FIELD_SIZE_DOT, 
                 center = CENTER,  
                 groups = GROUP_NR, 
                 rgbs = PRTC_FULL_COL, # just default, will not be shown
                 frameRate = REFRESH,
                 Jitter = JITTER_UPDATE):
        
        '''
        Initilization of the dots with parameters of choice
        ----------
        
        
        Parameters
        ----------
        alg: string - BM for Browninan Motion or MN for Movshon-Newsome dot updating
        dot_speed: float - Speed of dot motion in deg visual angle per frame
        dot_density: float - Average number of dots on apperture
        fieldsize: list - Size of squared apperture
        center: list - Center coorodinates of apperture
        groups: int - Number of groups - 1 or 2, actually only 2 works
        rgbs: list - default stimulus colors - will not actually be shown
        frameRate: int - monitor refreshrate
        Jitter:  int - to increase task difficulty coherent motion is only updated randomly on every nth(Jitter trial)
        
        Returns
        -------
        '''
        """ Initialize with algorithm choice """
        
        if alg != 'MN' and alg != 'BM':
            raise ValueError('The RDM algorithm you requested does not exist. '
                             'Please specify either "MN" for the Movshon-Newsome '
                             'algorithm, or "BM" for the Brownian motion algorithm') 
        # Check the dot number
        #fieldsize for now by default 14.8 degree for convenience so that we get 60 dots -
        # which is devisible by 6 (2 dot groups with three interlaced sequences)
        if groups == 2:
            self.n_dot = int(np.ceil(dot_density*np.square(fieldsize[0])/frameRate)) # number of dots
            if (self.n_dot%6) != 0:
                raise ValueError('Because you want to display two distinct dot_populations'
                                 ' with three distinct presentation sequences, the total'
                                 ' number of dots must be divisible by 6.')
        elif groups == 1:
            self.n_dot = int(np.ceil(dot_density*np.square(fieldsize[0])/frameRate)) # number of dots
            if self.n_dot%6 != 0:
                raise ValueError('Because you want to display one dot_population'
                                 ' with three distinct presentation sequences, the total'
                                 ' number of dots must be divisible by 6. 6?? Yes 6. Because '
                                 'coherence is defined with respect to two dots. In order to'
                                 ' make the results comparable.')
        else:
             raise ValueError('You must specify the groups parameter to the number of'
                              ' dot populations that you would like to display.' 
                              ' At present either one or teo dot populations can be ' 
                              'displayed.')  
             
        """ IMPORTANT! Coherence is calculated for one group the same way as for two groups. 
        Reason being, we want overall coherence to be the same for one and two groups in our
        paradigm. As such coherence is defined with respect to two groups (quite arbitrary, I know).
        """
        if alg == "BM":
            # we only show "one" dot pop not three - hence we need three times the number of dots
            self.n_dot = self.n_dot*3 
        
        self.speed = dot_speed # dot displacement
        self.center = center
        self.groups = groups # number of dot groups
        self.rgbs = rgbs # colors used
        self.frameRate = frameRate # Monitor Refreshrate
        self.fieldsize = fieldsize
        self.bounds_x = 0.5*self.fieldsize[0] + self.center[0] # determine aperature bounds on the x axis
        self.bounds_y = 0.5*self.fieldsize[1] + self.center[1] # determine aperature bounds on the y axis
        self.alg = alg
        self.Jitter = Jitter
        
    def create_dots(self):
        '''
        Outputs a matrix that contains information of each dot by column: 
        indices, population-membership, one column for each respective RGB value 
        and x,y coordinates of each dot
        ----------
        
        
        Parameters
        ----------
        
        Returns
        -------
        
        colors.tolist(): list - list with the specific color to each individual dot
        pos.tolist(): list - coordinates to every dot
        
        '''
       
        # first we create three sequences by creating a three dimensional array
        self.ind = np.arange(0,self.n_dot,1)
        # add a grouping variable and color codes
        if self.groups == 2:
            # add group
            self.ind =  np.column_stack((self.ind, repmat(np.array([1,2]), 1, int(self.n_dot/2)).T))
            # add rgb color codes
            self.ind =  np.column_stack((self.ind, repmat(self.rgbs, int(self.n_dot/2), 1)))
        else:
            # add group
            self.ind =  np.column_stack((self.ind, repmat(np.array([1]), 1, self.n_dot).T))
            # add rgb color codes
            self.ind =  np.column_stack((self.ind, repmat(np.array(self.rgbs), self.n_dot, 1)))
        # Then we set the coordinates for all dots (one array x, the other y)
        dot_cart = np.array([self.randomize_coord(self.n_dot, 0), 
                      self.randomize_coord(self.n_dot, 1)]).T
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
    
    def update_dots(self, frame):
        '''
        Function to update the dot positions - randomly selecting dots of the 
        target group to move coherently and the rest to reapear in random positions
        ----------
        
        
        Parameters
        ----------
        
        frame: int - frame number for the update - required for MN because only specific dots are updated at specific frames - ignored for BM
        
        Returns
        -------
        
        colors.tolist(): list - list with the specific color to each individual dot
        pos.tolist(): list - coordinates to every dot
        
        '''
        
        #quick fix for the BM -algorithm, which consitutes of only a single dot population
        if self.alg == 'BM':
            frame = 0
        
        #calculate dot displacement in degree of viusal angle
        displacement_x = self.speed*np.sin(self.direct*np.pi/180)/self.frameRate
        displacement_y = self.speed*np.cos(self.direct*np.pi/180)/self.frameRate
        
        #get indices of coherently moving dots
        coh_ind = self.get_coherent_dots(frame)
        
        # update the relevant indexes for coherent dots;
        self.ind[frame%3][coh_ind,5] +=  displacement_x
        self.ind[frame%3][coh_ind,6] +=  displacement_y
        
        # get the noise dot indices
        noise = np.ones(self.n_dot//3, dtype=bool)
        noise[coh_ind] = False
        
        #update the noiserandrange(10) dot indices
        if self.alg == 'MN':# for Movshon-Newsome updating (random speed and direction)
            # randomize x and y coordinates for the noise dots
            self.ind[frame%3][noise,5:7] = np.array([
                self.randomize_coord(np.count_nonzero(noise), 0),
                 self.randomize_coord(np.count_nonzero(noise), 1)]).T
        elif self.alg == 'BM': # for Brownian Motion updating (random direction, fixed speed)
            self.ind[frame%3][noise,5:7] = self.bm_random_loc(
                self.ind[frame%3][noise,5], 
                self.ind[frame%3][noise,6])
            
        # if any dot exceeds the limit of our circle, randomly redraw it
        # took this strategy from Arkady Zgonnikov's implementation:
        # "https://github.com/cherepaha/Gamble_RDK/blob/master/ui/rdk_mn.py"
        redraw = self.exceed_bounds(self.ind[frame%3][:,5:7])
        #if we find any coordinates in excess redraw them
        if redraw is not False:
            self.ind[frame%3][redraw,5:7] = np.array([self.randomize_coord(redraw.size, 0),
                    self.randomize_coord(redraw.size, 1)]).T
       
        # because I believe that the dots are drawn in a serial manner i shuffle all
        # the order to be on the safe side. Otherwise if two 
        # randomly occupy the same position one superimposes the other. Not shuffling 
        # might lead to one group of dots superimposing the other more often than the
        # other - just because of the order that I created the groups here. Probably 
        # I am overthinking, but it cannot hurt.
        np.random.shuffle(self.ind[frame%3])
        #noticed the input format for psychopy are lists are pairwise lists
        colors = self.ind[frame%3][:,2:5]
        pos = self.ind[frame%3][:,5:7]
        return  colors.tolist(), pos.tolist()

    
    def exceed_bounds(self, coord):
        '''
        Function to determine if specific dots exceed the bounds of our aperture.
        Returns indexes of dots that are in excess
        ----------
        
        
        Parameters
        ----------
        
        coord: list - coordinates to every dot being updated
        
        Returns
        -------
        
        redraw: bol/list - returns False if dots do not exceed apperture, else a list of dots exceeding the apperture
        
        '''
        
        if np.any((coord[:,0] < -self.bounds_x) | (coord[:,0] > self.bounds_x) 
                  | (coord[:,1] < -self.bounds_y) | (coord[:,1] > self.bounds_y), axis=0):
            # find row indices where bounds are exceeded for X coordinates
            redraw = np.nonzero((coord[:,0] > self.bounds_x) | (coord[:,0] < -self.bounds_x))
            # find row indices where bounds are exceeded for Y coordinates
            redraw = np.hstack((redraw,  np.nonzero((coord[:,1] > self.bounds_y) | (coord[:,1] < -self.bounds_y))))
            # find unique row indices where bounds are exceeded 
            redraw = np.unique(redraw)
        else:
            redraw = False
        return redraw
        
    def randomize_coord(self, x, axis):
        '''
        Find random coordinate within the bounds of the apperture 
        ----------
        
        
        Parameters
        ----------
        
         x: int - number of random draws/ dots to be updated
         axis: int - do we need to update the x (==0) or y (==1) axis coordinates
        
        Returns
        -------
        
        rand_loc: float - returns fresh random location within apperture bounds
        
        '''
        
        if axis == 0: #name axis in case aperture isn't square or center is elsewhere
            ax = 0
        elif axis == 1:
            ax = 1
        rand_loc = (np.random.rand(x)-.5)*self.fieldsize[ax] + self.center[ax]
        return rand_loc
    
    def get_coherent_dots(self, frame):
        '''
        Function that randomly selects coherently moving dots for either one or 
        two randomly moving dot populations
        ----------
        
        
        Parameters
        ----------
        
        coh_ind: int - frame number for the update - required for MN because only specific dots are updated at specific frames - ignored for BM
        
        Returns
        -------
        
        coh_ind: list - list of dot indexes to be updated coherently
        
        '''
        
        if type(self.coherence) is float:
            update_jitter = random.randrange(self.Jitter)
            if update_jitter == (self.Jitter-1):
                num_coh = int(self.coherence*int(self.n_dot//3)) # number of coherently moving dots (per group)
            else:
                num_coh = 0
                
            # indexes of coherently moving dots
            coh_ind = np.random.choice(range(int(self.n_dot//3)), num_coh, replace = False)
            return coh_ind
        elif len(self.coherence) == 2:
            update_jitter = random.randrange(self.Jitter)
            if update_jitter == (self.Jitter-1):
                num_coh = np.rint(np.dot(self.coherence,int(self.n_dot//6))) # number of coherently moving dots (per group)
            else:
                num_coh = [0,0]
            # Get the indices for both Dot pops
            Bol_pop1 = self.ind[frame%3][:,1]==1
            Pop_1 = np.where(Bol_pop1)[0]
            Pop_2 = np.where(~Bol_pop1)[0]
            # indexes of coherently moving dots
            coh_ind = np.random.choice(Pop_1, int(num_coh[0]), replace = False)
            coh_ind = np.concatenate((coh_ind, np.random.choice(Pop_2, int(num_coh[1]), replace = False)))
            return coh_ind
        else:
            raise ValueError('Please provide one or two coherence Values')
    
    def update_params(self, direction, color, coherence):
        '''
        Function to update class parameters for direction color and coherence. Done because we do not want to create a new RDM object class for every trial
        ----------
        
        
        Parameters
        ----------
        
        direction: str - coherent movement will be to the left or right
        color: list - list with the specific color to each individual dot
        coherence: list - percent of coherently moving dots in each dot color group
        
        Returns
        -------
        
        '''
        self.rgbs = color
        self.coherence = coherence[0]
        if direction == 'left': # convert direction in degree
            self.direct = 270
        elif direction == 'right':  # convert direction in degree
            self.direct = 90
            
    def bm_random_loc(self, start_x, start_y):
        '''
        Function to update noise dots if algorithm selected is BM. MV has random speed and direction, for BM speed is fixed. 
        Hence we only randomlöy draw a direction in degrees, then update coordinates.
        ----------
        
        
        Parameters
        ----------
        
        start_x: list - x coordinates of noise dots
        start_y: list - y coordinates of noise dots
        
        
        Returns
        -------
        
        new_coord: updated coordinates to noise dots
        
        '''
        rdm_theta = np.random.rand(len(start_x)) *2*np.pi # random angle on a circle
        new_x = start_x + self.speed*np.cos(rdm_theta)/self.frameRate # "speed" is treated as the radius
        new_y = start_y + self.speed*np.sin(rdm_theta)/self.frameRate
        new_coord = np.column_stack((new_x, new_y))
        return new_coord