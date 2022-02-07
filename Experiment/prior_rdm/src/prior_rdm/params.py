#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 15:00:21 2021

@author: jules
"""
#test

import numpy as np
from psychopy import monitors,visual
'Define Parameter for the Experiment'

# DISPLAY PARAMS
PIX_SIZE = [1920,1080]
WIDTH = 31
DISTANCE = 60
UNITS = 'deg'
BG_COLOR = [-1,-1,-1]
REFRESH = 61
EEG_OPT = False
PORT = 16344
SAVE_PATH =  '/home/jules/Dropbox/PhD_Thesis/DecisionMakingAndLearningStudy/Experiment/Development' 
RANDOMSEED = 1487
LIST_MAX_NR = 100


# DOT PARAMS
FIELD_SIZE = 5.0 # Field size for the array object
ALG =  'BM' #'MN'
DOT_SPEED = 1 #used to be 8
DOT_SIZE = 0.2
DOT_DENSITY = 16.7 # initially tried with 16.7 as shadlen etc, but the higher refresh rate the larger the aperture size 
FIELD_SIZE_DOT = [10.4, 10.4]  # #[14.8, 14.8] Field Size for the DOt Updates
CENTER = [0,0]
GROUP_NR = 2 #default, cannot be modified yet
JITTER_UPDATE = 2 # on which frames updates occur
DOT_N = 30

#FLICKERPHOTOMETRY PARAMS
WIDTH_PHOTO = 0.5
HEIGHT_PHOTO = 6.0
BAR_POS = [5,0]
RADIUS = 150
TARGET_FREQ = 30 #Hz
UPDATE_FLICKER = int(round(REFRESH/TARGET_FREQ/2)) 

# Experiment Objects
MY_MONITOR = monitors.Monitor(name='DellXPS15_screen')
MY_MONITOR.setSizePix(PIX_SIZE)
MY_MONITOR.setWidth(WIDTH)
MY_MONITOR.setDistance(DISTANCE)
MY_MONITOR.saveMon()

# win = visual.Window(size = PIX_SIZE,
#      monitor = "DellXPS15_screen",
#      units=UNITS,
#      fullscr=True, # change to fullscreen later
#      color=BG_COLOR, 
#  ) 

#Number of dots
# if ALG == 'MN':
#     DOT_N = int(np.ceil(DOT_DENSITY*np.square(FIELD_SIZE_DOT [0])/REFRESH))/3 #workaround
# else:
#     DOT_N = int(np.ceil(DOT_DENSITY*np.square(FIELD_SIZE_DOT [0])/REFRESH))

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

#green_hsv = [115, 0.6, 0.7]
green_hsv = [109,0.64,0.58]
#blue_hsv = [204, 0.68, 1]
blue_hsv = [211,0.62,0.78]
#yellow_hsv = [46, 1, 0.83]
yellow_hsv = [42,0.87,0.66]
#red_hsv = [14, 0.68, 0.8]
red_hsv = [359,0.46,0.77]
DOT_G_COL_hsv = [blue_hsv, blue_hsv], [blue_hsv, yellow_hsv], [blue_hsv, red_hsv], [blue_hsv, green_hsv]
BASE_COL_hsv = blue_hsv

# TRIAL PARAMS
TIME_TO_RESP = 0.5 # Time to respond after stimuli display - to catch slow responses eventually
INTERSTIMI= [1,1.4] # fixation duration
FRAMES = int(2.5*REFRESH) # used to be 30 (0.5) seconds
RESPONSE_KEYS = ['left', 'right']
NUMBER_KEYS = ['1','2']
COLOR_KEYS =['up','down']
CONTINUE_KEYS = ['return', 'space', 'escape']
QUIT_KEY = ['escape']
GUI_INP = {'ProbandenNr':'', 
           'Geschlecht':['männlich','weiblich','divers'],
            'Alter': '' , 
            'Händikeit': ['Links', 'Rechts'], 
            'Gruppe (für Experimentatorin)': ['PD', 'HC', 'PI']}


# ITEM PARAMS 
EXP_CON = ['Mono', 'Di_null', 'Di_part', 'Di_full']
BLOCK_NRS = [0,1,2,3]
BLOCK_NRS_SHORT = [0,1,2,3,4,5,6,7] # for the new short version
COHERENCE = [0.0, 2/30, 4/30, 10/30]#[0.0, 2/30, 4/30, 0.3] # Note: we can use
PROPORTION = [0.0, 2.0] #[0.2, 1.8]
TASK_NR =48 # defined with respect to each coherence level
PRACTICE_NR = 32 # defined with respect to each total tiral nr per practice part

# TEXT PARAMS
TEXT_COL = [1,1,1]

# INSTRUCTIONS PRACTICE

INST_FLICKER = (
    u'Bevor das Experiment beginnt müssen wir die in dem Experiment gezeigten Farben in ihrer Leuchtkraft anpassen.',
    u'Um das zu erreichen, brauchen wir Ihre Unterstützung.',
    u'Sie werden gleich die Darstellung eines flackernden Kreises sehen und daneben einen Balken.',
    u'Der Balken gibt die relative Helligkeit in Prozent an.',
    u'Mittels der Pfeiltasten "oben" und "unten" können Sie die Helligkeit anpassen.',
    u'Bitte varieren Sie die Helligkeit so lange bis das Flackern des Kreises annähernd verschwindet.',
    u'Sind sie zufrieden mit Ihrer Auswahl bestätigen Sie jeweils mit der Eingabe/Enter Taste.',
    u'Es folgt die nächste Farbe (insgesamt dreimal), bevor im Anschluss das Experiment beginnt.',
    u'Um zu Beginnen drücken Sie bitte die Leertaste.')

INTRO = (
    u'Willkommen bei unserem Experiment.', 
    u'Ziel unseres Experiments ist es ein besseres Verständnis wie das Gehirn Entscheidungen trifft.',
    u'Das Experiment besteht aus zwei Teilen, die jeweils ungefähr 15 Minuten in Anspruch nehmen.',
    u'Ihre Aufgabe ist es in diesem Experiment einfache visuelle Entscheidungen treffen.',
    u'Dabei werden Sie sich scheinbar zufällig bewegende Punkte auf dem Bildschirm sehen.',
    u'Die Punkte können dabei unterschiedliche Farben haben (z.B. nur blau, oder grün und rot)',
    u'Sie müssen bestimmen ob sich diese Punkte insgesamt jeweils mehrheitlich nach Links oder nach Rechts bewegen.',
    u'Dafür werden Sie die Punkte für 2.5 Sekunden beobachten können und müssen in diesem Zeitraum Ihre Antwort geben.',
    u'In jedem der beiden Teile des Experiments kommt einer Farbe hierbei eine besondere Bedeutung zu, die Sie vorher lernen.',
    u'Um mit dem ersten Teil des Experiments zu beginnen, drücken Sie bitte die Leertaste.'
    )

PRACTICE_FULL_1 = (
    u'In diesem Teil des Experiments sehen Sie zunächst Punkte in blauer und grüner Farbe',
    u'Nur grüngefärbte Punkte bewegt sich FAST IMMER mehrheitlich in eine Richtung.',
    u'Ihre Aufgabe ist es zu bestimmen in welche Richtung sich die grünen Punkte mehrheitlich bewegen',
    u'Wenn sich die Punkte mehrheitlich nach links bewegen, drücken Sie bitte die linke Pfeiltaste, andernfalls die Rechte Pfeiltaste.',
    u'Bitte seien Sie so genau und so schnell wie möglich und antworten Sie innerhalb von 2.5 Sekunden.',
    u'Achtung! Die Aufgabe ist sehr schwierig zu beantworten und dazu konzipiert das Sie Fehler machen.',
    u'Lassen Sie sich davon nicht beeinflussen und versuchen Sie in jedem Versuch intuitiv die Richtung der Bewegung zu schätzen.',
    u'Um fortzufahren und den ersten Übungsteil zu beginnen, drücken Sie bitte die Leertaste.')
    
PRACTICE_FULL_2 = (
    u'Sehr gut gemacht! Sie haben den zweiten Teil der Übung erreicht.', 
    u'In diesem Teil des Experiments sehen Sie Punkte in verschiedenen Farben.',
    u'Punkte in grüner Farbe bewegen sich FAST IMMER mehrheitlich in eine Richtung.',
    u'Bei allen anderen Farbkombinationen bewegen sich gleich viele Punkte in eine Richtung.',
    u'Um bestmöglich zu antworten ist es deshalb wichtig sich nur auf die grüngefärbten Punkte zu fokussieren.',
    u'Das heißt, fokussieren Sie sich nur auf die grün gefärbten Punkte um Ihre Antwort zu geben und ignorieren Sie die anderen Punkte.',
    u'Sollten keine grüngefärbten Punkte gezeigt werden, geben Sie die Richtung an in die sich die Punkte mehrheitlich bewegen.', 
    u'Wenn sich die Punkte mehrheitlich nach links bewegen, drücken Sie bitte die linke Pfeiltaste, andernfalls die rechte Pfeiltaste.',
    u'Um fortzufahren und den zweiten Übungsteil zu beginnen, drücken Sie bitte die Leertaste.')
    
EXP_FULL =(
    u'Sehr gut gemacht! Im folgenden startet der erste von vier Experimentellen Blöcken.',
    u'Vom Ablauf her ändert sich nichts.',
    u'Wenn Sie grüne Punkte sehen fokussieren Sie sich bitte wie bisher ausschließlich auf diese.',
    u'Bei allen anderen Farben/Farbkombinationen geben Sie wie bisher die mehrheitliche Richtung der Bewegung an.',
    u'Um fortzufahren und mit dem Experiment zu beginnen, drücken Sie bitte die Leertaste.',
    u'ACHTUNG folgend beginnt automatisch der erste Aufgabenblock.')

INTRO_SHORT = (
    u'Willkommen bei unserem Experiment.', 
    u'Ziel unseres Experiments ist es ein besseres Verständnis wie das Gehirn Entscheidungen trifft.',
    u'Das Experiment wird insgesamt ungefähr 40 Minuten in Anspruch nehmen.',
    u'Ihre Aufgabe ist es in diesem Experiment einfache visuelle Entscheidungen treffen.',
    u'Dabei werden Sie sich scheinbar zufällig bewegende Punkte auf dem Bildschirm sehen.',
    u'Die Punkte können dabei unterschiedliche Farben haben (z.B. blau, oder grün und rot)',
    u'Sie müssen bestimmen ob sich diese Punkte insgesamt jeweils mehrheitlich nach Links oder nach Rechts bewegen.',
    u'Dafür werden Sie die Punkte für 2.5 Sekunden beobachten können und müssen in diesem Zeitraum Ihre Antwort geben.',
    u'In jedem der beiden Teile des Experiments kommt einer Farbe hierbei eine besondere Bedeutung zu, die Sie vorher lernen.',
    u'Bitte seien Sie bei Ihren Antworten so SCHNELL und so GENAU wie möglich.'
    u'Um mit dem ersten Teil des Experiments zu beginnen, drücken Sie bitte die Leertaste.'
    )

PRACTICE_FULL_1_SHORT = (
    u'In diesem Teil des Experiments sehen Sie zunächst Punkte in blauer und grüner Farbe',
    u'Nur grüngefärbte Punkte bewegt sich FAST IMMER mehrheitlich in eine Richtung.',
    u'Ihre Aufgabe ist es zu bestimmen in welche Richtung sich die grünen Punkte mehrheitlich bewegen',
    u'Wenn sich die Punkte mehrheitlich nach links bewegen, drücken Sie bitte die linke Pfeiltaste, andernfalls die Rechte Pfeiltaste.',
    u'Für Ihre Antwort haben SIe insgesamt 2.5 Sekunden.',
    u'Achtung! Die Aufgabe ist sehr schwierig zu beantworten und dazu konzipiert das Sie Fehler machen.',
    u'Lassen Sie sich davon nicht beeinflussen und versuchen Sie in jedem Versuch intuitiv die Richtung der Bewegung zu schätzen.',
    u'Bitte seien Sie bei Ihren Antworten so SCHNELL und so GENAU wie möglich.'
    u'Um fortzufahren und den ersten Übungsteil zu beginnen, drücken Sie bitte die Leertaste.')
    
PRACTICE_FULL_2_SHORT = (
    u'Sehr gut gemacht! Sie haben den zweiten Teil der Übung erreicht.', 
    u'In diesem Teil des Experiments sehen Sie Punkte in verschiedenen Farben.',
    u'Punkte in grüner Farbe bewegen sich FAST IMMER mehrheitlich in eine Richtung.',
    u'Bei allen anderen Farbkombinationen bewegen sich gleich viele Punkte in eine Richtung.',
    u'Um bestmöglich zu antworten ist es deshalb wichtig sich nur auf die grüngefärbten Punkte zu fokussieren.',
    u'Das heißt, fokussieren Sie sich nur auf die grün gefärbten Punkte um Ihre Antwort zu geben und ignorieren Sie die anderen Punkte.',
    u'Sollten keine grüngefärbten Punkte gezeigt werden, geben Sie die Richtung an in die sich die Punkte mehrheitlich bewegen.', 
    u'Wenn sich die Punkte mehrheitlich nach links bewegen, drücken Sie bitte die linke Pfeiltaste, andernfalls die rechte Pfeiltaste.',
    u'Bitte seien Sie bei Ihren Antworten so SCHNELL und so GENAU wie möglich.'
    u'Um fortzufahren und den zweiten Übungsteil zu beginnen, drücken Sie bitte die Leertaste.')
    
EXP_FULL_SHORT =(
    u'Sehr gut gemacht! Im folgenden startet der erste von acht Experimentellen Blöcken.',
    u'Vom Ablauf her ändert sich nichts.',
    u'Wenn Sie grüne Punkte sehen fokussieren Sie sich bitte wie bisher ausschließlich auf diese.',
    u'Bei allen anderen Farben/Farbkombinationen geben Sie wie bisher die mehrheitliche Richtung der Bewegung an.',
    u'Bitte seien Sie bei Ihren Antworten so SCHNELL und so GENAU wie möglich.'
    u'Um fortzufahren und mit dem Experiment zu beginnen, drücken Sie bitte die Leertaste.',
    u'ACHTUNG folgend beginnt automatisch der erste Aufgabenblock.')

PRACTICE_PART_1 = (
    u'In diesem Teil des Experiments sehen Sie zunächst Punkte in blauer und roter Farbe',
    u'Nur eine der Farben bewegt sich mehrheitlich in eine Richtung.',
    u'Ihre Aufgabe ist es zu bestimmen in welche Richtung sich die blauen oder die roten Punkte mehrheitlich bewegen',
    u'Wenn sich die Punkte mehrheitlich nach links bewegen, drücken Sie bitte die linke Pfeiltaste, andernfalls die rechte Pfeiltaste.',
    u'Bitte seien Sie so genau und so schnell wie möglich und antworten Sie innerhalb von 2.5 Sekunden.',
    u'Achtung! Die Aufgabe ist sehr schwierig zu beantworten und dazu konzipiert das Sie Fehler machen.',
    u'Lassen Sie sich davon nicht beeinflussen und versuchen Sie in jedem Versuch intuitiv die Richtung der Bewegung zu schätzen.',
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
    u'Um fortzufahren und den dem dem Experiment zu beginnen, drücken Sie bitte die Leertaste.',
    u'ACHTUNG folgend beginnt automatisch der erste Aufgabenblock.')

BLOCK_INSTR= (
    u'Sie haben das Ende des %d\n von 4 Blocks erreicht. Um mit dem nächsten Block fortzufahren, drücken Sie bitte die Leertaste.',
     u'ACHTUNG folgend beginnt automatisch der nächste Aufgabenblock.'
    )

END = (
       u'Sie haben das Ende des Experiments erreicht. Vielen Dank für Ihre Teilnahme!'       
       )

PRACTICE_INST = (u'Sie haben das Ende des Blocks erreicht, drücken Sie die Leertaste um fortzufahren.')

EXP_END =(u'Sie haben diesen Teil des Experiments beendet. Drücken Sie bitte die Leertaste um fortzufahren.')

PRACTICE_FULL = [PRACTICE_FULL_1, PRACTICE_FULL_2]
PRACTICE_PART = [PRACTICE_PART_1, PRACTICE_PART_2]
PRACTICE_FULL_SHORT = [PRACTICE_FULL_1_SHORT, PRACTICE_FULL_2_SHORT]
