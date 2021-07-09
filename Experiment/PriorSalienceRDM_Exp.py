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
import os
os.chdir('/home/jules/Dropbox/PhD_Thesis/DecisionMakingAndLearningStudy/Experiment/Development/RDM_Project/Experiment/')

from psychopy import core, visual, gui, event, data, monitors
import pandas as pd
import random
from PriorPD.Task_func import trial_writer as tw # import csv writer
from PriorPD.TwoDotRDM import dot_stimuli as ds # import 2 pop RDM version
from params import * # import fixed parameter 
from PriorPD.Task_func import item_struct as itm # generate Items

#%% Instructions

# Prepare Input by User/Experimenter
GUI_INP['dateStr'] = data.getDateStr()  # add the current time

# Updates DIALOGUE with dialogue response
inp  = gui.DlgFromDict(GUI_INP, title='Random Dot Motion Task',fixed=['dateStr'])

# get class and variables
bl_lists = itm.GetBlockList(DOT_G_COL)

# Set Monitor

my_monitor = monitors.Monitor(name='DellXPS15_screen')
my_monitor.setSizePix(PIX_SIZE)
my_monitor.setWidth(WIDTH)
my_monitor.setDistance(DISTANCE)
my_monitor.saveMon()


win = visual.Window(size = PIX_SIZE,
    monitor = "DellXPS15_screen",
    units=UNITS,
    fullscr=True, # change to fullscreen later
    color=BG_COLOR
)

win.mouseVisible = False

#Instruction Window
Instruction = visual.TextStim(win=win, color=TEXT_COL )

TaskInfo = visual.TextStim(win=win, color=TEXT_COL, pos=(10.0,0.0))

#Fixation cross
fixation = visual.TextStim(win, text='+')
 
#%% Set Stimuli

# to keep track of time
clock = core.Clock()

# create the dot updating class 
DOT_UPD = ds.RDM_kinematogram(alg= ALG)

color, coord= DOT_UPD.create_dots()

# create the dot stimuli 
dot_stim= visual.ElementArrayStim(
    win=win,
    units=UNITS,
    colorSpace = 'rgb255',
    nElements=DOT_N,
    elementTex=None,
    elementMask="circle",
    xys=coord[0:DOT_N],
    sizes=DOT_SIZE,
    fieldSize = FIELD_SIZE,
    #fieldShape='circle',
    colors=color
)

# create the informative Cues
grating =visual.GratingStim(
    win=win,
    units=UNITS,
    size= GRATE_SIZE,
    sf = (5.0/4.0),
    mask = "circle",
    contrast = GRATE_CONT
    )

# create the non-informative cue 
circle = visual.Circle(
    win=win,
    units=UNITS,
    radius= 2,
    fillColor=CIRCLE_COL,
    lineColor=CIRCLE_COL
)


# Instruction presentation
def instruction_show(text, *BlockIndex):
    ''' Show instruction and wait for a response
    Source: Tutorial Lindelov'''
    if not BlockIndex:
        Instruction.text = text
    else:
        text = text%BlockIndex
        Instruction.text = text
    Instruction.draw()
    win.flip()
    key = event.waitKeys()
    if key == QUIT_KEY:
         win.close()
         core.quit()
    return key

def instruction_loop(instructions, *BlockIndex):
    if not BlockIndex:
        for inst in instructions:
            instruction_show(inst)
    else:
        for ind, inst in enumerate(instructions):
            if ind == 0:
                instruction_show(inst, *BlockIndex)
            else:
                instruction_show(inst)

