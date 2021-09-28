#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 16:16:21 2021

@author: jules
"""

from psychopy import parallel


class eeg_com():
    def __init__(self, port_adress = 0x378):
        self.port = port_adress
        
    def init_port(self):
        try:
            from ctypes import windll
            global io, parallel_port
            io = windll.dlportio # requires dlportio.dll !!!
            parallel_port = self.port
        except:
            print('The parallel port couldn\'t be opened')

        
    def block_trigger(self, block_nr):
        # First a zero trigger to reset ports
        try:
            io.DlPortWritePortUchar(self.port, 0)
        except:
            print('Failed to send zero trigger')
        self.sleep(2)
        
        # start recording
        try: 
            io.DlPortWritePortUchar(self.port, 254)
            print('Recording started')
        except:
            print('Recording did not start')
        self.sleep(2)
        #io.DlPortWritePortUchar(port, 0) # not sure why this is here?
        
        # Block Trigger
        try:
            io.DlPortWritePortUchar(self.port, block_nr)
            print(' Trigger number', block_nr, ' : Block started')
        except:
            print('Failed to send trigger')
        #io.DlPortWritePortUchar(port, 0) # not sure why this is here?
            
        
        
       