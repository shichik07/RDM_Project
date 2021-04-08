

# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:20:31 2020

@author: juliu
"""

#%reset
import random
import numpy as np
from numpy.matlib import repmat



class RDM_kinematogram(object):
    """ Functions to implement a random dot kinematogram in Psychopy using the 
    elementarray function. Two algorithms are implemented. The Movshon-Newsome 
    algorithm and the Brownian-Motion algorithm for randomly moving dots with 
    different coherence levels. For a more thorough overview of advantages and 
    disadvantages see Pilly and Seitz 2009"""
    def __init__(self, 
                 alg='MN', 
                 dot_speed = 8,  
                 dot_density = 16.7, 
                 fieldsize = [14.8, 14.8], 
                 center = [0,0],  
                 groups = 2, 
                 t_group = 1,
                 rgbs = [[ -1,0,1],[ 1,0,1]], 
                 frameRate = 61):
        """ Initialize with algorithm choice """
        if alg == 'MN':
            # Movshon Newsome
            self.rdm_alg = 'MN'
        elif alg == 'BM':
            self.rdm_alg = 'BM' # not implemented yet - not sure if I will have the time
        else:
            raise ValueError('The RDM algorithm you requested does not exist. '
                             'Please specify either "MN" for the Movshon-Newsome '
                             'algorithm, or "BM" for the Brownian motion algorithm') 
        # Check the dot number
        #fieldsize for now by default 14.8 degree for convenience so that we get 60 dots -
        # which is devisible by 6 (2 dot groups with three interlaced sequences)
        if groups == 2:
            self.n_dot = int(np.ceil(dot_density*np.square(fieldsize[0])/frameRate)) # number of dots
            self.t_group = t_group # target group either zero or one
            if (self.n_dot%6) != 0:
                raise ValueError('Because you want to display two distinct dot_populations'
                                 ' with three distinct presentation sequences, the total'
                                 ' number of dots must be divisible by 6.')
        elif groups == 1:
            self.n_dot = int(np.ceil(dot_density*np.square(fieldsize[0])/frameRate)) # number of dots
            self.t_group = 0 
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
        self.speed = dot_speed # dot displacement
        self.center = center
        self.groups = groups # number of dot groups
        self.rgbs = rgbs # colors used
        self.frameRate = frameRate # Monitor Refreshrate
        self.fieldsize = fieldsize
        self.bounds_x = 0.5*self.fieldsize[0] + self.center[0] # determine aperature bounds on the x axis
        self.bounds_y = 0.5*self.fieldsize[1] + self.center[1] # determine aperature bounds on the y axis
        self.alg = alg    
        
    def create_dots(self):
        ''' Outputs a matrix that contains information of each dot by column: 
        indices, population-membership, one column for each respective RGB value 
        and x,y coordinates of each dot'''
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
        
        """ Function to update the dot positions - randomly selecting dots of the 
        target group to move coherently and the rest to reapear in random positions"""
        
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
        
        #update the noise dot indices
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
        '''function to determine if specific dots exceed the bounds of our aperture.
        Returns indexes of dots that are in excess.
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
        # with this function we update noise dot locations randomly 
        ''' Note to self: in the final implementation including the BM 
        algorithm we need to distinguish here with updates of random speed
        and random direction for the MN algorithm and only random direction
        for the MN algorithm '''
        if axis == 0: #name axis in case aperture isn't square or center is elsewhere
            ax = 0
        elif axis == 1:
            ax = 1
        rand_loc = (np.random.rand(x)-.5)*self.fieldsize[ax] + self.center[ax]
        return rand_loc
    
    def get_coherent_dots(self, frame):
        """ Function that randomly selects coherently moving dots for either one or 
        two randomly moving dot populations"""
        if type(self.coherence) is float:
            num_coh = int(self.coherence*int(self.n_dot//3)) # number of coherently moving dots (per group)
            
            # indexes of coherently moving dots
            coh_ind = np.random.choice(range(int(self.n_dot//3)), num_coh, replace = False)
            return coh_ind
        elif len(self.coherence) == 2:
            num_coh = np.dot(self.coherence,int(self.n_dot//6)) # number of coherently moving dots (per group)
            
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
        self.rgbs = color
        self.coherence = coherence[0]
        if direction == 'left': # convert direction in degree
            self.direct = 270
        elif direction == 'right':  # convert direction in degree
            self.direct = 90
            
    def bm_random_loc(self, start_x, start_y):
        rdm_theta = np.random.rand(len(start_x)) *2*np.pi # random angle on a circle
        new_x = start_x + self.speed*np.cos(rdm_theta)/self.frameRate # "speed" is treated as the radius
        new_y = start_y + self.speed*np.sin(rdm_theta)/self.frameRate
        new_coord = np.column_stack((new_x, new_y))
        return new_coord
        
        

#%%


# """
# Add the dot functionality in degrees. I need to write this out properly since
# I had not done this before. I used the material by Geoffrey Boynton:
# http://www.mbfys.ru.nl/~robvdw/DGCN22/PRACTICUM_2011/LABS_2011/ALTERNATIVE_LABS/Lesson_2.html
# and again Arkady Zgonnikov's implementation (link in the class above) to derive
# at my own version.
# """
# class params_RDMK_display():
#     def __init__(self, nDots = 10, color = np.array([255,255,255]), size = 10,
#                  center = np.array([0,0]),  apertureSize = np.array([12,12]), frameRate = 61):
#         self.nDots = nDots
#         self.dim = 200
#         self.color = color
#         self.size = size # size of dots (pixels)
#         self.center = center # center of the field of dots (x,y)
#         self.apertureSize = apertureSize # size of rectangular aperture [w,h] in degrees.
#         self.speed = 3       # degrees/second
#         self.duration = 5    # seconds
#         self.direction = 45  # degrees (clockwise from straight up)
#         self.frameRate = frameRate
             
        
#     def inital_pos(self):
#         np.random.rand(self.nDots)-.5
#         self.x = (np.random.rand(self.nDots)-.5)*self.apertureSize[0] + self.center[0]
#         self.y = (np.random.rand(self.nDots)-.5)*self.apertureSize[1] + self.center[1]
        
