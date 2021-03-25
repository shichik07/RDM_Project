#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 12:51:38 2021

@author: jules
"""
import csv, os

class task_writer():
    def __init__(self, loc_string):
        self.trial_dict = {'Trial_nr': None , 
              'Condition':None, 
              'Gender': None,
              'Correct': None,
              'Coherence': None,
              'Response': None,
              'Group': None,
              'Direction': None,
              'Age': None,
              'Block': None,
              'RT': None,
              'Colors': None,
              'ISI': None,
              'Early_resp': None,
              'Handedness': None,
              'Part_Nr': None}
        self.loc = loc_string

    
    def set_file(self):
        # Check Saving Location Directory
        data_dir = os.path.abspath(self.loc + '/data/') # just in case the absolute path is required
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
        #create a text file to save data
        self.fileName = data_dir + '/RDM_PD' + 'participantX' + '_today' + '.csv'
        cnt = 0

        #Make sure we do not overwrite our data
        while os.path.exists(self.fileName):
            cnt += 1
            self.fileName = data_dir + '/RDM_PD' + 'participantX' + '_today' + '_v' + str(cnt) + '.csv'

        # Get the Fieldnames
        self.fnames = list(self.trial_dict.keys()) 
        # write a file
        self.dataFile = open(self.fileName, 'w')  # a simple text file with 'comma-separated-values'
        self.writer = csv.DictWriter(self.dataFile, fieldnames = self.fnames)
        self.writer.writeheader()
        
    def finish(self):
        self.dataFile.close()
    
    def start(self):
        self.dataFile = open(self.fileName, 'a') 
        self.writer = csv.DictWriter(self.dataFile,  fieldnames = self.fnames)

    
    def update(self, trl_info):
        for item in trl_info.items():
            self.trial_dict[item[0]] = item[1]
        self.writer.writerow(self.trial_dict)
        

#%% Test
    
save_path =  '/home/jules/Dropbox/PhD_Thesis/DecisionMakingAndLearningStudy/Experiment/Development' 
wrt = task_writer(save_path)
# Initialize file
wrt.set_file()

# Update file
new_dict = {'Condition': 'AB', 'Age':22}
wrt.update(new_dict)
wrt.finish()
wrt.start()
wrt.update(new_dict)
wrt.finish()