def block_loop(trials):
    for trl_ind, trial_info in trials.iterrows():
        wrt.start()
        #PRESENT FIXATION
        # Interstimulus interval in frames?
        ISI_1 = round(random.uniform(INTERSTIMI[0], INTERSTIMI[1]),2) 
        
        fixation.draw()
        win.flip()
        ISI = core.StaticPeriod(screenHz=REFRESH)
        ISI.start(ISI_1)  # start a period of 0.5s
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
              'ISI': [ISI_1],
              'Coherence_total': trial_info.Coherence_total,
              'Response': None,
              'Correct': 0, #default is incorrect
              'RT': None,
              'Exp': trial_info.Exp,
              'ColorSwitch': trial_info.ColorSwitch,
              'Late_Response': False}
            
        # create a fresh instance for the dots
        color, coord= DOT_UPD.create_dots()
       
        ISI.complete()  # finish theevent.clearEvents()
        condition = False
        #PRESENT STIM
        for frame in range(FRAMES):
            
            if frame == 0:
                clock.reset() # t0 for RT
                event.clearEvents() # reset events
                #send onset trigger
            dot_stim.colors, dot_stim.xys = DOT_UPD.update_dots(frame)
            dot_stim.draw()
            # TaskInfo.text = 'Coh = ' + str(trial_info.Coherence_total)
            # TaskInfo.draw()
            win.flip()
            keys = event.getKeys(timeStamped=clock)
            if keys != []:
                #print(keys)
                if keys[0][0] in QUIT_KEY:
                    wrt.finish()
                    win.close()
                    core.quit()
                elif condition == False:
                    if keys[0][0] in RESPONSE_KEYS:
                        condition = True
                        new_entries['Response'], new_entries['RT'] = keys[0]
                    elif keys[0][0] in NUMBER_KEYS:
                        condition = True
                        new_entries['Response'], new_entries['RT'] = keys[0]
                        #break # break presentation loop early
                    event.clearEvents()
                    Resp_given = core.getTime()
                    break
            # elif frame == FRAMES and keys == []:
            #     new_entries['Response'] = 'No_resp'
            #     new_entries['RT'] = None
        win.flip()  
        
        while (core.getTime() - Resp_given) < TIME_TO_RESP:
            keys = event.getKeys(timeStamped=clock)
            if keys != [] and condition == False:
                condition = True
                if keys[0][0] in RESPONSE_KEYS:
                    new_entries['Response'], new_entries['RT'] = keys[0]
                    new_entries['Late_Response'] = True
                    #break # break presentation loop early
                elif keys[0][0] in NUMBER_KEYS:
                    new_entries['Response'], new_entries['RT'] = keys[0]
                    new_entries['Late_Response'] = True
            elif keys !=[]:
                if keys[0][0] in QUIT_KEY:
                    wrt.finish()
                    win.close()
                    core.quit()
        #Write Trial Information´
        if new_entries['Response'] == new_entries['Direction']:
            new_entries['Correct'] = 1
        wrt.update(new_entries)
        wrt.finish()
   
    # Display Instructions to indicate Block ended
    if trial_info.Block == 'Practice_1' or trial_info.Block == 'Practice_2':
        instruction_show(PRACTICE_INST)
    elif int(trial_info.Block)+1 == 4:
        instruction_show(EXP_END)
    else:
        instruction_loop(BLOCK_INSTR, int(trial_info.Block)+1) #BLOCKBREAK SCREEN
     
    
    


#%% Experimental loop

Instruction.text = 'LADE DATEN ...'
Instruction.draw()
# generate the list
lis = bl_lists.init_list()
# randomize items per block
lis = lis.sample(frac=1)
lis = lis.sort_values(by=['Exp', 'Block'])
lis = lis.reset_index()
lis = lis.drop(['index'], axis = 1) # get rid of the extra index column
    
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
              'Exp':None,
              'ColorSwitch':None,
              'Date': inp.data[5],
              'Late_Response':None}
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
win.flip()


# start Block
Experimental_Parts = lis.Exp.unique() # Get Both Experimental Parts
if inp.data[4]%2 == 0:
    Experimental_Parts = Experimental_Parts[::-1]
Practice = lis.Block[(lis.Block.apply(lambda x: isinstance(x, str)))].unique() # Practice Blocks
Task = lis.Block[(lis.Block.apply(lambda x: isinstance(x, int)))].unique()
for exp in Experimental_Parts:
    #exp = 'Exp_Part'
    # Start the Practice Session
    # Get the correct instructions
    if exp == 'Exp_Full': 
        prtc_inst = PRACTICE_FULL
        task_inst = EXP_FULL 
    else:
        prtc_inst = PRACTICE_PART
        task_inst = EXP_PART
    for prac_idx, prac in enumerate(Practice):
        instruction_loop(prtc_inst[prac_idx]) #display the practice instructions
        Prtc_trials = lis.loc[(lis.Block == prac) & (lis.Exp == exp)] # Get practice trials
        block_loop(Prtc_trials) #run practice
    Exp_trials = lis.loc[(lis.Block != Practice[0]) & (lis.Block != Practice[1]) & (lis.Exp == exp)] # Get Task Trials
    instruction_loop(task_inst) # display the task instructions
    for blc_idx, block in enumerate(Task):
        trials = Exp_trials.loc[Exp_trials.Block == block] # get Block trials
        block_loop(trials) #run block
instruction_show(END) # Finish Message
win.close()
core.quit()