#         self.displacement_x = self.speed*np.sin(self.direction*np.pi/180)/self.frameRate
#         self.displacement_y = -self.speed*np.cos(self.direction*np.pi/180)/self.frameRate
#         return self.displacement_x, self.displacement_y
#     # def dot_outside(self):
#         # we create a mask via equation of an ellipse to determine which dots fall inside
#         # goodDots = np.square((params.x - params.center[0]))/np.square((params.apertureSize[0]/2)) + 
#         # np.square((params.y - params.center[1]))/np.square((params.apertureSize[1]/2))
#     def randomize_coord(self, x):
#         # with this function we update noise dot locations randomly 
#         ''' Note to self: in the final implementation including the BM 
#         algorithm we need to distinguish here with updates of random speed
#         and random direction for the MN algorithm and only random direction
#         for the MN algorithm '''
#         rand_loc2 = (np.random.rand(x)-.5)*self.apertureSize[0] + self.center[0]
#         rand_loc = np.random.randint(-self.dim, self.dim, x)
#         return rand_loc2
         
    
# params = params_RDMK_display() 
# x, y = params.inital_pos()

# bounds = 0.5*self.apertureSize[0] + self.center[0]


# a = np.random.randint(0, 20, 20).reshape((10,2))          
# redraw =  (a > 15) | (a < 5) | (a > 15) | (a < 5)

# a[redraw] = np.random.randint(5, 15, np.sum(redraw))

# speed = 3
# direction = 60
# frameRate = 61
# displacement_x = speed*np.sin(direction*np.pi/180)/frameRate
# displacement_y = speed*np.cos(direction*np.pi/180)/frameRate


# params.x
# goodDots = np.square((params.x - params.center[0]))/np.square((params.apertureSize[0]/2)) + np.square((params.y - params.center[1]))/np.square((params.apertureSize[1]/2))
    
# np.square([10, 5])

# print(x)
# #%%
# """
# Playground
# """
# lis.iloc[1,].Colors[0]
# lis.iloc[1,].Coherence[0]
# lis.iloc[1,].Direction

# x = RDM_kinematogram()

# color1, pos = x.create_dots()

# item_list = x.ind
# ind = item_list
# ## PARAMETER

# frameRate = 61
# n_dot = 60
# coherence = [0.5,0.5]
# groups = 2
# frame = 1
# rgbs = [[ -1,0,1],[ 1,0,1]]
# speed = 6
# center = [0,0]
# fieldsize = [14.8, 14.8]
# bounds_x = 0.5*fieldsize[0] + center[0] # determine aperature bounds on the x axis
# bounds_y = 0.5*fieldsize[1] + center[1] # determine aperature bounds on the y axis
# t_group = 1
# direct = 270
# alg = 'MN'
# ## FUCTIONS


# def randomize_coord(x, axis):
#         # with this function we update noise dot locations randomly 
#         ''' Note to self: in the final implementation including the BM 
#         algorithm we need to distinguish here with updates of random speed
#         and random direction for the MN algorithm and only random direction
#         for the MN algorithm '''
#         if axis == 0: #name axis in case aperture isn't square or center is elsewhere
#             ax = 0
#         elif axis == 1:
#             ax = 1
#         rand_loc = (np.random.rand(x)-.5)*fieldsize[ax] + center[ax]
#         return rand_loc

