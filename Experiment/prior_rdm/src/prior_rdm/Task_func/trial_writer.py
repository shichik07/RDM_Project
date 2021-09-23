#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 12:51:38 2021

@author: jules
"""
import csv, os

class task_writer():
    '''
    Class to write trial information into a csv file - inspired by the Psychopy tutorial of
    tutorial by Jonas K. Lindelov
    ('https://lindeloev.net/psychopy-course/past-courses/cml-seminar-2018/')
    
    '''
    def __init__(self, loc_string, trl_dct):
        '''
        Function with parameters to initialize csv file.
        ----------
        
        
        Parameters
        ----------
        
        loc_string: str - string with the location where trial information is to be saved
        trl_dct: dict - dictionary setup including headers fol types of information that are to be saved
        
        
        Returns
        -------
        
        '''
        self.trial_dict = trl_dct
        self.loc = loc_string

    
    def set_file(self):
        '''
        Function to initialize csv file. Creates a new file and checks if a similar version already exists.
        In that case creates another to make sure no data is overwritten
        ----------
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        '''
        
        # Check Saving Location Directory
        data_dir = os.path.abspath(self.loc + '/data/') # just in case the absolute path is required
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
        #create a text file to save data
        self.fileName = data_dir + '/RDM_PD' + 'participant_' + self.trial_dict['Part_Nr']  + '.csv'
        cnt = 0

        #Make sure we do not overwrite our data
        while os.path.exists(self.fileName):
            cnt += 1
            self.fileName = data_dir + '/RDM_PD' +'participant_' + self.trial_dict['Part_Nr'] + '_v' + str(cnt) + '.csv'

        # Get the Fieldnames
        self.fnames = list(self.trial_dict.keys()) 
        # write a file
        self.dataFile = open(self.fileName, 'w')  # a simple text file with 'comma-separated-values'
        self.writer = csv.DictWriter(self.dataFile, fieldnames = self.fnames)
        self.writer.writeheader()
        
    def finish(self):
        '''
        Function to close csv file for writing to make sure we do not lose our data
        ----------
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        '''
        self.dataFile.close()
    
    def start(self):
        '''
        Function to open csv file for writing
        ----------
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        '''
        self.dataFile = open(self.fileName, 'a') 
        self.writer = csv.DictWriter(self.dataFile,  fieldnames = self.fnames)

    
    def update(self, trl_info):
        '''
        Function to write new trial information into our csv file
        ---------
        
        Parameters
        ----------
        
        trl_info: dict - dictionary containing information of trial to be written into csv file
        
        
        Returns
        -------
        
        '''
        for item in trl_info.items():
            self.trial_dict[item[0]] = item[1]
        self.writer.writerow(self.trial_dict)