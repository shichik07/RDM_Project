# -*- coding: utf-8 -*-
"""
Created on Tue March  5 11:20:31 2021

@author: Julius Kricheldorff
@instituition: University of Oldenburg

For this Experiment I borrowed from the tutorial by Jonas K. Lindelov
('https://lindeloev.net/psychopy-course/past-courses/cml-seminar-2018/')
and  Arkady Zgonnikov's implementation of a random dot kinematogram:
"https://github.com/cherepaha/Gamble_RDK/blob/master/ui/rdk_mn.py". The trial 
randomization structure is inspired by... 


"""

from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import random, os
import numpy as np
from numpy.matlib import repmat
import csv




#%% RDM Module for the time being


class RDM_kinematogram(object):
    """ Functions to implement a random dot kinematogram in Psychopy. Two 
    algorithms are implemented. The Movshon-Newsome algorithm and the Brownian-Motion
    algorithm for randomly moving dots with different coherence levels. For a 
    more thorough overview of advantages and disadvantages see Pilly and Seitz
    2009"""
    def __init__(self, alg='MN', dot_speed = 5, coherence = 0.2, 
                 direction = 'left', dot_density = 0.167, num_dot = 180, 
                 radius = 200, groups = 2, t_group = 1, rgbs = [[ 0,1,0],[1,0,0]]):
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
        if groups == 2:
            if num_dot%6 == 0:
                self.n_dot = num_dot # number of dots
                self.num_coh = int(coherence*(num_dot/6)) # number of coherently moving dots (per group)
                self.t_group = t_group # target group either one or two
            else:
                raise ValueError('Because you want to display two distinct dot_populations'
                                 ' with three distinct presentation sequences, the total'
                                 ' number of dots must be divisible by 6.')
        elif groups == 1:
            if num_dot%3 == 0:
                self.n_dot = num_dot # number of dots
                self.num_coh = int(coherence*(num_dot/6)) # number of coherently moving dots
                self.t_group = 1 
            else:
                raise ValueError('Because you want to display one dot_population'
                                 ' with three distinct presentation sequences, the total'
                                 ' number of dots must be divisible by 3.')
        else:
             raise ValueError('You must specify the groups parameter to the number of'
                              ' dot populations that you would like to display.' 
                              ' At present either one or teo dot populations can be ' 
                              'displayed.')    
        self.speed = dot_speed # dot displacement
        self.n_dot = num_dot # number of dots
        self.num_coh = int(coherence*(num_dot/6)) #  coherently moving dots each frame
        self.dim = radius # display dimensions
        self.groups = groups # number of dot groups
        self.rgbs = rgbs # colors used 
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
        dot_cart = np.array([self.randomize_coord(self.n_dot), 
                      self.randomize_coord(self.n_dot)]).T
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
        # All indexes in this frame
        group_ind = np.where(self.ind[frame%3][:,1]==self.t_group)
        # indexes of coherently moving dots
        coh_ind = np.random.choice(group_ind[0], self.num_coh, replace = False)
        # update the relevant indexes for coherent dots; self.direct negative 
        # for leftward motion
        self.ind[frame%3][coh_ind,5] +=  self.speed*self.direct
        # if any dot exceeds the limit of our circle, randomly redraw it
        # took this strategy from Arkady Zgonnikov's implementation:
        # "https://github.com/cherepaha/Gamble_RDK/blob/master/ui/rdk_mn.py"
        if any(np.abs(self.ind[frame%3][coh_ind,5]) > self.dim):
            # find the relevant items outside 
            redraw = np.abs(self.ind[frame%3][coh_ind,5]) > self.dim
            redraw = coh_ind[redraw]
            # randomize x and y coordinates for the abarrant coherent dots
            self.ind[frame%3][redraw,5:7] = np.array([self.randomize_coord(redraw.size),
                    self.randomize_coord(redraw.size)]).T
        # update the noise dots and if exist the redraw coordinates
        noise = np.ones(self.n_dot//3, dtype=bool)
        noise[coh_ind] = False
        # randomize x and y coordinates for the noise dots
        self.ind[frame%3][noise,5:7] = np.array([self.randomize_coord(np.count_nonzero(noise)),
                    self.randomize_coord(np.count_nonzero(noise))]).T
        # because I believe that the dots are drawn in a serial manner i shuffle all
        # the order to be on the safe side. Otherwise if two 
        # randomly occupy the same position one superimposes the other. Not shuffling 
        # might lead to one group of dots superimposing the other more often than the
        # other - just because of the order that I created the groups here. Probably 
        # I am overthinking, but it cannot hurt.
        np.random.shuffle(self.ind[frame%3])
        # noticed the input format for psychopy are lists are pairwise lists
        colors = self.ind[frame%3][:,2:5]
        pos = self.ind[frame%3][:,5:7]
        return  colors.tolist(), pos.tolist()
        
    def randomize_coord(self, x):
        # with this function we update noise dot locations randomly 
        ''' Note to self: in the final implementation including the BM 
        algorithm we need to distinguish here with updates of random speed
        and random direction for the MN algorithm and only random direction
        for the MN algorithm '''
        rand_loc = np.random.randint(-self.dim, self.dim, x)
        return rand_loc

#%% Instructions
win = visual.Window(
    size=[400,400],
    units="pix",
    fullscr=False, # change to fullscreen later
    color=[0,0,0]
)

Instruction = visual.TextStim(win=win, color=[1,1,1])
    


txt_1 = 'Welcome to the Experiment'
txt_2 = u'In this task you will be presented with a set of seemingly random moving dots.'
txt_3 = u'Your task will be to decide whether these dots are moving to either the left or right, by clicking the left and right arrows.'
txt_4 = u'Please be as acruate and fast as possible.'
#%% Set Dot Presentation Parameter
dot_parameter = RDM_kinematogram()
color, coord= dot_parameter.create_dots()

frames = 16000
n_dots = 180
trgt_size = 20  # size of the group of coherently moving dots
dot_xys = []
dot_speed= 6
dot_size = 10

field_size = 5.0

# to keep track of time
clock = core.Clock()

# Instruction presentation
def instruction_show(text):
    ''' SHow instruction and wait for a response
    Source: Tutorial Lindelov'''
    Instruction.text = text
    Instruction.draw()
    win.flip()
    key = event.waitKeys()
    # if key == 'escape':
    #     win.close()
    #     core.quit()
    return key

# create the dot stimuli
dot_stim = visual.ElementArrayStim(
    win=win,
    units="pix",
    nElements=60,
    elementTex=None,
    elementMask="circle",
    xys=coord[0:60],
    sizes=dot_size,
    fieldSize = field_size,
    fieldShape='circle',
    colors=color
)
#%% Experimental loop

# Prepare Input by User/Experimenter
expInfo = {'ProbandenNr':'', 'Geschlecht':['männlich','weiblich','divers'],
            'Alter': '' , 'Händikeit': ['Links', 'Rechts'], 'Gruppe (für Experimentatorin)': ['PD', 'HC']}
expInfo['dateStr'] = data.getDateStr()  # add the current time

# Updates DIALOGUE with dialogue response
inp  = gui.DlgFromDict(expInfo, title='Random Dot Motion Task',fixed=['dateStr'])
ID   = inp.data[4]
DATE = inp.data[5]

instruction_show('wot')
instruction_show(txt_2)
instruction_show(txt_3)
instruction_show(txt_4)

## Initialize data saving

save_path =  '/home/jules/Dropbox/PhD_Thesis/DecisionMakingAndLearningStudy/Experiment/Development' + '/data/'
data_dir = os.path.abspath(save_path) # just in case the absolute path is required

if not os.path.exists(data_dir):
   os.makedirs(data_dir)

# make a text file to save data
data_file  = data_dir + 'RDM_PD' + ID  + '_time_' + DATE + '.csv'
cnt = 0
#
#Make sure we do not overwrite our data
while os.path.exists(data_file):
    cnt += 1
    data_file = data_dir + 'RDM_PD' + expInfo['Participant_nr'] + expInfo['dateStr'] + '_v' + str(cnt) + '.csv'


data = open(data_file, 'w')  # a simple text file with 'comma-separated-values'
data.write(['condition', 'gender' ,'age', 'correct', 'block', 'condition', 
               'trial_nr', 'coherence', 'response', 'direction' ])



with  open(data_file, 'w')  as csv_file:  
    writer = csv.writer(csv_file)
    for key, value in mydict.items():
       writer.writerow([key, value])
#
#dataFile = open(fileName, 'w')  # a simple text file with 'comma-separated-values'
#dataFile.write('condition,gender,age, correct\n', 'block', 'condition',
#                'trial_nr', 'coherence', 'response', 'direction' )
#






frame = 0
clock.reset()

#Present Instructions
text_1.draw()
win.flip()

event.getKeys(timeStamped=clock)

event.clearEvents()

for frame in range(frames):
    dot_stim.colors, dot_stim.xys = dot_parameter.update_dots(frame)
    dot_stim.draw()
    win.flip()
    if event.getKeys(['escape']):
        core.quit()
    elif event.getKeys(['left']):
        print(event.getKeys())
        win.close()

print(clock.getTime()) 
win.close()