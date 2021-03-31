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

from psychopy import core, visual, gui, event, data, monitors
from psychopy.tools.filetools import fromFile, toFile
import random, os
import numpy as np
from numpy.matlib import repmat
import csv


#%% RDM Module for the time being

class RDM_kinematogram(object):
    """ Functions to implement a random dot kinematogram in Psychopy using the 
    elementarray function. Two algorithms are implemented. The Movshon-Newsome 
    algorithm and the Brownian-Motion algorithm for randomly moving dots with 
    different coherence levels. For a more thorough overview of advantages and 
    disadvantages see Pilly and Seitz 2009"""
    def __init__(self, 
                 alg='MN', 
                 dot_speed = 6,  
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
        
        #calculate dot displacement in degree of viusal angle
        displacement_x = self.speed*np.sin(self.direct*np.pi/180)/self.frameRate
        displacement_y = self.speed*np.cos(self.direct*np.pi/180)/self.frameRate
        
        #get indices of coherently moving dots
        coh_ind = self.get_coherent_dots(frame)
        
        # update the relevant indexes for coherent dots; self.direct negative 
        # for leftward motion
        self.ind[frame%3][coh_ind,5] +=  displacement_x
        self.ind[frame%3][coh_ind,6] +=  displacement_y
        
        # if any dot exceeds the limit of our circle, randomly redraw it
        # took this strategy from Arkady Zgonnikov's implementation:
        # "https://github.com/cherepaha/Gamble_RDK/blob/master/ui/rdk_mn.py"
        redraw = self.exceed_bounds(self.ind[frame%3][coh_ind,5:7])
        #if we find any coordinates in excess redraw them
        if redraw is not False:
            self.ind[frame%3][coh_ind[redraw],5:7] = np.array([self.randomize_coord(redraw.size, 0),
                    self.randomize_coord(redraw.size, 1)]).T
        # update the noise dots and if exist the redraw coordinates
        noise = np.ones(self.n_dot//3, dtype=bool)
        noise[coh_ind] = False
        # randomize x and y coordinates for the noise dots
        self.ind[frame%3][noise,5:7] = np.array([self.randomize_coord(np.count_nonzero(noise), 0),
                    self.randomize_coord(np.count_nonzero(noise), 1)]).T
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
        

#%% Instructions

# Set Monitor

my_monitor = monitors.Monitor(name='DellXPS15_screen')
my_monitor.setSizePix((1366, 768))
my_monitor.setWidth(31)
my_monitor.setDistance(60)
my_monitor.saveMon()


win = visual.Window(size = [400,400],#[1920,1080],
    monitor = "DellXPS15_screen",
    units="deg",
    fullscr=False, # change to fullscreen later
    color=[0,0,0]
)


#Instruction Window
Instruction = visual.TextStim(win=win, color=[1,1,1])

#Fixation cross
fixation = visual.TextStim(win, text='+')
    


txt_1 = 'Welcome to the Experiment'
txt_2 = u'In this task you will be presented with a set of seemingly random moving dots.'
txt_3 = u'Your task will be to decide whether t hese dots are moving to either the left or right, by clicking the left and right arrows.'
txt_4 = u'Please be as accurate and fast as possible.'
text_fin = u'You have finished the end of the Experiment. Thank you for your participation!'
#%% Set Dot Presentation Parameter


refresh_rate = 60
ISI_interval = [0.8,1.2]
coherence = [0.3, 0.5]
RGBS = [[ -1,0,1],[ 1,0,1]]
frames = 300
n_dots = 60
trgt_size = 20  # size of the group of coherently moving dots
dot_xys = []
dot_speed= 6
dot_size = 0.3
direction = 'left'
RESPONSE_KEYS = ['left', 'right']
CONTINUE_KEYS = ['return', 'space']
QUIT_KEY = ['escape']

CueFrames = round(0.4*refresh_rate)
exp_con = ['Mono', 'Di_null', 'Di_part', 'Di_full']
field_size = 5.0
Orientations =  [0.0,90.0] # of the informative cue stimuli

# to keep track of time
clock = core.Clock()





# create the dot updating class 
DOT_UPD = RDM_kinematogram()
color, coord= DOT_UPD.create_dots()

# create the dot stimuli 
dot_stim= visual.ElementArrayStim(
    win=win,
    units="deg",
    nElements=20,
    elementTex=None,
    elementMask="circle",
    xys=coord[0:20],
    sizes=dot_size,
    fieldSize = field_size,
    #fieldShape='circle',
    colors=color
)

# create the informative Cues
grating =visual.GratingStim(
    win=win,
    units="deg",
    size= [4,4],
    sf = (5.0/4.0),
    mask = "circle",
    contrast = 1
    )

# create the non-informative cue 
circle = visual.Circle(
    win=win,
    units="deg",
    radius= 2,
    fillColor=[1, 1, 1],
    lineColor=[0, 0, 0]
)


# Instruction presentation
def instruction_show(text):
    ''' Show instruction and wait for a response
    Source: Tutorial Lindelov'''
    Instruction.text = text
    Instruction.draw()
    win.flip()
    key = event.waitKeys()
    if key == 'escape':
         win.close()
         core.quit()
    return key

for trl_ind, trial_info in lis.iterrows():
    pass

def block_loop(trials):
    
    for trl_ind, trial_info in trials.iterrows():
        #PRESENT FIXATION
        # Interstimulus interval in frames?
        ISI_1 = round(random.uniform(ISI_interval[0], ISI_interval[1]),2) 
        ISI_2 = round(random.uniform(ISI_interval[0], ISI_interval[1]),2) #get another random interval
        
        fixation.draw()
        win.flip()
        ISI = core.StaticPeriod(screenHz=refresh_rate)
        ISI.start(ISI_2)  # start a period of 0.5s
        ''' Here we could load a cue '''
        # update the trial parameter
        DOT_UPD.update_params(direction = trial_info.Direction, 
                              color= trial_info.Colors, 
                              coherence = trial_info.Coherence)
        # Update Trial dictionary
        new_entries =  {'Trial_nr': trl_ind, 
              'Condition': trial_info.Condition, 
              'Coherence': trial_info.Coherence,
              'Direction':  trial_info.Direction,
              'Block': trial_info.Block,
              'Colors': trial_info.Colors,
              'ISI': [ISI_1, ISI_2],
              'Coherence_total': trial_info.Coherence_total,
              'Response': None,
              'Correct': 0, #default is incorrect
              'RT': None}
            

        
        # create a fresh instance for the dots
        color, coord= DOT_UPD.create_dots()
       
        #stim.image = 'largeFile.bmp'  # could take some time
        ISI.complete()  # finish theevent.clearEvents()
        
        #PRESENT CUE
        if trial_info.Condition == exp_con[0] or trial_info.Condition == exp_con[1]:
            for frame in range(CueFrames):
                circle.draw()
                win.flip()
        elif trial_info.Condition == exp_con[2]:
            grating.ori = Orientations[0]
            for frame in range(CueFrames):          
                grating.draw()
                win.flip()
        elif trial_info.Condition == exp_con[3]:
            grating.ori = Orientations[1]
            for frame in range(CueFrames):
                grating.draw()
                win.flip()
            
        
        #PRESENT FIXATION Number 2
        fixation.draw()
        win.flip()
        ISI = core.StaticPeriod(screenHz=refresh_rate)
        ISI.start(ISI_2)  # start a period of 0.5s
        ISI.complete()  # finish theevent.clearEvents()
        
        
        #PRESENT STIM
        for frame in range(frames):
            if frame == 0:
                clock.reset() # t0 for RT
                event.clearEvents() # reset events
                #send onset trigger
            dot_stim.colors, dot_stim.xys = DOT_UPD.update_dots(frame)
            dot_stim.draw()
            win.flip()
            keys = event.getKeys(timeStamped=clock)
            if keys != []:
                if keys[0][0] in QUIT_KEY:
                    wrt.finish()
                    win.close()
                    core.quit()
                elif keys[0][0] in RESPONSE_KEYS:
                    new_entries['Response'], new_entries['RT'] = keys[0]
                    break # break presentation loop early
            elif frame == frames and keys == []:
                new_entries['Response'] = 'No_resp'
                new_entries['RT'] = None
          
        #Write Trial Information 
        if new_entries['Response'] == new_entries['Direction']:
            new_entries['Correct'] = 1
        
        wrt.update(new_entries)    
    wrt.finish() # save intermediate results     
    
    


#%% Experimental loop


# Prepare Input by User/Experimenter
expInfo = {'ProbandenNr':'', 'Geschlecht':['männlich','weiblich','divers'],
            'Alter': '' , 'Händikeit': ['Links', 'Rechts'], 'Gruppe (für Experimentatorin)': ['PD', 'HC', 'PI']}
expInfo['dateStr'] = data.getDateStr()  # add the current time

# Updates DIALOGUE with dialogue response
inp  = gui.DlgFromDict(expInfo, title='Random Dot Motion Task',fixed=['dateStr'])
ID   = inp.data[4]
DATE = inp.data[5]

#LOAD TRIALS

#lis = ...



# Initialize data saving
save_path =  '/home/jules/Dropbox/PhD_Thesis/DecisionMakingAndLearningStudy/Experiment/Development' 
wrt = task_writer(save_path)

# Create Trial dictionary
BaseInf =  {'Gender': inp.data[1],
          'Group': inp.data[2],
          'Age': inp.data[0],
          'Handedness': inp.data[3],
          'Part_Nr': inp.data[4],
          'Date': inp.data[5]}


# Initialize file
wrt.set_file()
wrt.update(BaseInf)  
wrt.finish()

instruction_show('wot')
instruction_show(txt_2)
instruction_show(txt_3)
instruction_show(txt_4)

## Initialize data saving
wrt.start()


# start Block
blocks = lis.Block.unique()
for block in blocks:
    trials = lis.loc[lis.Block == block]
    block_loop(trials)
    
instruction_show(text_fin)
