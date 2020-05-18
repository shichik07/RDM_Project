"""measure your JND in orientation using a staircase method"""
from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import numpy, random, os

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

frames = 120
n_dots = 100
trgt_size = 10 # size of the group of coherently moving dots
dot_xys = []
dot_speed= 5
dot_size = 10

# index of random dots
coh_dot = random.sample(range(n_dots),  trgt_size) 

# to keep track of time
clock = core.Clock()

for dot in range(n_dots):
    dot_x = random.uniform(-200,200)
    dot_y = random.uniform(-200,200)
    dot_xys.append([dot_x,dot_y])


dot_stim = visual.ElementArrayStim(
    win=win,
    units="pix",
    nElements=n_dots,
    elementTex=None,
    elementMask="circle",
    xys=dot_xys,
    sizes=dot_size
)

clock.reset()

dot_xys = []
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
    dot_stim.xys = dot_xys
    dot_stim.draw()
    win.flip()


print(clock.getTime()) 


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