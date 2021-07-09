#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 15:00:21 2021

@author: jules
"""


import numpy as np
'Define Parameter for the Experiment'

# DISPLAY PARAMS
PIX_SIZE = [1920,1080]
WIDTH = 31
DISTANCE = 60
UNITS = 'deg'
BG_COLOR = [-1,-1,-1]
REFRESH = 61

# DOT PARAMS
FIELD_SIZE = 5.0 # Field size for the array object
ALG =  'BM' #'MN'
DOT_SPEED = 1.5 #used to be 8
DOT_SIZE = 0.2
DOT_DENSITY = 16.7 
FIELD_SIZE_DOT = [10.4, 10.4]  # #[14.8, 14.8] Field Size for the DOt Updates
CENTER = [0,0]
GROUP_NR = 2 #default, cannot be modified yet
JITTER_UPDATE = 2 # on which frames updates occur




#Number of dots
if ALG == 'MN':
    DOT_N = int(np.ceil(DOT_DENSITY*np.square(FIELD_SIZE_DOT [0])/REFRESH))/3 #workaround
else:
    DOT_N = int(np.ceil(DOT_DENSITY*np.square(FIELD_SIZE_DOT [0])/REFRESH))

# Colors of all dot Groups and luminance matching 
green = [85,188,75]
blue = [81, 186, 255]
red = [255, 121, 81]
yellow =[214,165,0]
#DOT_G_COL = [[ 1,1,1],[ 1,1,1]], [[ 0.9,-1,-1],[-0.73,0,1]], [[ 0.9,-1,-1],[-0.73,0,1]], [[ 0.9,-1,-1],[-0.73,0,1]]
DOT_G_COL = [blue, blue], [blue, yellow], [blue, red], [blue, green]
PRTC_FULL_COL = [green, green]
BASE_COL = blue # color against which other colors are compared
LUM_METHOD = 'flicker' # Luminance matchin method, either "flicker" or 'min_mo' 


green_hsv = [115, 0.6, 0.7]
blue_hsv = [204, 0.68, 1]
yellow_hsv = [46, 1, 0.83]
red_hsv = [14, 0.68, 0.8]
DOT_G_COL_hsv = [blue_hsv, blue_hsv], [blue_hsv, yellow_hsv], [blue_hsv, red_hsv], [blue_hsv, green_hsv]
BASE_COL_hsv = blue_hsv

# CUE PARAMS
CUE_FRAMES = round(0.4*REFRESH)
CUE_ORI =  [0.0,90.0]
GRATE_SIZE = [4,4]
GRATE_CONT = 1
CIRCLE_COL = [0, 0, 0]


# TRIAL PARAMS
TIME_TO_RESP = 2.5 #2.5 seconds
INTERSTIMI= [0.8,1.2]
FRAMES = 120 # used to be 30 (0.5) seconds
RESPONSE_KEYS = ['left', 'right']
NUMBER_KEYS = ['1','2']
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
COHERENCE = [0.0, 4/30, 6/30, 8/30]#[0.0, 2/30, 4/30, 0.3] # Note: we can use
PROPORTION = [0.0, 2.0] #[0.2, 1.8]
TASK_NR = 40 # defined with respect to each coherence level
PRACTICE_NR = 32 # defined with respect to each total tiral nr per practice part

# TEXT PARAMS
TEXT_COL = [1,1,1]

# INSTRUCTIONS PRACTICE

INTRO = (
    u'Willkommen bei unserem Experiment.', 
    u'Ziel unseres Experiments ist es ein besseres Verständnis wie das Gehirn Entscheidungen trifft.',
    u'Das Experiment besteht aus zwei Teilen, die jeweils ungefähr 20 Minuten in Anspruch nehmen.',
    u'Ihre Aufgabe ist es in diesem Experiment einfache visuelle Entscheidungen treffen.',
    u'Dabei werden Sie sich scheinbar zufällig bewegende Punkte auf dem Bildschirm sehen.',
    u'Die Punkte können dabei unterschiedliche Farben haben (z.B. nur blau, oder grün und rot)',
    u'Sie müssen bestimmen ob sich diese Punkte insgesamt jeweils mehrheitlich nach Links oder nach Rechts bewegen.',
    u'Dafür werden Sie die Punkte für ca. eine halbe Sekunde beobachten können und haben anschließend zwei Sekund um Ihre Antwort zu geben.',
    u'In jedem der beiden Teile des Experiments kommt einer Farbe hierbei eine besondere Bedeutung zu, die Sie vorher lernen.',
    u'Um mit dem ersten Teil des Experiments zu beginnen, drücken Sie bitte die Leertaste.'
    )

PRACTICE_FULL_1 = (
    u'In diesem Teil des Experiments sehen Sie zunächst nur Punkte in einer Farbe die sich mehrheitlich in eine Richtung bewegen',
    u'Wenn sich die Punkte mehrheitlich nach links bewegen, drücken Sie bitte die linke Pfeiltaste, andernfalls die Rechte Pfeiltaste.',
    u'Bitte seien Sie so genau wie möglich und antworten Sie innerhalb von drei Sekunden.',
    u'Achtung! Die Aufgabe ist sehr schwierig zu beantworten und dazu konzipiert das Sie Fehler machen.',
    u'Lassen Sie sich davon nicht beeinflussen und versuchen Sie in jedem Versuch intuitiv die Richtung der Bewegung zu schätzen.',
    u'Um fortzufahren und den ersten Übungsteil zu beginnen, drücken Sie bitte die Leertaste.')
    
PRACTICE_FULL_2 = (
    u'Sehr gut gemacht! Sie haben den zweiten Teil der Übung erreicht.', 
    u'In diesem Teil des Experiments sehen Sie Punkte in verschiedenen Farben.',
    u'Punkte in grüner Farbe bewegen sich IMMER mehrheitlich in eine Richtung.',
    u'Bei allen anderen Farbkombinationen bewegen sich gleich viele Punkte in eine Richtung.',
    u'Um bestmöglich zu antworten ist es deshalb wichtig sich nur auf die grüngefärbten Punkte zu fokussieren.',
    u'Das heißt, fokussieren Sie sich nur auf die grün gefärbten Punkte um Ihre Antwort zu geben und ignorieren Sie die anderen.',
    u'Wenn sich die Punkte mehrheitlich nach links bewegen, drücken Sie bitte die linke Pfeiltaste, andernfalls die rechte Pfeiltaste.',
    u'Um fortzufahren und den zweiten Übungsteil zu beginnen, drücken Sie bitte die Leertaste.')
    
EXP_FULL =(
    u'Sehr gut gemacht! Im folgenden startet der erste von vier Experimentellen Blöcken.',
    u'Vom Ablauf her ändert sich nichts.',
    u'Wenn Sie grüne Punkte sehen fokussieren Sie sich bitte wie bisher ausschließlich auf diese.',
    u'Bei allen anderen Farben/Farbkombinationen geben Sie wie bisher die mehrheitliche Richtung der Bewegung an.',
    u'Um fortzufahren und den zweiten Übungsteil zu beginnen, drücken Sie bitte die Leertaste.',
    u'ACHTUNG folgend beginnt automatisch der erste Aufgabenblock.')

PRACTICE_PART_1 = (
    u'In diesem Teil des Experiments sehen Sie zunächst Punkte in blauer und roter Farbe',
    u'Nur eine der Farben bewegt sich mehrheitlich in eine Richtung.',
    u'Ihre Aufgabe ist es zu bestimmen in welche Richtung sich die blauen oder die roten Punkte mehrheitlich bewegen',
    u'Wenn sich die Punkte mehrheitlich nach links bewegen, drücken Sie bitte die linke Pfeiltaste, andernfalls die rechte Pfeiltaste.',
    u'Bitte seien Sie so genau wie möglich und antworten Sie innerhalb von drei Sekunden.',
    u'Um fortzufahren und den ersten Übungsteil zu beginnen, drücken Sie bitte die Leertaste.')
    
PRACTICE_PART_2 = (
    u'Sehr gut gemacht! Sie haben den zweiten Teil der Übung erreicht.', 
    u'In diesem Teil des Experiments sehen Sie Punkte in verschiedenen Farbkombinationen.',
    u'Sehen Sie Punkte in roter Farbe bewegt sich eine Gruppe immer mehrheitlich in eine Richtung.',
    u'Bei allen anderen Farbkombinationen bewegen sich gleich viele Punkte in eine Richtung.',
    u'Wenn sich die Punkte mehrheitlich nach links bewegen, drücken Sie bitte die linke Pfeiltaste, andernfalls die Rechte Pfeiltaste.',
    u'Um fortzfahren und den zweiten Übungsteil zu beginnen, drücken Sie bitte die Leertaste.')
    
EXP_PART =(
    u'Sehr gut gemacht! Im folgenden startet der erste von vier Experimentellen Blöcken.',
    u'Vom Ablauf her ändert sich nichts.',
    u'Wenn sich die Punkte mehrheitlich nach links bewegen, drücken Sie bitte die linke Pfeiltaste, andernfalls die Rechte Pfeiltaste.',
    u'Um fortzufahren und den zweiten Übungsteil zu beginnen, drücken Sie bitte die Leertaste.',
    u'ACHTUNG folgend beginnt automatisch der erste Aufgabenblock.')

BLOCK_INSTR= (
    u'Sie haben das Ende des Blocks erreicht. Um mit dem nächsten Block fortzufahren, drücken Sie bitte die Leertaste.',
     u'ACHTUNG folgend beginnt automatisch der nächste Aufgabenblock.'
    )

END = (
       u'Sie haben das Ende des Experiments erreicht. Vielen Dank für Ihre Teilnahme!'       
       )

PRACTICE_FULL = [PRACTICE_FULL_1, PRACTICE_FULL_2]
PRACTICE_PART = [PRACTICE_PART_1, PRACTICE_PART_2]