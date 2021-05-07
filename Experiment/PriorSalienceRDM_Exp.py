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
os.chdir('/home/jules/Dropbox/PhD_Thesis/DecisionMakingAndLearningStudy/Experiment/Development/RDM_Project/Experiment')

from psychopy import core, visual, gui, event, data, monitors
import pandas as pd
import random
from PriorPD.Task_func import trial_writer as tw # import csv writer
from PriorPD.TwoDotRDM import dot_stimuli as ds # import 2 pop RDM version
from params import * # import fixed parameter 
from PriorPD.Task_func import item_struct as itm # generate Items

#%% Instructions



# Set Monitor

my_monitor = monitors.Monitor(name='DellXPS15_screen')
my_monitor.setSizePix(PIX_SIZE)
my_monitor.setWidth(WIDTH)
my_monitor.setDistance(DISTANCE)
my_monitor.saveMon()


win = visual.Window(size = PIX_SIZE,
    monitor = "DellXPS15_screen",
    units=UNITS,
    fullscr=False, # change to fullscreen later
    color=BG_COLOR
)


#Instruction Window
Instruction = visual.TextStim(win=win, color=TEXT_COL )

TaskInfo = visual.TextStim(win=win, color=TEXT_COL, pos=(10.0,0.0))

#Fixation cross
fixation = visual.TextStim(win, text='+')
    

txt_1 = 'Willkommen bei unserem Experiment'
txt_2 = u'In diesem Experiment werden Sie sich scheinbar zufäälig bewegende Punkte auf dem Bildschirm sehen.'
txt_3 = u'Die Punkte sind entweder weiß in machen Versuchen, oder Rot und Blau in anderen.'
txt_4 = u'Ihre Aufgabe wird es sein zu bestimmen ob sich diese Punkte jeweils mehrheitlich nach Links oder nach Rechts bewegen.'
txt_5 = u'Dabei bekommen Sie vor jedem Versuch einen Hinweis.'
txt_6 = u'Sehen Sie einen weißen Kreis, können Sie sich allein auf die Punkte und deren Bewegungen konzentrieren.'
txt_7 = u'Wenn Sie einen vertikal schattierten Kreis sehen, heißt das Sie sehen gleich Rote und Blaue Punkte. Und eine der beiden Farben wird sich im Experiment mehrheitlich in eine Richtung bewegen.'
txt_8 = u'Um mit dem Experiment zu beginnen, drücken Sie bitte die Leertaste.'
txt_blcP = u'Sie haben das Ende des Blocks erreicht, drücken SIe die Leertaste um fortzufahren.'
text_fin = u'You have finished the end of the Experiment. Thank you for your participation!'
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
    nElements=20,
    elementTex=None,
    elementMask="circle",
    xys=coord[0:20],
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
def instruction_show(text):
    ''' Show instruction and wait for a response
    Source: Tutorial Lindelov'''
    Instruction.text = text
    Instruction.draw()
    win.flip()
    key = event.waitKeys()
    if key == QUIT_KEY:
         win.close()
         core.quit()
    return key

def instruction_loop(instructions):
    for inst in instructions:
        instruction_show(inst)
        

def block_loop(trials):
    for trl_ind, trial_info in trials.iterrows():
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
              'ColorSwitch': trial_info.ColorSwitch}
            
        # create a fresh instance for the dots
        color, coord= DOT_UPD.create_dots()
       
        ISI.complete()  # finish theevent.clearEvents()
        
        #PRESENT STIM
        for frame in range(FRAMES):
            if frame == 0:
                clock.reset() # t0 for RT
                event.clearEvents() # reset events
                #send onset trigger
            dot_stim.colors, dot_stim.xys = DOT_UPD.update_dots(frame)
            dot_stim.draw()
            TaskInfo.text = 'Coh = ' + str(trial_info.Coherence_total)
            TaskInfo.draw()
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
            elif frame == FRAMES and keys == []:
                new_entries['Response'] = 'No_resp'
                new_entries['RT'] = None
          
        #Write Trial Information 
        if new_entries['Response'] == new_entries['Direction']:
            new_entries['Correct'] = 1
        
        wrt.update(new_entries)    
    wrt.finish() # save intermediate results
    instruction_show(txt_blcP) #BLOCKBREAK SCREEN
     
    
    


#%% Experimental loop

# Prepare Input by User/Experimenter
GUI_INP['dateStr'] = data.getDateStr()  # add the current time

# Updates DIALOGUE with dialogue response
inp  = gui.DlgFromDict(GUI_INP, title='Random Dot Motion Task',fixed=['dateStr'])

# get class and variables
bl_lists = itm.GetBlockList(DOT_G_COL)



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

win.flip()
instruction_show(txt_1)
instruction_show(txt_2)
instruction_show(txt_3)
instruction_show(txt_4)
instruction_show(txt_5)
instruction_show(txt_6)
instruction_show(txt_7)
instruction_show(txt_8)


## Initialize data saving
wrt.start()


# start Block
Experimental_Parts = lis.Exp.unique() # Get Both Experimental Parts
Practice = lis.Block[(lis.Block.apply(lambda x: isinstance(x, str)))].unique() # Practice Blocks
Task = lis.Block[(lis.Block.apply(lambda x: isinstance(x, int)))].unique()
for exp in Experimental_Parts:
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
        Prtc_trials = lis.loc[(lis.Block == prac) and (lis.Exp == exp)] # Get practice trials
        block_loop(Prtc_trials) #run practice
    Exp_trials = lis.loc[(lis.Block != Practice[0]) & (lis.Block != Practice[1]) & (lis.Exp == exp)] # Get Task Trials
    instruction_loop(task_inst) # display the task instructions
    for blc_idx, block in enumerate(Task):
        trials = lis.loc[lis.Block == block] # get Block trials
        block_loop(trials) #run block
        if blc_idx == len(block):
            instruction_show(BLOCK_INSTR)
instruction_show(END) # Finish Message
