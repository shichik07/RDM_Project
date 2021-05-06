#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 14:33:01 2021

@author: jules
"""
# Gamma corrected Luminance matching
# https://www.101computing.net/colour-luminance-and-contrast-ratio/
# https://en.wikipedia.org/wiki/Grayscale#Colorimetric_(perceptual_luminance-preserving)_conversion_to_grayscale
# https://e2eml.school/convert_rgb_to_grayscale.html
# https://en.wikipedia.org/wiki/SRGB

import numpy as np 

def lum_calc(R,G,B):
    div = 255
    R0 = R/div
    G0 = G/div
    B0 = B/div
    
    R1 = col_conv(R0)
    G1 = col_conv(G0)
    B1 = col_conv(B0)
    Lum = (0.2126*R1) + (0.7152*G1) + (0.0722*B1)
    return round(Lum,4)*100
    
    

def col_conv(col):
    if col <= 0.04045:
        col1 = col/12.92
    else:
        col1 = np.power(((col + 0.055)/1.055), 2.4) 
    return col1

lum_calc(0,0,255)
lum_calc(0,255,0)
lum_calc(255,0,0)

# http://www.basseq.com/fun/utils/xyy2rgb.html
green = (85,188,75)
blue = (81, 186, 255)
red = (255, 121, 81)
yellow =(214,165,0)


c1 =yellow

lum_calc(c1[0], c1[1], c1[2])
