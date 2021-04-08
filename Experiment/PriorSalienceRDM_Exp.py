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
import pandas as pd
import random
from PriorPD.Task_func import trial_writer as tw
from PriorPD.TwoDotRDM import dot_stimuli as ds

#%% Instructions



# Set Monitor

my_monitor = monitors.Monitor(name='DellXPS15_screen')
my_monitor.setSizePix((1366, 768))
my_monitor.setWidth(31)
my_monitor.setDistance(60)
my_monitor.saveMon()


win = visual.Window(size = [800, 800],#[1920,1080],
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
DOT_UPD = ds.RDM_kinematogram()
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

direct = r'/home/jules/Dropbox/PhD_Thesis/DecisionMakingAndLearningStudy/Experiment/Development/Lists/'
lis = pd.read_csv(direct +'PriorRDM_PilotList_' + str(ID)  +'.csv')
   
# Initialize data saving
# Insert columns
TRIAL ={'Trial_nr': None , 
              'Condition':None, 
              'Gender': inp.data[1],
              'Correct': None,
              'Coherence': None,
              'Response': None,
              'Group': inp.data[2],
              'Direction': None,
              'Age': inp.data[0],
              'Block': None,
              'RT': None,
              'Colors': None,
              'ISI': None,
              'Early_resp': None,
              'Handedness': inp.data[3],
              'Part_Nr': inp.data[4],
              'Coherence_total':None,
              'Date': inp.data[5]}
#set path
save_path =  '/home/jules/Dropbox/PhD_Thesis/DecisionMakingAndLearningStudy/Experiment/Development' 
# start writing
wrt = tw.task_writer(save_path, TRIAL)

# Create Trial dictionary
BaseInf =  {'Gender': inp.data[1],
          'Group': inp.data[2],
          'Age': inp.data[0],
          'Handedness': inp.data[3],
          'Part_Nr': inp.data[4],
          'Date': inp.data[5]}


# Initialize file
wrt.set_file()
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
    
#instruction_show(text_fin)
