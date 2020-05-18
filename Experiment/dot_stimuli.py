# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:20:31 2020

@author: juliu
"""
import random

# Define Experimental parameter
frames = 60
direction = "left"
n_dots = 200
trgt_size = 30
dot_xys = []
coh_dot = random.sample(range(n_dots),  trgt_size) 
dot_speed = 5
print(coh_dot)
a = 0


for frame in range(frames):
    for dot in range(n_dots):
        if frame == 0: # randomly assign initial position
            dot_x = random.uniform(-200,200)
            dot_y = random.uniform(-200,200)
            dot_xys.append([dot_x,dot_y])
        else:
            if coh_dot.count(dot) == 1: # determine if dot is in target group via count function
                if dot_xys[dot][0] + dot_speed < 200: # if the dot is still within the window
                    dot_xys[dot][0] = dot_xys[dot][0] + dot_speed
                    dot_xys[dot][1] = dot_xys[dot][1] + random.randint(-dot_speed, dot_speed)
                else: # if the dot would move beyond
                    dot_xys[dot][0] = dot_xys[dot][0] + dot_speed - 400
                    dot_xys[dot][1] = dot_xys[dot][1] + random.randint(-dot_speed, dot_speed)
            else: # update the remaining dots
                dot_xys[dot][0] = dot_xys[dot][0] + random.randint(-dot_speed, dot_speed)
                dot_xys[dot][1] = dot_xys[dot][1] + random.randint(-dot_speed, dot_speed)
                if dot_xys[dot][0] > 200:
                    dot_xys[dot][0] = dot_xys[dot][0] - 400
                elif dot_xys[dot][0] < -200:
                    dot_xys[dot][0] = dot_xys[dot][0] + 400
                elif dot_xys[dot][1] > 200:
                    dot_xys[dot][1] = dot_xys[dot][1] - 400
                elif dot_xys[dot][1] < -200:
                    dot_xys[dot][1] = dot_xys[dot][1] + 400
                else:
                    pass
    print(dot_xys[17][0])
                
                    
                
                
                