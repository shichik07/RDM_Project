#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 13:42:04 2021

@author: jules
"""
import random
import pandas as pd
import numpy as np


class GetBlockList(object):
    def __init__(self):
        # Define List parameter
        self.Trial_Nr = 36
        self.Coherence_Levels = [0, 0.1, 0.2, 0.5]
        self.Conditions = ['Mono', 'Di_null', 'Di_part', 'Di_full']
        self.Directions = ['left', 'right']
        self.Block = 6
        self.Color = [[ -1,0,1],[ 1,0,1]], [[ -1,0,1],[ 1,0,1]], [[ -1,0,1],[ 1,0,1]], [[ -1,0,1],[ 1,0,1]]
        self.Color = pd.Series(self.Color)
        self.proportion = [0.2, 1.8]
        self.Trial_total = self.Trial_Nr* len(self.Conditions)*len(self.Coherence_Levels)
        # repeats per unique individual item
        self.reps_itm = 3
        # Create Item Pandas frame
        self.Items = pd.DataFrame({ 'Condition': [None]*self.Trial_total, 
                                       'Coherence': [None]*self.Trial_total,
                                    'Colors': [None]*self.Trial_total,
                                         'Direction': [None]*self.Trial_total,
                                         'Block': [None]*self.Trial_total},
                                  'Coherence_total': [None]*self.Trial_total)
        
    def init_list(self, colors):
        ind = 0
        for blck in range(self.Block):    
            for con_idx, con in enumerate(self.Conditions):
                for coh in self.Coherence_Levels:
                    coh_count = 0
                    for resp in self.Directions:
                        for rp in range(self.reps_itm):
                            self.Items.loc[ind, 'Block'] = blck
                            self.Items.loc[ind, 'Condition'] = con
                            self.Items.at[ind, 'Coherence'] = self.translate_coherence(con, coh)
                            self.Items.loc[ind, 'Coherence_total'] coh
                            self.Items.loc[ind, 'Direction'] = self.Directions[ind%len(self.Directions)]
                            self.Items.at[ind, 'Colors'] = self.Color[con_idx]
                            
                            if con == self.Conditions[3]:
                                if coh_count <= 7:
                                    #Swap the colors
                                    self.Items.at[ind, 'Colors'] = self.reverse_color(self.Items.at[ind, 'Colors'])
                                if coh_count == 7 or coh_count == 7:
                                    #determine direction at random (we have 6 reps per unique item - 75% of those need to be for one color)
                                    # in order to have items approximately balanced across blocks one item needs to be selected at random determined
                                      self.Items.loc[ind, 'Direction'] = random.choice(self.Directions)
                            if con == self.Conditions[2]:
                                if coh_count <= 5:
                                    #Swap Colors
                                    self.Items.at[ind, 'Colors'] = self.reverse_color(self.Items.at[ind, 'Colors'])
                            # Update indices
                            ind +=1
                            coh_count += 1
        return self.Items 
    
    def reverse_color(self,entry):
        col = entry
        list.reverse(col)
        return col
    
    def translate_coherence(self, condition, coherence):
        # if both dot pops contain the same amount of info or are colored the same
        if condition ==  self.Conditions[0] or condition == self.Conditions[1]:
            coh_two = [[coherence, coherence]]
        else:
            # if one of the two dot pops has to contain more info than the other
            coh_two = [[round(coherence*self.proportion[0],2), round(coherence*self.proportion[1],2)]]
        return coh_two
    
#%% Playground

           
a = GetBlockList()
lis = a. init_list(3)
