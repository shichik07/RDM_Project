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

from psychopy import core, visual, gui, data, event, monitors
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
    
    def update_dots(self, frame, direction, coherence):

        """ Function to update the dot positions - randomly selecting dots of the 
        target group to move coherently and the rest to reapear in random positions"""
        
        if direction == 'left': # convert direction in degree
            direct = 270
        elif direction == 'right':  # convert direction in degree
            direct = 90
            
        #calculate dot displacement in degree of viusal angle
        displacement_x = self.speed*np.sin(direct*np.pi/180)/self.frameRate
        displacement_y = self.speed*np.cos(direct*np.pi/180)/self.frameRate
        
        #get indices of coherently moving dots
        coh_ind = self.get_coherent_dots(frame, coherence)
        
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
    
    def get_coherent_dots(self, frame, coherence):
        """ Function that randomly selects coherently moving dots for either one or 
        two randomly moving dot populations"""
        if type(coherence) is float:
            num_coh = int(coherence*int(self.n_dot//3)) # number of coherently moving dots (per group)
            
            # indexes of coherently moving dots
            coh_ind = np.random.choice(range(int(self.n_dot//3)), num_coh, replace = False)
            return coh_ind
        elif len(coherence) == 2:
            num_coh = np.dot(coherence,int(self.n_dot//6)) # number of coherently moving dots (per group)
            
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

#%% Instructions

# Set Monitor

my_monitor = monitors.Monitor(name='DellXPS15_screen')
my_monitor.setSizePix((1366, 768))
my_monitor.setWidth(31)
my_monitor.setDistance(60)
my_monitor.saveMon()


win = visual.Window(size = [1920,1080],
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
txt_3 = u'Your task will be to decide whether these dots are moving to either the left or right, by clicking the left and right arrows.'
txt_4 = u'Please be as clock.reset()
        event.getKeys(timeStamped=clock)
        event.clearEvents() acruate and fast as possible.'
#%% Set Dot Presentation Parameter


refresh_rate = 60
coherence = [0.3, 0.5]
RGBS = [[ -1,0,1],[ 1,0,1]]
frames = 1600
n_dots = 60
trgt_size = 20  # size of the group of coherently moving dots
dot_xys = []
dot_speed= 6
dot_size = 0.3
direction = 'left'
RESPONSE_KEYS = ['left', 'right']
CONTINUE_KEYS = ['return', 'space']
QUIT_KEY = ['escape']

field_size = 5.0

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

# Instruction presentation
def instruction_show(text):
    ''' Show instruction and wait for a response
    Source: Tutorial Lindelov'''
    Instruction.text = text
    Instruction.draw()
    win.flip()
    key = event.waitKeys()
    # if key == 'escape':
    #     win.close()
    #     core.quit()
    return key

def block_loop(trials, block_nr):
    for trial in trials:
        #PRESENT FIXATION
        # Interstimulus interval in frames?
        ISI_time = round(random.uniform(1,1.4),2) 
        fixation.draw()
        win.flip()
        ISI = StaticPeriod(screenHz=refresh_rate)
        ISI.start(ISI_time)  # start a period of 0.5s
        ''' Here we could load a cue '''
        # update the color variable parameter
        DOT_UPDATE.rgbs = RGBS
        # create a fresh instance for the dots
        color, coord= DOT_UPDATE.create_dots()
        # update the color variable parameter
        DOT_UPDATE.rgbs = RGBS
        #stim.image = 'largeFile.bmp'  # could take some time
        ISI.complete()  # finish theevent.clearEvents()
        #PRESENT CUE
        
        #PRESENT FIXATION
       
        win = visual.Window(size = [1920,1080],
            monitor = "DellXPS15_screen",
            units="deg",
            fullscr=False, # change to fullscreen later
            color=[0,0,0]
        )
        
                
        #RESET CLOCK and clear events
        clock.reset()
        
        event.clearEvents()
        
        #PRESENT STIM
        for frame in range(frames):
           dot_stim.colors, dot_stim.xys = DOT_UPD.update_dots(frame, direction, coherence)
           dot_stim.draw()
           win.flip()
           keys = event.getKeys(RESPONSE_KEYS,timeStamped=clock)
           if event.getKeys(QUIT_KEY):
               win.close()
               core.quit()
           elif len(keys)>0:
               print(keys)
               break
                
    


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

save_path =  '/home/jules/Dropbox/PhD_Thesis/DecisionMakingAndLearningStudy/Experiment/Development' 
data_dir = os.path.abspath(save_path + '/data/') # just in case the absolute path is required

if not os.path.exists(data_dir):
   os.makedirs(data_dir)

# make a text file to save data
data_file  = data_dir + '/RDM_PD' + ID  + '_time_' + DATE + '.csv'
cnt = 0
#
#Make sure we do not overwrite our data
while os.path.exists(data_file):
    cnt += 1
    data_file = data_dir + '/RDM_PD' + expInfo['Participant_nr'] + expInfo['dateStr'] + '_v' + str(cnt) + '.csv'


# Create a dictionary with the trial Infos
trial_dict = {'Trial_nr': None , 
              'Condition':None, 
              'Gender': None,
              'Correct': None,
              'Coherence': None,
              'Response': None,
              'Group': None,
              'Direction': None,
              'Age': None,
              'Block': None,
              'RT': None,
              'Colors': None,
              'ISI': None,
              'Early_resp': None}



# Get the Fieldnames
fnames = list(trial_dict.keys()) 

dataFile = open(fileName, 'w')  # a simple text file with 'comma-separated-values'
writer = csv.DictWriter(dataFile, fieldnames = fnames)
writer.writeheader()



writer.writerow(trial_dict)

dataFile.close()
