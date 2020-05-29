"""measure your JND in orientation using a staircase method"""
from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import random, os
import numpy as np

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
        dot_cart = np.array([self.randomize_coord(self.n_dot), 
                      self.randomize_coord(self.n_dot)])
        return dot_cart
    
        
    def update_dots(self, dot_cart, frame):
        # indexes of coherently moving dots
        coh_ind = np.random.choice(self.ind[[frame%3],...].flat, 
                                   self.num_coh, replace = False)
        # update the relevant indexes for coherent dots; self.direct negative 
        # for leftward motion
        dot_cart[1,coh_ind] +=  self.speed*self.direct 
        # if any dot exceeds the limit of our circle, randomly redraw it
        # took this strategy from Arkady Zgonnikov's implementation:
        # "https://github.com/cherepaha/Gamble_RDK/blob/master/ui/rdk_mn.py"
        if any(np.abs(dot_cart[1,coh_ind]) > self.dim):
            # find the relevant items outside 
            redraw = np.abs(dot_cart[1,coh_ind]) > self.dim
            redraw = coh_ind[redraw]
            # randomize x and y coordinates for the abarrant coherent dots
            dot_cart[...,redraw] = np.array([self.randomize_coord(redraw.size),
                    self.randomize_coord(redraw.size)])
        # update the noise dots and if exist the redraw coordinates
        noise = np.isin(self.ind[[frame%3],...], coh_ind, invert=True)
        noise = self.ind[[frame%3],noise.flat]
         # randomize x and y coordinates for the noise dots
        dot_cart[...,noise] = np.array([self.randomize_coord(noise.size),
                    self.randomize_coord(noise.size)])
        return dot_cart
    
    
    def randomize_coord(self, x):
        # with this function we update noise dot locations randomly 
        ''' Note to self: in the final implementation including the BM 
        algorithm we need to distinguish here with updates of random speed
        and random direction for the MN algorithm and only random direction
        for the MN algorithm '''
        rand_loc = np.random.randint(-self.dim, self.dim, x)
        return rand_loc



dot_parameter = RDM_kinematogram(direction='right')
coordinates = dot_parameter.create_dots()



frames = 120
n_dots = 180
coherence = 0.4
dot_xys = []
dot_speed= 5
dot_size = 10


# create window and stimuli and text elements
win = visual.Window(
    size=[400,400],
    units="pix",
    fullscr=False, # change to fullscreen later
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

dot_stim = visual.ElementArrayStim(
    win=win,
    units="pix",
    nElements=n_dots,
    elementTex=None,
    elementMask="circle",
    xys=coordinates.list,
    sizes=dot_size
)
clock = core.Clock()
#clock.reset()

for frame in range(frames):
    coordinates = dot_parameter.create_dots()
    dot_stim.xys = coordinates.list
    dot_stim.draw()
    win.flip()


print(clock.getTime()) 



# index of random dots
#coh_dot = random.sample(range(n_dots),  trgt_size) 
#
# to keep track of time
#clock = core.Clock()
#
#for dot in range(n_dots):
#    dot_x = random.uniform(-200,200)
#    dot_y = random.uniform(-200,200)
#    dot_xys.append([dot_x,dot_y])
#
#
#dot_stim = visual.ElementArrayStim(
#    win=win,
#    units="pix",
#    nElements=n_dots,
#    elementTex=None,
#    elementMask="circle",
#    xys=dot_xys,
#    sizes=dot_size
#)
#
#clock.reset()
#
#dot_xys = []
#for frame in range(frames):
#    
#    for dot in range(n_dots):
#        if frame == 0: # randomly assign initial position
#            dot_x = random.uniform(-200,200)
#            dot_y = random.uniform(-200,200)
#            dot_xys.append([dot_x,dot_y])
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
#
#
#print(clock.getTime()) 


event.waitKeys()

win.close()


#
#feedback1.draw()
#fixation.draw()
#win.flip()
#event.waitKeys()  # wait for participant to respond
#
#win.close()
#core.quit()