# -*- coding: utf-8 -*-
"""
Created on Tue March  5 11:20:31 2021

@author: Julius Kricheldorff
@instituition: University of Oldenburg

For this Experiment I borrowed from the tutorial by Jonas K. Lindelov
('https://lindeloev.net/psychopy-course/past-courses/cml-seminar-2018/')
and  Arkady Zgonnikov's implementation of a random dot kinematogram:
"https://github.com/cherepaha/Gamble_RDK/blob/master/ui/rdk_mn.py". For the 
translation in angular degrees I used materials by Geoffrey Boynton:
# http://www.mbfys.ru.nl/~robvdw/DGCN22/PRACTICUM_2011/LABS_2011/ALTERNATIVE_LABS/Lesson_2.html


"""
# import os
# os.chdir('/home/jules/Dropbox/PhD_Thesis/DecisionMakingAndLearningStudy/Experiment/Development/RDM_Project/Experiment/')



from psychopy import core, visual, gui, event, data, monitors
import pandas as pd
import random
from prior_rdm.Task_func import trial_writer as tw # import csv writer
from prior_rdm.TwoDotRDM import dot_stimuli as ds # import 2 pop RDM version
from prior_rdm.params import * # import fixed parameter 
from prior_rdm.Task_func import item_struct as itm # generate Items
from prior_rdm.PerceptEqiluminance import HeterochromaticFlicker as flicker # luminance match function

#%% Instructions

# Prepare Input by User/Experimenter
GUI_INP['dateStr'] = data.getDateStr()  # add the current time

# Updates DIALOGUE with dialogue response
inp  = gui.DlgFromDict(GUI_INP, title='Random Dot Motion Task',fixed=['dateStr'])


# Set Monitor
my_monitor = MY_MONITOR

win = visual.Window(size = PIX_SIZE,
    monitor = "DellXPS15_screen",
    units=UNITS,
    fullscr=True, # change to fullscreen later
    color=BG_COLOR, 
)
win.mouseVisible = False

#Instruction Window
Instruction = visual.TextStim(win=win, color=TEXT_COL )
Continue = visual.TextStim(win=win, 
                           color=TEXT_COL, 
                           pos=(0.0, -7.0), 
                           italic=True,
                           height = 0.6)
Continue.text = u'(Um Fortzufahren, drücken Sie bitte die Leertaste.)'

#Fixation cross
fixation = visual.TextStim(win, text='+')


# Addition

Info = visual.TextStim(win=win, color=TEXT_COL, pos=(10.0,0.0))
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
    colorSpace = 'hsv',#'rgb255',
    nElements=DOT_N,
    elementTex=None,
    elementMask="circle",
    xys=coord[0:DOT_N],
    sizes=DOT_SIZE,
    fieldSize = FIELD_SIZE,
    #fieldShape='circle',
    colors=color
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
    Continue.draw()
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

def block_loop(trials, expart):
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
              'Exp_Part': expart,
              'Late_Response': False}
            
        # create a fresh instance for the dots
        color, coord= DOT_UPD.create_dots()
       
        ISI.complete()  # finish theevent.clearEvents()
        condition = False
        #PRESENT STIM,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
        for frame in range(FRAMES):
            
            if frame == 0:
                clock.reset() # t0 for RT
                event.clearEvents() # reset events
                #send onset trigger
            dot_stim.colors, dot_stim.xys = DOT_UPD.update_dots(frame)
            dot_stim.draw()
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
                    Resp_given = True
                    break
        win.flip()  
        
        # in case our participants respond after the stimulus presentation
        if 'Resp_given' not in locals():
            Resp_time = core.getTime()
            while (core.getTime() - Resp_time) < TIME_TO_RESP:
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
win.flip() 

# Participant number has to be included
try:
    if int(inp.data[4])%2 == 0: #this is fucking mega akward. But since we only deal numbers at present, I guess it is okay
        pass
except ValueError:
    print('Please indicate a participant number!')
    win.close()
    core.quit()

# Match Colors
instruction_loop(INST_FLICKER)
hsv_set = flicker.heterochromatic_flicker(win, DOT_G_COL_hsv)
# get class and variables
bl_lists = itm.GetBlockList(hsv_set)

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
              'Late_Response':None,
              'Exp_Part':None}

#set path
save_path =  '/home/jules/Dropbox/PhD_Thesis/DecisionMakingAndLearningStudy/Experiment/Development' 


# start writing
wrt = tw.task_writer(save_path, TRIAL)

# Initialize file
wrt.set_file()
wrt.finish()
win.flip()


# start Block
Experimental_Parts = lis.Exp.unique() # Get Both Experimental Parts
try: # if we have no participant number restart
    if int(inp.data[4])%2 == 0:
        Experimental_Parts = Experimental_Parts[::-1]
except ValueError:
    print('Please indicate a participant number!')
    win.close()
    core.quit()
    
Practice = lis.Block[(lis.Block.apply(lambda x: isinstance(x, str)))].unique() # Practice Blocks
Task = lis.Block[(lis.Block.apply(lambda x: isinstance(x, int)))].unique()
instruction_loop(INTRO)
for exp_ind, exp in enumerate(Experimental_Parts):
    Exp_info = exp_ind +1 # index for experiment part 1 or 2
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
        block_loop(Prtc_trials, Exp_info) #run practice
    Exp_trials = lis.loc[(lis.Block != Practice[0]) & (lis.Block != Practice[1]) & (lis.Exp == exp)] # Get Task Trials
    instruction_loop(task_inst) # display the task instructions
    for blc_idx, block in enumerate(Task):
        trials = Exp_trials.loc[Exp_trials.Block == block] # get Block trials
        block_loop(trials, Exp_info) #run block
instruction_show(END) # Finish Message
win.close()
core.quit()
