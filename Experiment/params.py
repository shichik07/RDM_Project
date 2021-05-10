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
ALG =  'BM' #'MN'
DOT_SPEED = 8
DOT_SIZE = 0.2
#Number of dots
if ALG == 'MN':
    DOT_N = 20
else:
    DOT_N = 60

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

# INSTRUCTIONS PRACTICE

INTRO = (
    u'Willkommen bei unserem Experiment.', 
    u'Ziel unseres Experiments ist es ein besseres Verständnis wie das Gehirn Entscheidungen trifft.',
    u'Das Experiment besteht aus zwei Teilen, die jeweils ungefähr 15 Minuten in Anspruch nehmen.'
    u'Ihre Aufgabe ist es in diesem Experiment einfache visuelle Entscheidungen treffen.',
    u'Dabei werden Sie sich scheinbar zufällig bewegende Punkte auf dem Bildschirm sehen.',
    u'Sie müssen bestimmen ob sich diese Punkte jeweils mehrheitlich nach Links oder nach Rechts bewegen.',
    u'Die Punkte können dabei einfarbig sein, aber auch zwei verschiedene Farben haben.',
    u'In jedem der beiden Teile des Experiments kommt einer Farbe hierbei eine besondere Bedeutung zu, die Sie vorher lernen.',
    u'Um mit dem ersten Teil des Experiments zu beginnen, drücken Sie bitte die Leertaste.'
    )

PRACTICE_FULL_1 = (
    u'In diesem Teil des Experiments sehen Sie zunächst nur Punkte in einer Farbe die sich mehrheitlich in eine Richtung bewegen',
    u'Wenn sich die Punkte mehrheitlich nach links bewegen, drücken Sie bitte die linke Pfeiltaste, andernfalls die Rechte Pfeiltaste.',
    u'Bitte seien Sie so genau wie möglich und antworten Sie innerhalb von drei Sekunden.',
    u'Um fortzfahren und den ersten Übungsteil zu beginnen, drücken Sie bitte die Leertaste.')
    
PRACTICE_FULL_2 = (
    u'Sehr gut gemacht! Sie haben den zweiten Teil der Übung erreicht.', 
    u'In diesem Teil des Experiments sehen Sie Punkte in verschiedenen Farben.',
    u'Punkte in grüner Farbe bewegen sich IMMER mehrheitlich in eine Richtung.',
    u'Bei allen anderen Farbkombinationen bewegen sich gleich viele Punkte in eine Richtung.',
    u'Um bestmöglich zu antworten ist es deshalb wichtig sich nur auf die grüngefärbten Punkte zu fokussieren',
    u'Um fortzufahren und den zweiten Übungsteil zu beginnen, drücken Sie bitte die Leertaste.')
    
EXP_FULL =(
    u'Sehr gut gemacht! Im folgenden startet der erste von vier Experimentellen Blöcken.',
    u'Vom Ablauf her ändert sich nichts. Bitte fokussieren Sie sich wie bisher immer separat auf die Grünen Punkte',
    u'Um fortzufahren und den zweiten Übungsteil zu beginnen, drücken Sie bitte die Leertaste.')

PRACTICE_PART_1 = (
    u'In diesem Teil des Experiments sehen Sie zunächst Punkte in grüner und blauer Farbe',
    u'Nur eine der Farben bewegt sich mehrheitlich in eine Richtung.',
    u'Ihre Aufgabe wird es sein zu bestimmen ob sich die grünen oder die blauen Punkte mehrheitlich bewegen',
    u'Wenn sich die grünen Punkte mehrheitlich bewegen, drücken Sie bitte die "1", bei den blauen die "2"',
    u'Bitte seien Sie so genau wie möglich und antworten Sie innerhalb von drei Sekunden.',
    u'Um fortzufahren und den ersten Übungsteil zu beginnen, drücken Sie bitte die Leertaste.')
    
PRACTICE_PART_2 = (
    u'Sehr gut gemacht! Sie haben den zweiten Teil der Übung erreicht.', 
    u'In diesem Teil des Experiments sehen Sie Punkte in verschiedenen Farbkombinationen.',
    u'Sehen Sie Punkte in blauer Farbe bewegt sich eine Gruppe immer mehrheitlich in eine Richtung.',
    u'Bei allen anderen Farbkombinationen bewegen sich gleich viele Punkte in eine Richtung.',
    u'Sollten sie Punkte in blauer Farbe sehen, identifizieren Sie zuerst welche Punkte sich Mehrheitlich bewegen ...',
    u'und geben Sie die Richtung der Bewegung an.'
    u'Wenn sich die Punkte mehrheitlich nach links bewegen, drücken Sie bitte die linke Pfeiltaste, andernfalls die Rechte Pfeiltaste.',
    u'Um fortzfahren und den zweiten Übungsteil zu beginnen, drücken Sie bitte die Leertaste.')
    
EXP_PART =(
    u'Sehr gut gemacht! Im folgenden startet der erste von vier Experimentellen Blöcken.',
    u'Vom Ablauf her ändert sich nichts. Wenn Sie blaue Punkte sehen, fokussieren Sie sich bitte wie bisher auf eine der Gruppen.',
    u'Um fortzufahren und den zweiten Übungsteil zu beginnen, drücken Sie bitte die Leertaste.')

BLOCK_INSTR= (
    u'Sie haben das Ende des Blocks erreicht. Um mit dem nächsten Block fortzufahren, drücken Sie bitte die Leertaste.'
    )

END = (
       u'Sie haben das Ende des Experiments erreicht. Vielen Dank für Ihre Teilnahme!'       
       )

PRACTICE_FULL = [PRACTICE_FULL_1, PRACTICE_FULL_2]
PRACTICE_PART = [PRACTICE_PART_1, PRACTICE_PART_2]