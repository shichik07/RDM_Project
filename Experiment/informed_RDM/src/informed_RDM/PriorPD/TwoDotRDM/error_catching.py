#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 16:38:02 2021

@author: jules
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
from PriorPD.PerceptEqiluminance import HeterochromaticFlicker as flicker # lum


DOT_UPD = ds.RDM_kinematogram(alg= ALG)

color, coord= DOT_UPD.create_dots()

bl_lists = itm.GetBlockList(DOT_G_COL_hsv)
lis = bl_lists.init_list()
# randomize items per block
lis = lis.sample(frac=1)
lis = lis.sort_values(by=['Exp', 'Block'])
lis = lis.reset_index()
lis = lis.drop(['index'], axis = 1) # get rid of the extra index column


for trl_ind, trial_info in lis.iterrows():
    DOT_UPD.update_params(direction = trial_info.Direction, 
                              color= trial_info.Colors, 
                              coherence = trial_info.Coherence)
    color, coord= DOT_UPD.create_dots()
    if str(trial_info.Condition) == 'Di_full':
        print("Condition " + str(trial_info.Condition) + " movement " + str(trial_info.Coherence))
        for i in range(1):
            colors, xys = DOT_UPD.update_dots(i)