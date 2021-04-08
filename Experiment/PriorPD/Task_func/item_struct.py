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
        self.BlockBias = [1,3,5], [0,2,4]
        self.Trial_Nr = 36
        self.Coherence_Levels = [0, 0.1, 0.2, 0.5]
        self.Conditions = ['Mono', 'Di_null', 'Di_part', 'Di_full']
        self.Directions = ['left', 'right']
        self.minorDir = ['left', 'right']
        self.Block = 6
        self.proportion = [0.2, 1.8]
        self.Trial_total = self.Trial_Nr* len(self.Conditions)*len(self.Coherence_Levels)
        # repeats per unique individual item
        self.reps_itm = 3
        # Create Item Pandas frame
        self.Items = pd.DataFrame({ 'Condition': [None]*self.Trial_total, 
                                       'Coherence': [None]*self.Trial_total,
                                    'Colors': [None]*self.Trial_total,
                                         'Direction': [None]*self.Trial_total,
                                         'Block': [None]*self.Trial_total,
                                  'Coherence_total': [None]*self.Trial_total})
        
    def init_list(self, colors, Block_order):
        # determine in which manner we bias our list allocation (to reach the 75|25 color imbalance)
        if Block_order == 1:
            bias_con = self.BlockBias[1]
        elif Block_order == 0:
             bias_con = self.BlockBias[0]
        else: 
            raise ValueError('Please specify Block_order as either 0 or 1') 
            
        #set color
        Color = pd.Series(colors)

            
        # important to shuffle coherence values
        random.shuffle(self.Coherence_Levels)
        ind = 0
        for blck in range(self.Block): 
            # important to shuffle coherence values
            random.shuffle(self.Coherence_Levels)
            for con_idx, con in enumerate(self.Conditions):
                for coh in self.Coherence_Levels:
                    coh_count = 0
                    for resp in self.Directions:
                        for rp in range(self.reps_itm):
                            self.Items.loc[ind, 'Block'] = blck
                            self.Items.loc[ind, 'Condition'] = con
                            self.Items.at[ind, 'Coherence'] = self.translate_coherence(con, coh)
                            self.Items.loc[ind, 'Coherence_total'] = coh
                            self.Items.loc[ind, 'Direction'] = self.Directions[ind%len(self.Directions)]
                            self.Items.at[ind, 'Colors'] = Color[con_idx]
                          
                            if con == self.Conditions[3]:
                                #for the fully informative condition 75% of the items will be switched
                                if coh_count <= 3:
                                    #Swap the colors
                                    self.Items.at[ind, 'Colors'] = self.reverse_color(self.Items.at[ind, 'Colors'])
                            elif con == self.Conditions[2]:
                                #for the partially informative condition (50% of the items are switched)
                                if coh_count <= 2:
                                    #Swap Colors
                                    self.Items.at[ind, 'Colors'] = self.reverse_color(self.Items.at[ind, 'Colors'])
                                    
                            # To make the last two directions random - otherwise we will have the low probability relevant condition more often left than right moving
                            # for the fully informative condition only. for the partially informative condition we have to do the same for the third and sxth index
                            if con == self.Conditions[3]:
                                if coh_count == 4:
                                    random.shuffle(self.minorDir)
                                    self.Items.loc[ind, 'Direction'] = self.minorDir[0]
                                elif coh_count == 5:
                                    #here take the other direction helps us to get a more unbiased list for each participant
                                    self.Items.loc[ind, 'Direction'] = self.minorDir[1]
                            elif con == self.Conditions[2]:
                                #for the partially informative condition
                                if coh_count == 2:
                                    random.shuffle(self.minorDir)
                                    self.Items.loc[ind, 'Direction'] = self.minorDir[0]
                                elif coh_count == 5:
                                    #here take the other direction helps us to get a more unbiased list for each participant
                                    self.Items.loc[ind, 'Direction'] = self.minorDir[1]
                            
                            # Here we make sure that overall we get to our 75%|25% major color distinction per majority coherence
                            # in an approximately random manner
                            if con == self.Conditions[3]:
                                if blck in bias_con and coh_count == 4:
                                    if coh == self.Coherence_Levels[1] or coh == self.Coherence_Levels[3]:
                                        self.Items.at[ind, 'Colors'] = self.reverse_color(self.Items.at[ind, 'Colors'])
                                elif blck not in bias_con and coh_count == 4:
                                    if coh == self.Coherence_Levels[0] or coh == self.Coherence_Levels[2]:
                                        self.Items.at[ind, 'Colors'] = self.reverse_color(self.Items.at[ind, 'Colors'])
                                    
                            # Update indices
                            ind +=1
                            coh_count += 1
        # Have to copy - otherwise everytime we create a new list all former list will be the same. Prob would have been smarter to create a new pandas frame every time                    
        Item_list = self.Items.copy()
        return Item_list
    
    def reverse_color(self,entry):
        col = entry[::-1]
        return col
    
    def translate_coherence(self, condition, coherence):
        # if both dot pops contain the same amount of info or are colored the same
        if condition ==  self.Conditions[0] or condition == self.Conditions[1]:
            coh_two = [[coherence, coherence]]
        else:
            # if one of the two dot pops has to contain more info than the other
            coh_two = [[round(coherence*self.proportion[0],2), round(coherence*self.proportion[1],2)]]
        return coh_two
    
#%% How to use
# a = GetBlockList()
# BiasC =  [0,1]
# colors = [[ -1,0,1],[ 1,0,1]], [[ 3,3,3],[ 5,5,5]], [[ 7,7,7],[ 1,1,1]], [[ 9,9,9],[ 2,2,2]]
# colors2 = [None]*4
# for ix,col in enumerate(colors): 
#     colors2[ix] = a.reverse_color(col)


# # for x in y:
#     # bs = BiasC[x%2]
#     # if x%4 <=2:
#     #     col = colors
#     # else:
#     #     col = colors2
#     # lis= a.init_list(3, bs)

# lis= a.init_list(colors, BiasC[0])
# lis2= a.init_list(colors2, BiasC[0])

