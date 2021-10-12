#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 12:32:16 2021

@author: jules
"""

import pandas as pd
import string
import os
from random import randrange, choice, seed
from prior_rdm.params import * 

class pseudonym():
    def __init__(self, seed_nr = RANDOMSEED, 
                 loc_string = SAVE_PATH, 
                 max_subj = LIST_MAX_NR):
        '''
        Function with parameters to initialize pseudonym generation.
        ----------
        
        
        Parameters
        ----------
        
        loc_string: str - string with the location where trial information is to be saved
        max_subj: int - number of pseudonyms to be generated
        seed_nr : random seed to make pseudonym generation reproducible
        
        
        Returns
        -------
        
        '''
        
        self.random_seed = seed_nr
        self.nr = max_subj 
        self.loc = loc_string
        self.path = self.loc + '/pseudo_list.csv'
    
    def create_csv_pseudo(self):
        '''
        Function to generate pseudonyms. Saves a csv file with pseudonyms if none has been generated yet
        ----------
        
        
        Parameters
        ----------
        
        
        
        Returns
        -------
        
      
        '''
        if not os.path.exists(self.path):
            seed(self.random_seed)
            Alphab = list(string.ascii_uppercase)
            code = pd.DataFrame({'Code':[None]*self.nr,
                                 'Condition':['PD']*int(self.nr/2) + ['HC']*int(self.nr/2),
                                 'Number': [int(x+1) for x in range(int(self.nr/2))]*2,
                                 'Participant': [None]*self.nr
                                 })
            cd = 0
            while cd < self.nr:
                Pseudo = choice(Alphab) + choice(Alphab) + choice(Alphab)
                Pseudo += str(randrange(10)) + str(randrange(10))
                cont = code.loc[code['Code'] == Pseudo]
                if len(cont)!= 0:
                    pass
                else:
                    code.loc[cd, 'Code'] = Pseudo
                    cd +=1
            # save pseudonyms
            if  len(code.Code.unique()) == self.nr: # double check
                code.to_csv(self.path)
            else:
                raise ValueError('Something with the pseudonym generation went wrong')
                
    def get_pseudonym(self, index, con):
        '''
        Function to retrieve a pseudonym for a participant
        ----------
        
        
        Parameters
        ----------
        index: int - index of the current participant number 
        
        
        
        Returns
        -------
        part_code: str - string with the pseudonym for the current participant number
        
      
        '''
        
        code = pd.read_csv(self.path)
        target_ind = code.index[(code['Condition'] == con) & (code['Number'] == index)] 
        part_code = code.Code.loc[target_ind].item()
        return part_code

