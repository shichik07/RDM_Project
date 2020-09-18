"""measure your JND in orientation using a staircase method"""
from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import random, os
import numpy as np
from numpy.matlib import repmat


#
#try:  # try to get a previous parameters file
#    expInfo = fromFile('lastParams.pickle')
#except:  # if not there then use a default set
#    expInfo = {'Participant_nr':'0', 'gender':['male','female','non-binary'],
#            'Age':0, 'Handedness': ['left', 'right'], 'group': ['PD', 'HC']}
#expInfo['dateStr'] = data.getDateStr()  # add the current time
#
#
# present a dialogue to change params
#dlg = gui.DlgFromDict(expInfo, title='Random Dot Motions Task',
#                    fixed=['dateStr'])
#
#if dlg.OK:
#    toFile('lastParams.pickle', expInfo)  # save params to file for next time
#else:
#    core.quit()  # the user hit cancel so exit
#
#
# Check data dir Note: Hardcoded version here, for the upload to Github and export to other PCs this 
# needs to eb more automated
#
#experiment_path = "C:\\Users\juliu\OneDrive\Dokumente\PhD-Thesis\Decision_making and Learning Study\Experiment\Test data RDM task" + "\\data\\" 
#data_dir = os.path.abspath(experiment_path) # just in case the absolute path is required
#
#if not os.path.exists(data_dir):
#    os.makedirs(data_dir)
#
#
# make a text file to save data
#fileName = data_dir + 'RDM_PD' + expInfo['Participant_nr'] + expInfo['dateStr'] + '.csv'
#cnt = 0
#
# Make sure we do not overwrite our data
#while os.path.exists(data_file):
#    cnt += 1
#    data_file = data_dir + 'RDM_PD' + expInfo['Participant_nr'] + expInfo['dateStr'] +
#            '_v' + str(cnt) + '.csv'
#
#
#dataFile = open(fileName, 'w')  # a simple text file with 'comma-separated-values'
#dataFile.write('condition,gender,age, correct\n', 'block', 'condition',
#                'trial_nr', 'coherence', 'response', 'direction' )
#
# create the staircase handler
#staircase = data.StairHandler(startVal = 20.0,
#                          stepType = 'db', stepSizes=[8,4,4,2],
#                          nUp=1, nDown=3,  # will home in on the 80% threshold
#                          nTrials=1)




class RDM_kinematogram(object):
    """ Functions to implement a random dot kinematogram in Psychopy. Two 
    algorithms are implemented. The Movshon-Newsome algorithm and the Brownian-Motion
    algorithm for randomly moving dots with different coherence levels. For a 
    more thorough overview of advantages and disadvantages see Pilly and Seitz
    2009"""
    def __init__(self, alg='MN', dot_speed = 5, coherence = 0.4, 
                 direction = 'left', dot_density = 0.167, num_dot = 180, 
                 radius = 200, groups = 2, t_group = 1, rgbs = [[ -1,0,1],[ 1,0,1]]):
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

win = visual.Window(
    size=[400,400],
    units="pix",
    fullscr=True, # change to fullscreen later
    color=[0,0,0]
)

text_1 = visual.TextStim(win=win, 
    text=("Welcome to this experiment!"),
    color=[-1,-1,-1],
    flipHoriz=False #if you ever need mirrored writing set this True
)

text_2 = visual.TextStim(win=win, 
    text=("In this task you will be presented with a set of seemingly random moving dots."),
    color=[-1,-1,-1],
    flipHoriz=False #if you ever need mirrored writing set this True
)

text_3 = visual.TextStim(win=win, 
    text=("Your task will be to decide whether these dots are moving to either the left or right, by clicking the left and right arrows."),
    color=[-1,-1,-1],
    flipHoriz=False #if you ever need mirrored writing set this True
)

text_4 = visual.TextStim(win=win, 
    text=("Please be as acruate and fast as possible."),
    color=[-1,-1,-1],
    flipHoriz=False #if you ever need mirrored writing set this True
)


#
dot_parameter = RDM_kinematogram()
color, coord= dot_parameter.create_dots()

frames = 590
n_dots = 180
trgt_size = 40 # size of the group of coherently moving dots
dot_xys = []
dot_speed= 5
dot_size = 10

field_size = 5.0


# to keep track of time
clock = core.Clock()

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




clock.reset()

for frame in range(frames):
    dot_stim.colors, dot_stim.xys = dot_parameter.update_dots(frame)
    dot_stim.draw()
    win.flip()

#dot_xys = []
#for frame in range(frames):
#    
#    for dot in range(n_dots):
#        if frame == 0: # randomly assign initial position
#            dot_x = random.uniform(-200,200)
#            dot_y = random.uniform(-200,200)
#            dot_xys.append([dot_x,dot_y])
#
#        else:
#            if coh_dot.count(dot) == 1: # determine if dot is in target group via count function
#                if dot_xys[dot][0] + dot_speed < 200: # if the dot is still within the window
#                    dot_xys[dot][0] = dot_xys[dot][0] + dot_speed
#                    dot_xys[dot][1] = dot_xys[dot][1] + random.randint(-dot_speed, dot_speed)
#                else: # if the dot would move beyond
#                    dot_xys[dot][0] = dot_xys[dot][0] + dot_speed - 400
#                    dot_xys[dot][1] = dot_xys[dot][1] + random.randint(-dot_speed, dot_speed)
#            else: # update the remaining dots
#                dot_xys[dot][0] = dot_xys[dot][0] + random.randint(-dot_speed, dot_speed)
#                dot_xys[dot][1] = dot_xys[dot][1] + random.randint(-dot_speed, dot_speed)
#                if dot_xys[dot][0] > 200:
#                    dot_xys[dot][0] = dot_xys[dot][0] - 400
#                elif dot_xys[dot][0] < -200:
#                    dot_xys[dot][0] = dot_xys[dot][0] + 400
#                elif dot_xys[dot][1] > 200:
#                    dot_xys[dot][1] = dot_xys[dot][1] - 400
#                elif dot_xys[dot][1] < -200:
#                    dot_xys[dot][1] = dot_xys[dot][1] + 400
#                else:
#                    pass
#    dot_stim.xys = dot_xys
#    dot_stim.draw()
#    win.flip()


print(clock.getTime()) 


win.close()



#
#feedback1.draw()
#fixation.draw()
#win.flip()
#event.waitKeys()  # wait for participant to respond
#
#win.close()
#core.quit()