#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 16:16:21 2021

@author: Julius Kricheldorff

Trigger Code Scheme:

# Practice Triggers
Practice Start: 200
Practice End: 201
    
# Block Triggers
Start Block: 1:8
End Block: 11:18

# Onset Fixation
Fixation Onset: 20

# Trial Onset by condition
Mono_info_onset: 31:34 - by coherence low to high
Null_info_onset: 41:44 - by coherence low to high
Part_info_onset: 51:54 - by coherence low to high
Full_info_onset: 61:64 - by coherence low to high

# Correct Response by condition
Mono_info_correct: 131:134 - by coherence low to high
Null_info_correct: 141:144 - by coherence low to high
Part_info_correct: 151:154 - by coherence low to high
Full_info_correct: 161:164 - by coherence low to high

# False Response by condition
Mono_info_false: 135:138 - by coherence low to high
Null_info_false: 145:148 - by coherence low to high
Part_info_false: 155:158 - by coherence low to high
Full_info_false: 165:168 - by coherence low to high

# No response by condition
Mono_info_none: 139 - no resp
Null_info_none: 149 - no resp
Part_info_none: 159 - no resp
Full_info_none: 169 - no resp
"""


#from psychopy import parallel

class eeg_com():
    '''
    Class to communicate with recodring PC for Brain Products EEG System. Trigger are send via the parallel port
    '''
    def __init__(self, conditions, coherence_vals,  port_adress = 0x378):
        '''
        Function to set parameter relevant to access port and convert trial information to trigger codes
        ----------
        
        
        Parameters
        ----------
        
        conditions: list - list of strings containing the condition names
        coherence_vals: list - list of floats containing possible coherence values
        port_adress: int - paralel port adress
        
        Returns
        -------
        
        '''
        self.port = port_adress
        self.con_list = conditions # list of experimental conditions CAREFUL! Ordered!
        self.coh_list  = [round(num, 2) for num in coherence_vals] # rounded coherence values
        
    def init_port(self):
        '''
        Function to initialize parallel port
        ----------
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        '''
        try:
            from ctypes import windll
            global io, parallel_port
            io = windll.dlportio # requires dlportio.dll !!!
            parallel_port = self.port
        except:
            print('The parallel port couldn\'t be opened')

    def practice_start_trigger(self):
        '''
        Function to send a trigger at the beginning of a practice block
        ----------
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        '''
        prac = 200
        # First a zero trigger to reset ports
        try:
            io.DlPortWritePortUchar(self.port, 0)
        except:
            print('Failed to send zero trigger')
        #self.sleep(2)
        
        # start recording
        try: 
            io.DlPortWritePortUchar(self.port, 254)
            print('Recording started')
        except:
            print('Recording could not start')
        #self.sleep(2)
        #io.DlPortWritePortUchar(port, 0) # not sure why this is here?
        
        # Block Trigger
        try:
            io.DlPortWritePortUchar(self.port, prac)
            print(' Trigger number',  prac, ' : Block started')
        except:
            print('Failed to send trigger')
        #io.DlPortWritePortUchar(port, 0) # not sure why this is here?
        
    def practice_end_trigger(self):
        '''
        Function to send a trigger at the end of a practice block
        ----------
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        '''
        prac = 201
        # First a zero trigger to reset ports
        try:
            io.DlPortWritePortUchar(self.port, 0)
        except:
            print('Failed to send zero trigger')
        #self.sleep(2)
        
        # start recording
        try: 
            io.DlPortWritePortUchar(self.port, 254)
            print('Recording started')
        except:
            print('Recording could not start')
        #self.sleep(2)
        #io.DlPortWritePortUchar(port, 0) # not sure why this is here?
        
        # Block Trigger
        try:
            io.DlPortWritePortUchar(self.port, prac)
            print(' Trigger number',  prac, ' : Block started')
        except:
            print('Failed to send trigger')
        #io.DlPortWritePortUchar(port, 0) # not sure why this is here?
        
    def block_start_trigger(self, block_nr):
        '''
        Function to send a trigger at the beginning of a block
        ----------
        
        
        Parameters
        ----------
        block_nr: int - number of current block
        
        
        Returns
        -------
        
        '''
        # First a zero trigger to reset ports
        try:
            io.DlPortWritePortUchar(self.port, 0)
        except:
            print('Failed to send zero trigger')
        #self.sleep(2)
        
        # start recording
        try: 
            io.DlPortWritePortUchar(self.port, 254)
            print('Recording started')
        except:
            print('Recording could not start')
        #self.sleep(2)
        #io.DlPortWritePortUchar(port, 0) # not sure why this is here?
        
        # Block Trigger
        try:
            io.DlPortWritePortUchar(self.port, block_nr)
            print(' Trigger number', block_nr, ' : Block started')
        except:
            print('Failed to send trigger')
        #io.DlPortWritePortUchar(port, 0) # not sure why this is here?
        
    def block_end_trigger(self, block_nr):
        '''
        Function to send a trigger at the end of a block
        ----------
        
        
        Parameters
        ----------
        block_nr: int - number of current block
        
        
        Returns
        -------
        
        '''
        # First a zero trigger to reset ports
        try:
            io.DlPortWritePortUchar(self.port, 0)
        except:
            print('Failed to send zero trigger')
        #self.sleep(2)
        
        # end recording
        try: 
            io.DlPortWritePortUchar(self.port, 255)
            print('Recording ended')
        except:
            print('Recording could not end')
        #self.sleep(2)
        #io.DlPortWritePortUchar(port, 0) # not sure why this is here?
        
        # Block Trigger
        try:
            io.DlPortWritePortUchar(self.port, block_nr)
            print(' Trigger number', block_nr, ' : Block started')
        except:
            print('Failed to send trigger')
        #io.DlPortWritePortUchar(port, 0) # not sure why this is here?
        
    def onset_trigger(self,  Condition, Coherence):
        '''
        Function to send appropriate exp stim onset trigger
        ----------
        
        
        Parameters
        ----------
        Condition: str - number of current block
        Coherence: float - valid coherence values in this task
        
        
        Returns
        -------
        
        '''
        code = self.trial_to_code(Condition, Coherence)
        try:
            io.DlPortWritePortUchar(self.port, code)
            print(' Trigger number', code, ' : Dots displayed')
        except:
            print('Failed to send trigger')
        #io.DlPortWritePortUchar(port, 0) # not sure why this is here?
        
    def fixation_trigger(self):
        '''
        Function to send a trigger at the onset of presenting a fixation cross
        ----------
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        '''
        # Fixation Onset Trigger
        fix = 20
        try:
            io.DlPortWritePortUchar(self.port, fix)
            print(' Trigger number', fix, ' : Fixation Presented')
        except:
            print('Failed to send trigger')
        #io.DlPortWritePortUchar(port, 0) # not sure why this is here?
    
    def response_trigger(self, Condition, Coherence, Response):
        '''
        Function to send appropriate response triggers
        ----------
        
        
        Parameters
        ----------
        Condition: str - number of current block
        Coherence: float - valid coherence values in this task
        Response: str|NoneType - Either correct or incorrect response or None 
        if no response was given within time interval
        
        
        Returns
        -------
        
        '''
        code = self.trial_to_code(Condition, Coherence, Response)
        # Response Trigger
        try:
            io.DlPortWritePortUchar(self.port, code)
            print(' Trigger number', code, ' : Response Recorded')
        except:
            print('Failed to send trigger')
        #io.DlPortWritePortUchar(port, 0) # not sure why this is here?
        
    
        
    def trial_to_code(self, Condition, Coherence, *Response):
        '''
        Function to translate trial information to a trigger code
        ----------
        
        
        Parameters
        ----------
        Condition: str - number of current block
        Coherence: float - valid coherence values in this task
        Response: str|NoneType - Either correct or incorrect response or None 
        if no response was given within time interval
        
        
        Returns
        -------
        code: int - trigger code with trial information
        
        '''
        
        Con_num = self.con_list.index(Condition)*10 + 30 
        Coh_num = self.coh_list.index(Coherence) + 1 
        if Response:
            base = 100
            if Response[0] == 0:
                Coh_num = 4 + Coh_num
            elif Response[0] == None:
                Coh_num = 9    
        else:
            base = 0
        code = base + Con_num + Coh_num
        return code
            
            