# def exceed_bounds(coord):
#         '''function to determine if specific dots exceed the bounds of our aperture.
#         Returns indexes of dots that are in excess.
#         '''
#         if np.any((coord[:,0] < -bounds_x) | (coord[:,0] > bounds_x) 
#                   | (coord[:,1] < -bounds_y) | (coord[:,1] > bounds_y), axis=0):
#             # find row indices where bounds are exceeded for X coordinates
#             redraw = np.nonzero((coord[:,0] > bounds_x) | (coord[:,0] < -bounds_x))
#             # find row indices where bounds are exceeded for Y coordinates
#             redraw = np.hstack((redraw,  np.nonzero((coord[:,1] > bounds_y) | (coord[:,1] < -bounds_y))))
#             # find unique row indices where bounds are exceeded 
#             redraw = np.unique(redraw)
#         else:
#             redraw = False
#         return redraw

# def create_dots():
#         ''' Outputs a matrix that contains information of each dot by column: 
#         indices, population-membership, one column for each respective RGB value 
#         and x,y coordinates of each dot'''
#         # first we create three sequences by creating a three dimensional array
#         ind = np.arange(0,n_dot,1)
#         # add a grouping variable and color codes
#         if groups == 2:
#             # add group
#             ind =  np.column_stack((ind, repmat(np.array([1,2]), 1, int(n_dot/2)).T))
#             # add rgb color codes
#             ind =  np.column_stack((ind, repmat(rgbs, int(n_dot/2), 1)))
#         else:
#             # add group
#             ind =  np.column_stack((ind, repmat(np.array([1]), 1, n_dot).T))
#             # add rgb color codes
#             ind =  np.column_stack((ind, repmat(np.array(rgbs), n_dot, 1)))
#         # Then we set the coordinates for all dots (one array x, the other y)
#         dot_cart = np.array([randomize_coord(n_dot, 0), 
#                       randomize_coord(n_dot, 1)]).T
#         ## add the random coordinates to our matrix
#         ind =  np.column_stack((ind, dot_cart))
#         # create three sequences by creating a three dimensional array. In only do 
#         # bthis because it helps me to visualize and keep track of the different 
#         # frame populations. A two dimensional frame would do fine as well.
#         ind = np.vsplit(ind, 3)
#         # noticed the input format for psychopy are lists are pairwise lists
#         colors = ind[0][:,range(2,5)]
#         pos = ind[0][:,range(5,7)]
#         return colors.tolist(), pos.tolist() 

# def get_coherent_dots(frame):
#         """ Function that randomly selects coherently moving dots for either one or 
#         two randomly moving dot populations"""
#         if type(coherence) is float:
#             num_coh = int(coherence*int(n_dot//3)) # number of coherently moving dots (per group)
           
#             # indexes of coherently moving dots
#             coh_ind = np.random.choice(range(int(n_dot//3)), num_coh, replace = False)
#             return coh_ind
#         elif len(coherence) == 2:
#             num_coh = np.dot(coherence,int(n_dot//6)) # number of coherently moving dots (per group)
           
#             # Get the indices for both Dot pops
#             Bol_pop1 = ind[frame%3][:,1]==1
#             Pop_1 = np.where(Bol_pop1)[0]
#             Pop_2 = np.where(~Bol_pop1)[0]
           
#             # indexes of coherently moving dots
#             coh_ind = np.random.choice(Pop_1, int(num_coh[0]), replace = False)
#             coh_ind = np.concatenate((coh_ind, np.random.choice(Pop_2, int(num_coh[1]), replace = False)))
#             return coh_ind
#         else:
#             raise ValueError('Please provide one or two coherence Values')
   

# def update_dots(frame):

#         """ Function to update the dot positions - randomly selecting dots of the 
#         target group to move coherently and the rest to reapear in random positions"""
        
#         #calculate dot displacement in degree of viusal angle
#         displacement_x = speed*np.sin(direct*np.pi/180)/frameRate
#         displacement_y = speed*np.cos(direct*np.pi/180)/frameRate
        
#         #get indices of coherently moving dots
#         coh_ind = get_coherent_dots(frame)
        
#         # update the relevant indexes for coherent dots; self.direct negative 
#         # for leftward motion
#         ind[frame%3][coh_ind,5] +=  displacement_x
#         ind[frame%3][coh_ind,6] +=  displacement_y
        
#           # find the noise dots 
#         noise = np.ones(n_dot//3, dtype=bool)
#         noise[coh_ind] = False
        
