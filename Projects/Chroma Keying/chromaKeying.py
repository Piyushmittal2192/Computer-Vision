# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 15:27:51 2020

@author: piyus
"""

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

class green:
    def __init__(self, windowname,trackbarName, dests, trackValue):
        #self.point = None
        self.windowname = windowname
        self.trackbarName = trackbarName
        self.dests = dests
        self.trackValue = trackValue
        self.background = {'red': False, 'green': False, 'blue': False }
        self.background_color_range = {'lower': None, 'upper': None }
        self.blur = self.dests[0]
        self.blurHSV = None
        self.show()
        self.f = None
        self.s= None
        self.first = []
        self.second = []
        cv.setMouseCallback(self.windowname, self.on_mouse)
        cv.createTrackbar(self.trackbarName, self.windowname, self.trackValue, 255, self.onChange)
        #cv.createTrackbar(self.trackbarName, self.windowname, self.trackValue, 70, self.onChange)
        
    
    def show(self):
        cv.imshow(self.windowname, self.dests[1])
        #cv.imshow(self.windowname + ": mask", self.dests[1])
        cv.imshow(self.windowname + ": Without Green", self.dests[5])
    def mask(self):
        self.dests[2] = cv.inRange(self.blurHSV,self.background_color_range['lower'], self.background_color_range['upper'])
        bc_color = [k for k in self.background.keys() if self.background[k] == True][0]
        binary_mask = np.uint8((255 - self.dests[2])/255)
        full_mask = cv.merge((binary_mask,binary_mask,binary_mask))
        self.dests[3] = cv.multiply(self.dests[0],full_mask)
        
        binary_mask_bg = np.uint8(self.dests[2]/255)
        full_mask_bg = cv.merge((binary_mask_bg,binary_mask_bg,binary_mask_bg))
        test_bg = cv.multiply(self.dests[4], full_mask_bg)
        self.dests[5] = cv.add(self.dests[3], test_bg)
        
        print(str(bc_color) + ' is the BackGround Color')
        self.show()
        
    #def on_tolerance(self, )
    # draw rectanlge and avg the amount of hue in the rectangle pick the corrdinates os the point
    
    def on_mouse(self, action, x, y, flags, userdata): 
        #first = []
        #second = []
        #global f , s
        if action ==cv.EVENT_LBUTTONDOWN:
            self.f = (x,y)
            self.first.append(self.f)
            #cv.rectangle(self.dests[0],selffirst[0], (first[0][0] + 5, first[0][1] - 5), (255,255,0), 2, cv.LINE_AA );
        elif action == cv.EVENT_LBUTTONUP:
            self.s = (x,y)
            self.second.append(self.s)
            cv.rectangle(self.dests[1],self.f, self.s, (255,255,0), 2, cv.LINE_AA );
        self.show()
    
    def applyChanges(self):
        min_color_H = None
        min_color_S = None
        min_color_V = None
        min_color_list_H = []
        min_color_list_S = []
        min_color_list_V = []
        for i in range(len(self.first)): 
            min_y, max_y, min_x, max_x = min(self.first[i][0], self.second[i][0]), max(self.first[i][0], self.second[i][0]), min(self.first[i][1], self.second[i][1]) , max(self.first[i][1], self.second[i][1])
            #self.blur=cv.GaussianBlur(self.dests[0],(3,3),0,0)
            self.blurHSV = cv.cvtColor(self.dests[0], cv.COLOR_BGR2HSV)
            #hsv = cv.cvtColor(self.dests[0], cv.COLOR_BGR2HSV)
            H,S,V = cv.split(self.blurHSV)
            selected_color_H = H[min_x : max_x, min_y: max_y]
            selected_color_S = S[min_x : max_x, min_y: max_y]
            selected_color_V = V[min_x : max_x, min_y: max_y]
            mc_H = np.min(selected_color_H)
            mc_S = np.min(selected_color_S)
            mc_V = np.min(selected_color_V)
            min_color_list_H.append(mc_H)
            min_color_list_S.append(mc_S)
            min_color_list_V.append(mc_V)
        min_color_H = int(np.ceil(np.min(min_color_list_H)))
        min_color_S = int(np.ceil(np.min(min_color_list_S)))
        min_color_V = int(np.ceil(np.min(min_color_list_V)))
        if 36 < int(min_color_H) < 70:
            self.background_color_range['lower'] = (min_color_H, min_color_S, min_color_V )
            self.background_color_range['upper'] = (70, 255 ,255)
            #self.trackValue = min_color_S
            self.background['green'] = True
        
        self.mask()
    
    def onChange(self, *args):
        self.background_color_range['lower'] = (args[0], self.background_color_range['lower'][1], self.background_color_range['lower'][2])
        self.mask()
        #pass
        
        
        
            

im = cv.imread('chroma_key.jpg')
bground = cv.imread('background image.jpg')

bc_resize = cv.resize(bground, (im.shape[1], im.shape[0]),interpolation = cv.INTER_AREA)

img_copy = im.copy()
# Create a black copy of original image
# Acts as a mask
mask = np.zeros(im.shape[:2], np.uint8)
green_removed = np.zeros(im.shape[:2], np.uint8)

g = green('Image','tName',  [im, img_copy, mask, green_removed, bc_resize, bc_resize.copy()], 0)

while True:
    ch = cv.waitKey()
    if ch == 27:
        break
    if ch == ord('a'):
        g.applyChanges()
        
    if ch == ord('r'):
        g.dests[0][:] = im
        g.dests[1][:] = im
        g.dests[2][:] = np.zeros(im.shape[:2], np.uint8)
        g.dests[3][:] = np.zeros(im.shape, np.uint8)
        g.dests[4][:] = bc_resize
        g.show()
cv.destroyAllWindows()