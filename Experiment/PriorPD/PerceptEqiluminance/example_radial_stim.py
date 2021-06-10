#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 16:39:27 2021

@author: jules
"""

from psychopy import visual, event, core
from psychopy.tools.colorspacetools import hsv2rgb
import numpy as np

# #create texture (note imperfect rounding of 64/3)
# rgb = np.zeros([64,64,3])-1#start with all channels in all locs = -1
# rgb[:, 0:int((64/3)), 0]=1 #bottom 1/3rd of the first channel=1
# rgb[:, int((64/3)):int((64*2/3)), 1]=1 #middle 1/3rd of the 2nd channel=1
# rgb[:, int((64*2/3)):int((64*3/3)), 2]=1 #top 1/3rd of the 3rd channel=1

tex_num =64
#create texture (note imperfect rounding of 64/3)
rgb = np.zeros([tex_num,tex_num,3])-1#start with all channels in all locs = -1
rgb[:, 0:int((tex_num/3)), 0]=1 #bottom 1/3rd of the first channel=1
rgb[:, int((tex_num/3)):int((tex_num*2/3)), 1]=1 #middle 1/3rd of the 2nd channel=1
rgb[:, int((tex_num*2/3)):int((tex_num*3/3)), 2]=1 #top 1/3rd of the 3rd channel=1



Green = [115, 0.6, 0.7]
Blue = [204, 0.68, 1]
Yellow = [46, 1, 0.83]
Red = [14, 0.68, 0.8]

def hsv_array(col1, col2, arr_size):
    hsv = np.zeros([arr_size, arr_size, 3])
    hsv[:,0:int((arr_size/2)), :] = col1
    hsv[:,int((arr_size/2)): int((arr_size)*2/2), :] = col2
    return hsv

hsv1 = hsv_array(Blue, Yellow, tex_num)
    
globalClock = core.Clock()
win = visual.Window([800,800])
#make two wedges (in opposite contrast) and alternate them for flashing

# ring1 = visual.RadialStim(win, 
#                           tex=rgb, 
#                           color=[1,1,1],size=1,
#                           mask=[0,0,1,1,0,0,0,0,0,0,], 
#                           radialCycles=0, 
#                           angularCycles=8,
#                           interpolate=False)

ring1 = visual.RadialStim(win, 
                          tex=hsv1, 
                          color=[1,1,1],
                          size=1,
                          mask=[0,0,1,1,0,0,0,0,0,0,], 
                          radialCycles=0, 
                          angularCycles=8,
                          interpolate=False)


ring2 = visual.RadialStim(win, 
                          tex='sqrXsqr',
                          color=[1,-1,-1],
                          size=1, 
                          mask=[0,0,0,0,0,0,1,1,0,0,], 
                          radialCycles=0, 
                          angularCycles=8,
                          interpolate=False)

circle = visual.Circle(win=win,
                       radius=150,
                       units ='pix',
                       colorSpace = "hsv",
                       color=Green               
)


t = 0
rotationRate = 0.01 #revs per sec
while t<10:#for 5 secs
    t=globalClock.getTime()
    ring1.tex = hsv2rgb(hsv1)
    ring1.setOri(t*rotationRate*360.0)
    ring1.draw()
    #circle.draw()
    # ring2.setOri(-t*rotationRate*360.0)
    # ring2.draw()
    win.flip()

win.close()


