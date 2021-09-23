#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 12:31:00 2021

@author: jules
"""
from psychopy.colors import Color
from psychopy import core, visual, gui, event, data, monitors
from psychopy.tools.colorspacetools import hsv2rgb, rgb2hsv
import numpy as np
import pandas as pd
import random
from prior_rdm.params import * # import fixed parameter 
from prior_rdm.Task_func import item_struct as itm # generate Items


def heterochromatic_flicker(win, colors):
    '''
    Function to create flicker photometry object to qualize color luminance for each participant psychophysically.
    All parameters necessary are not listed here unfortunately. Can be found in the params file.
    Sorry for the mess, but I had a hard time including objects from the psychopy experiment in a class (if I remember correctly).
    
    ---------
        
    Parameters
    ----------
        
    win: obj - window object of the experiment
    colors: list - list of colors to be matched in hsv color space
        
        
    Returns
    -------
        
    '''
    
    # Flicker Photometry Objects
    ProgressInfo = visual.TextStim(win=win, color=TEXT_COL, pos=(10.0,0.0))

    bar_outline = visual.Rect(win=win, 
                          pos=(BAR_POS), 
                          size=(WIDTH_PHOTO, HEIGHT_PHOTO*1.07), 
                          lineColor='White')
    bar_adj = visual.Rect(win=win,
                      pos=(BAR_POS),
                      fillColor = 'White')
    
    #for heterochromatic flicker photometry
    circle = visual.Circle(win=win,
                            radius=RADIUS,
                            units = "pix",
                            colorSpace = "hsv",
                            color= green_hsv)
    for comp in range(len(colors)-1):
        bar_pos = [5,0] # introduce here so that we always start at 0
        target_color = colors[comp + 1][1]
        base_color = BASE_COL_hsv
        ColorFound = False
        count1 = 0
        count2 = 0
        event.clearEvents()
        if LUM_METHOD == 'flicker':
            while ColorFound == False:
                keys = event.getKeys()
                count1 +=1
                circle.draw()
                bar_outline.draw()
                # move the progressbar
                bar_adj.pos = bar_pos[0], target_color[2]*HEIGHT_PHOTO- HEIGHT_PHOTO/2
                # Adjust Text
                ProgressInfo.text = 'Helligkeit : ' + str(round(target_color.copy()[2]*100)) + '%'
                ProgressInfo.draw()
                bar_adj.draw()
                win.flip()
                if count1%2 == 0:
                    circle.color = base_color
                else:
                    circle.color = target_color
                if keys != []:
                    if keys[0] == COLOR_KEYS[0]:
                        #if up has been pressed, increase brightness
                        if target_color[2] < 1:
                            target_color[2] += 0.01 
                            event.clearEvents() # clear events
                    elif keys[0] == COLOR_KEYS[1]:
                        #if up has been pressed, decrease brightness
                        if target_color[2] > 0:
                            target_color[2] -= 0.01 
                            event.clearEvents() # clear events
                    elif keys[0] == CONTINUE_KEYS[0]:
                        #target condition has been found, end loop
                        ColorFound = True
                        event.clearEvents()
                        print(target_color)
    return colors      

            
## NOT IMPLEMENTED MINIMUM MOTION TECHNIQUE BASICS

# # for Minimum Motion Technique
# def hsv_array(col1, col2, arr_size):
#     hsv = np.zeros([arr_size, arr_size, 3])
#     hsv[:,0:int((arr_size/2)), :] = col1
#     hsv[:,int((arr_size/2)): int((arr_size)*2/2), :] = col2
#     return hsv

# hsv1 = hsv_array(Blue, Yellow, arr)
# hsv2 = hsv_array(Yellow, Blue, arr)
    
# ring1 = visual.RadialStim(win, 
#                           tex=hsv1, 
#                           color=[1,1,1],
#                           size=8,
#                           mask=[0,0,1,1,0,0,0,0,0,0,], 
#                           radialCycles=0, 
#                           angularCycles=8,
#                           interpolate=False)

# ring2 = visual.RadialStim(win, 
#                           tex=hsv2, 
#                           color=[1,1,1],
#                           size=8,
#                           mask=[0,0,1,1,0,0,0,0,0,0,], 
#                           radialCycles=0, 
#                           angularCycles=8,
#                           interpolate=False)

# """
# Color comparison for-loop: We have one base color green which is kept constant.  
# All other colors are matched with respect to the baseline color. We also have to
# include another button in case the baseline color does not work.
# """

# target_color = Yellow.copy()

# for comp in range(len(DOT_G_COL)-1):
#     target_color = DOT_G_COL_hsv[comp + 1][1]
#     base_color = BASE_COL_hsv
#     ColorFound = False
#     count1 = 0
#     count2 = 0
#     event.clearEvents()
#     if LUM_METHOD == 'flicker':
#         while ColorFound == False:
#             keys = event.getKeys()
#             count1 +=1
#             circle.draw()
#             bar_outline.draw()
#             # move the progressbar
#             bar_adj.pos = bar_pos[0], target_color[2]*height - height/2
#             # Adjust Text
#             ProgressInfo.text = 'Helligkeit : ' + str(round(target_color.copy()[2]*100)) + '%'
#             ProgressInfo.draw()
#             bar_adj.draw()
#             win.flip()
#             if count1%2 == 0:
#                 circle.color = base_color
#             else:
#                 circle.color = target_color
#             if keys != []:
#                 print(keys)
#                 print(target_color)
#                 if keys[0] == COLOR_KEYS[0]:
#                     #if up has been pressed, increase brightness
#                     if target_color[2] < 1:
#                         target_color[2] += 0.01 
#                         event.clearEvents() # clear events
#                 elif keys[0] == COLOR_KEYS[1]:
#                     #if up has been pressed, decrease brightness
#                     if target_color[2] > 0:
#                         target_color[2] -= 0.01 
#                         event.clearEvents() # clear events
#                 elif keys[0] == CONTINUE_KEYS[0]:
#                     #target condition has been found, end loop
#                     ColorFound = True
#                     event.clearEvents()
#                     print(target_color)
#         print(Green, target_color)        
        
        
#     elif LUM_METHOD == 'min_mo':
#          while ColorFound == False:
#             keys = event.getKeys()
#             count1 +=1
#             if count1%2 == 0:
#                 ring1.tex = hsv2rgb(hsv1)
#                 ring1.draw()
#             else:
#                 ring2.tex = hsv2rgb(hsv2)
#                 ring2.draw()
#             win.flip()
#             if keys != []:
#                 print(keys)
#                 print(target_color)
#                 if keys[0] == COLOR_KEYS[0]:
#                     #if up has been pressed, increase brightness
#                     if target_color[2] < 1:
#                         target_color[2] += 0.01 
#                         event.clearEvents() # clear events
#                 elif keys[0] == COLOR_KEYS[1]:
#                     #if up has been pressed, decrease brightness
#                     if target_color[2] > 0:
#                         target_color[2] -= 0.01 
#                         event.clearEvents() # clear events
#                 elif keys[0] == CONTINUE_KEYS[0]:
#                     #target condition has been found, end loop
#                     ColorFound = True
#                     event.clearEvents()
#                     print(target_color)
#             hsv1 = hsv_array(BASE_COL, target_color, arr)
#             hsv2 = hsv_array(target_color, BASE_COL, arr) 
            
# win.close()
# core.quit()  
            