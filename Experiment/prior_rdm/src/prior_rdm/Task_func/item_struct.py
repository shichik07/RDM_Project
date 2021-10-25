#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 13:42:04 2021

@author: jules
"""
import pandas as pd
import numpy as np
import random
from prior_rdm.params import * # import fixed parameter 


class GetBlockList():
    '''
        Class which returns a the unrandomized practice and experimental Item Lists.
        Not very flexible and hardcoded in part. Only intended to be used in our experiment.
        Sorry for the mess.
    
            '''
    def __init__(self, Col_con):
        # Define List parameter
        self.Trial_Nr = TASK_NR
        self.Practice_Nr = PRACTICE_NR
        self.Coherence_Levels = COHERENCE
        self.Conditions = EXP_CON
        self.Directions = RESPONSE_KEYS
        self.Block = BLOCK_NRS
        self.proportion = PROPORTION 
        self.Color = Col_con 
        self.Prtc_col = PRTC_FULL_COL 
        self.Trial_total = self.Trial_Nr* len(self.Conditions)*len(self.Coherence_Levels)
        self.Total_prtc = self.Practice_Nr*4
        # Create Item Pandas frame
        self.Items = pd.DataFrame({ 'Condition': [None]*self.Trial_total, 
                                       'Coherence': [None]*self.Trial_total,
                                    'Colors': [None]*self.Trial_total,
                                         'Direction': [None]*self.Trial_total,
                                         'Block': [None]*self.Trial_total,
                                  'Coherence_total': [None]*self.Trial_total,
                                 'Exp': [None]*self.Trial_total,
                             'ColorSwitch': [None]*self.Trial_total})
        self.Practice = pd.DataFrame({ 'Condition': [None]*self.Total_prtc, 
                                       'Coherence': [None]*self.Total_prtc,
                                    'Colors': [None]*self.Total_prtc,
                                         'Direction': [None]*self.Total_prtc,
                                         'Block': [None]*self.Total_prtc,
                                  'Coherence_total': [None]*self.Total_prtc,
                                 'Exp': [None]*self.Total_prtc,
                             'ColorSwitch': [None]*self.Total_prtc})
        
    def generate_items(self):
        '''
        Function which operates on the initialized item list of the class.
        Create the basic balanced item combination for all experimental conditions.
    
        Parameters
        ----------
        
        Returns
        -------

            '''
        # create all possible Item combinations
        ind = 0
        for con_idx, con in enumerate(self.Conditions):
            for coh in self.Coherence_Levels:
                for rep in range(self.Trial_Nr):
                    self.Items.loc[ind, 'Condition'] = con
                    self.Items.at[ind, 'Coherence'] = self.translate_coherence(con, coh)
                    self.Items.loc[ind, 'Coherence_total'] = coh
                    self.Items.loc[ind, 'Direction'] = self.Directions[ind%len(self.Directions)]
                    self.Items.at[ind, 'Colors'] = self.Color[con_idx]
                    ind += 1
                    
    def init_list(self):
        '''
        Function which calls individual class functions to generate the item and
        practice list, and functions to get balanced blocks for the experimental
        parts and implement the color ration manipulations.
    
        Parameters
        ----------
        
        Returns
        -------
        All : Pandas DataFrame - 
            A DataFrame containing both all practice and experimental items
    
            '''
        #get the basic item list
        self.generate_items()
        # allocate items to experimental parts and blocks
        self.get_blocks()
        # put in informative ratios for colors
        self.color_ratios()
        # Generate the practice items
        self.generate_practice()
        # Put items and practice together
        All = pd.concat([self.Items, self.Practice])
        return All
    
        
    def get_blocks(self):
        '''
        Function which operates on the initialized item list of the class.
        Creates the balanced blocks for each experimental part.
    
        Parameters
        ----------
        
        Returns
        -------
    
            '''
        for con in self.Conditions:
            for coh in self.Coherence_Levels:
                con_in = self.Items.index[(self.Items['Condition'] == con) & (self.Items['Coherence_total'] == coh)] 
                if con == self.Conditions[0] or con == self.Conditions[1]:
                    con_in = self.Items.index[(self.Items['Condition'] == con) & (self.Items['Coherence_total'] == coh)] 
                    # Assort items to individual blocks and split between full and partially informative
                    blocks = np.repeat(self.Block, [self.Trial_Nr/len(self.Block)/2], axis=0)
                    self.Items.loc[con_in[0:int(self.Trial_Nr/2)], 'Block'] = blocks
                    self.Items.loc[con_in[0:int(self.Trial_Nr/2)], 'Exp'] = 'Exp_Full' 
                    self.Items.loc[con_in[int(self.Trial_Nr/2): self.Trial_Nr], 'Block'] =  blocks
                    self.Items.loc[con_in[int(self.Trial_Nr/2): self.Trial_Nr], 'Exp'] = 'Exp_Part'
                else:
                    blocks = np.repeat(self.Block, [int(self.Trial_Nr/len(self.Block))], axis=0)
                    self.Items.loc[con_in, 'Block'] = blocks
                    if con == self.Conditions[2]:
                         self.Items.loc[con_in, 'Exp'] = 'Exp_Part'
                    else:
                         self.Items.loc[con_in, 'Exp'] = 'Exp_Full'
    
    def generate_practice(self):
        '''
        Function which calls individual class functions to generate the practice 
        trials for both the partial informative and fully informative experimental part.

        Parameters
        ----------
        
        Returns
        -------
            '''
        self.partial_practice()
        self.full_practice()
    
    def full_practice(self):
        '''
        Function which operates on the initialized item practice List of the class.
        Create the basic balanced item combination the fully informative practice items.
    
        Parameters
        ----------
        
        Returns
        -------

            '''
        con = self.Conditions[3]
        ind = 0
        # first Part of the Practice
        for coh in self.Coherence_Levels:
                for rep_idx, rep in enumerate(range(int(self.Practice_Nr/4 + 4))):
                    self.Practice.loc[ind, 'Condition'] = con
                    self.Practice.at[ind, 'Coherence'] = self.translate_coherence(con, coh)
                    self.Practice.loc[ind, 'Coherence_total'] = coh
                    self.Practice.loc[ind, 'Direction'] = self.Directions[ind%len(self.Directions)]
                    self.Practice.loc[ind, 'Exp']  = 'Exp_Full' 
                    if rep_idx >=8:
                        self.Practice.loc[ind, 'Block'] ='Practice_2'
                        self.Practice.at[ind, 'Colors'] = self.Color[3]
                    else:
                        self.Practice.loc[ind, 'Block'] ='Practice_1'
                        self.Practice.at[ind, 'Colors'] = self.Color[3] # uni colored items for this practice
                    ind += 1
        # second Part of the practice
        uninformative = self.Conditions[0:2]
        for con_idx, con in enumerate(uninformative):
            for  coh in self.Coherence_Levels:
                    for rep in range(2):
                        self.Practice.loc[ind, 'Condition'] = con
                        self.Practice.at[ind, 'Coherence'] = self.translate_coherence(con, coh)
                        self.Practice.loc[ind, 'Coherence_total'] = coh
                        self.Practice.loc[ind, 'Direction'] = self.Directions[ind%len(self.Directions)]
                        self.Practice.at[ind, 'Colors'] = self.Color[con_idx]
                        self.Practice.loc[ind, 'Exp']  = 'Exp_Full' 
                        self.Practice.loc[ind, 'Block'] ='Practice_2'
                        ind += 1
    
    def partial_practice(self):
        '''
        Function which operates on the initialized item practice List of the class.
        Create the basic balanced item combination the partially informative practice items.
    
        Parameters
        ----------
        
        Returns
        -------

            '''
        con = self.Conditions[2]
        ind = int(self.Total_prtc/2)  
        for coh in self.Coherence_Levels:
                for rep_idx, rep in enumerate(range(int(self.Practice_Nr/4 + 4))):
                    self.Practice.loc[ind, 'Condition'] = con
                    self.Practice.at[ind, 'Coherence'] = self.translate_coherence(con, coh)
                    self.Practice.loc[ind, 'Coherence_total'] = coh
                    self.Practice.loc[ind, 'Direction'] = self.Directions[ind%len(self.Directions)]
                    self.Practice.at[ind, 'Colors'] = self.Color[2]
                    self.Practice.loc[ind, 'Exp']  = 'Exp_Part' 
                    if rep_idx <=3:
                        self.Practice.loc[ind, 'ColorSwitch']= 'True'   
                    if rep_idx >=8:
                        self.Practice.loc[ind, 'Block'] ='Practice_2'
                        if rep_idx < 10:
                            self.Practice.loc[ind, 'ColorSwitch']= 'True'   
                    else:
                        self.Practice.loc[ind, 'Block'] ='Practice_1'
                    ind += 1     
        # switch color directions
        Swtch_idx = self.Practice.index[(self.Practice['ColorSwitch'] == 'True')] 
        self.Practice.Colors.loc[Swtch_idx] = self.Practice.Colors.loc[Swtch_idx].apply(lambda x: self.reverse_color(x))
        # second Part of the practice
        uninformative = self.Conditions[0:2]
        for con_idx, con in enumerate(uninformative):
            for coh in self.Coherence_Levels:
                    for rep in range(2):
                        self.Practice.loc[ind, 'Condition'] = con
                        self.Practice.at[ind, 'Coherence'] = self.translate_coherence(con, coh)
                        self.Practice.loc[ind, 'Coherence_total'] = coh
                        self.Practice.loc[ind, 'Direction'] = self.Directions[ind%len(self.Directions)]
                        self.Practice.at[ind, 'Colors'] = self.Color[con_idx]
                        self.Practice.loc[ind, 'Exp']  = 'Exp_Part' 
                        self.Practice.loc[ind, 'Block'] ='Practice_2'
                        ind += 1
                    
    def color_ratios(self):
        '''
        Function which operates on the initialized item list of the class.
        Creates the proabilistic informativeness of the practiced color combinations,
        i.e. colors are switched with regards to coherence on part of the items.
        50/50 for the partially informative condition and 80/20 for the fully 
        informative condition.
    
        Parameters
        ----------
        
        Returns
        -------
    
            '''
        for con in self.Conditions[2:]:
            for coh in self.Coherence_Levels:
                for blck in self.Block:
                    con_in = self.Items.index[(self.Items['Condition'] == con) & (self.Items['Coherence_total'] == coh) & (self.Items['Block'] == blck)] 
                    if con == self.Conditions[2]:
                        if blck%2 == 0:
                            #switch colors index 0:6  and 6:12 so we make sure we have equal proportions left 
                            # and right over the whole experiment
                            self.Items.Colors.loc[con_in[0:6]] = self.Items.Colors.loc[con_in[0:5]].apply(lambda x: self.reverse_color(x))
                            self.Items.ColorSwitch.loc[con_in[0:6]] = 'True' # not really true for partially informative but important
                        else:
                            # and 6:12
                            self.Items.Colors.loc[con_in[6:12]] = self.Items.Colors.loc[con_in[5:10]].apply(lambda x: self.reverse_color(x))
                            self.Items.ColorSwitch.loc[con_in[6:12]] = 'True'
                    else:
                        # switch colors for the first two indices only (80/20)
                        self.Items.Colors.loc[con_in[0:2]] = self.Items.Colors.loc[con_in[0:2]].apply(lambda x: self.reverse_color(x))
                        self.Items.ColorSwitch.loc[con_in[0:2]] = 'True'    
                        
                                   
    def reverse_color(self,entry):
        '''
        Function revereses the order of an entered list, in case of the class, color
        ----------
        
        
        Parameters
        ----------
        entry: list - colors of the items
        
        Returns
        -------
        col :  list - colors of the items in reversed order
            '''
        col = entry[::-1]
        return col
                
                    
    
    def translate_coherence(self, condition, coherence):
        '''
        Function which calculates the total coherence of an RDM trial onto two
        independent dot groups. Distinguishes conditions - non-informative conditions
        have equal proportions, informative conditions have 1:1 coherence per group,
        informative conditions have 1:9 coherence per group.
        ----------
        
        
        Parameters
        ----------
        conditio: string - Name of the experimental condition in question
        coherence: float - Total Coherence value per trial
        
        Returns
        -------
        coh_two :  list - two coherence values for each dot group
            '''
        # if both dot pops contain the same amount of info or are colored the same
        if condition ==  self.Conditions[0] or condition == self.Conditions[1]:
            coh_two = [[coherence, coherence]]
        else:
            # if one of the two dot pops has to contain more info than the other
            coh_two = [[round(coherence*self.proportion[0],2), round(coherence*self.proportion[1],2)]]
        return coh_two