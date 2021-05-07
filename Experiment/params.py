#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 15:00:21 2021

@author: jules
"""



'Define Parameter for the Experiment'

# DISPLAY PARAMS
PIX_SIZE = [1920,1080]
WIDTH = 31
DISTANCE = 60
UNITS = 'deg'
BG_COLOR = [-1,-1,-1]
REFRESH = 60

# DOT PARAMS
FIELD_SIZE = 5.0
ALG =  'MN'
DOT_SPEED = 8
DOT_SIZE = 0.2
# Colors of all dot Groups
green = [85,188,75]
blue = [81, 186, 255]
red = [255, 121, 81]
yellow =[214,165,0]
#DOT_G_COL = [[ 1,1,1],[ 1,1,1]], [[ 0.9,-1,-1],[-0.73,0,1]], [[ 0.9,-1,-1],[-0.73,0,1]], [[ 0.9,-1,-1],[-0.73,0,1]]
DOT_G_COL = [blue, blue], [blue, yellow], [blue, red], [blue, green]
PRTC_FULL_COL = [green, green]


# 'dot_density': 16.7, 
# 'fieldsize' = [14.6, 14.6], 
# 'center' = [0,0],  
# 'groups' = 2,
# 't_group' = 1,
# 'rgbs' = [[ -1,0,1],[ 1,0,1]] 
# 'frameRate' = 61)

# CUE PARAMS
CUE_FRAMES = round(0.4*REFRESH)
CUE_ORI =  [0.0,90.0]
GRATE_SIZE = [4,4]
GRATE_CONT = 1
CIRCLE_COL = [0, 0, 0]


# TRIAL PARAMS
INTERSTIMI= [0.8,1.2]
FRAMES = 180
RESPONSE_KEYS = ['left', 'right']
CONTINUE_KEYS = ['return', 'space']
QUIT_KEY = ['escape']
GUI_INP = {'ProbandenNr':'', 
           'Geschlecht':['männlich','weiblich','divers'],
            'Alter': '' , 
            'Händikeit': ['Links', 'Rechts'], 
            'Gruppe (für Experimentatorin)': ['PD', 'HC', 'PI']}

# ITEM PARAMS 
EXP_CON = ['Mono', 'Di_null', 'Di_part', 'Di_full']
BLOCK_NRS = [0,1,2,3]
COHERENCE = [0.0, 0.1, 0.2, 0.5]
PROPORTION = [0.2, 1.8]
TASK_NR = 40 # defined with respect to each coherence level
PRACTICE_NR = 32 # defined with respect to each total tiral nr per practice part

# TEXT PARAMS
TEXT_COL = [1,1,1]

# INSTRUCTIONS PRATICE