#         #update the noise dots dependent on algorithm choice
#         if alg == 'MN':
#             # randomize x and y coordinates for the noise dots
#             ind[frame%3][noise,5:7] = np.array([randomize_coord(np.count_nonzero(noise), 0),
#                         randomize_coord(np.count_nonzero(noise), 1)]).T
#         elif alg == 'BM':
#             ind[frame%3][noise,5:7] = bm_random_loc(ind[frame%3][noise,5], ind[frame%3][noise,6])
            
#         # if any dot exceeds the limit of our circle, randomly redraw it
#         # took this strategy from Arkady Zgonnikov's implementation:
#         # "https://github.com/cherepaha/Gamble_RDK/blob/master/ui/rdk_mn.py"
#         redraw = exceed_bounds(ind[frame%3][:,5:7])
#         #if we find any coordinates in excess redraw them
#         if redraw is not False:
#             ind[frame%3][redraw,5:7] = np.array([randomize_coord(redraw.size, 0),
#                     randomize_coord(redraw.size, 1)]).T
#         # update the noise dots 
#         noise = np.ones(n_dot//3, dtype=bool)
#         noise[coh_ind] = False
#         # randomize x and y coordinates for the noise dots
#         ind[frame%3][noise,5:7] = np.array([randomize_coord(np.count_nonzero(noise), 0),
#                     randomize_coord(np.count_nonzero(noise), 1)]).T
#         # because I believe that the dots are drawn in a serial manner i shuffle all
#         # the order to be on the safe side. Otherwise if two 
#         # randomly occupy the same position one superimposes the other. Not shuffling 
#         # might lead to one group of dots superimposing the other more often than the
#         # other - just because of the order that I created the groups here. Probably 
#         # I am overthinking, but it cannot hurt.
#         np.random.shuffle(ind[frame%3])
#         #noticed the input format for psychopy are lists are pairwise lists
#         colors = ind[frame%3][:,2:5]
#         pos = ind[frame%3][:,5:7]
#         return  colors.tolist(), pos.tolist()


# def bm_random_loc(start_x, start_y):
#         rdm_theta = np.random.rand(len(start_x)) *2*np.pi # random angle on a circle
#         new_x = start_x + speed*np.cos(rdm_theta)/frameRate # "speed" is treated as the radius
#         new_y = start_y + speed*np.sin(rdm_theta)/frameRate
#         new_coord = np.column_stack((new_x, new_y))
#         return new_coord


# update_dots(2)

# ind = create_dots()

# #%%
# """
# Slow Version
# """

# # Define Experimental parameter
# frames = 60
# direction = "left"
# n_dots = 200
# trgt_size = 30
# dot_xys = []
# coh_dot = random.sample(range(n_dots),  trgt_size) 
# dot_speed = 5
# print(coh_dot)
# a = 0

      
# for frame in range(frames):
#     for dot in range(n_dots):
#         if frame == 0: # randomly assign initial position
#             dot_x = random.uniform(-200,200)
#             dot_y = random.uniform(-200,200)
#             dot_xys.append([dot_x,dot_y])
#         else:
#             if coh_dot.count(dot) == 1: # determine if dot is in target group via count function
#                 if dot_xys[dot][0] + dot_speed < 200: # if the dot is still within the window
#                     dot_xys[dot][0] = dot_xys[dot][0] + dot_speed
#                     dot_xys[dot][1] = dot_xys[dot][1] + random.randint(-dot_speed, dot_speed)
#                 else: # if the dot would move beyond
#                     dot_xys[dot][0] = dot_xys[dot][0] + dot_speed - 400
#                     dot_xys[dot][1] = dot_xys[dot][1] + random.randint(-dot_speed, dot_speed)
#             else: # update the remaining dots
#                 dot_xys[dot][0] = dot_xys[dot][0] + random.randint(-dot_speed, dot_speed)
#                 dot_xys[dot][1] = dot_xys[dot][1] + random.randint(-dot_speed, dot_speed)
#                 if dot_xys[dot][0] > 200:
#                     dot_xys[dot][0] = dot_xys[dot][0] - 400
#                 elif dot_xys[dot][0] < -200:
#                     dot_xys[dot][0] = dot_xys[dot][0] + 400
#                 elif dot_xys[dot][1] > 200:
#                     dot_xys[dot][1] = dot_xys[dot][1] - 400
#                 elif dot_xys[dot][1] < -200:
#                     dot_xys[dot][1] = dot_xys[dot][1] + 400
#                 else:
#                     pass
#     print(dot_xys[17][0])
                
# import numpy as np            
# fieldsize = 14.8 # fixed for now because this way I can get an ideal number of dots (60)
# frameRate = 61              
# np.ceil(16.7*np.square(fieldsize)/frameRate)
                