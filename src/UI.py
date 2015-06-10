from __future__ import division

'''Import own code'''
from grid import *

'''Import Python Libreries'''
import math
import random
import time

'''Import Kivy Libraries'''
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.logger import Logger
from kivy.graphics import (Canvas, Translate, Fbo, ClearColor, ClearBuffers, Scale)
from kivy.core.window import Window


class MyKnotworkWidget(Widget):
    '''Contains all the logic for displaying the knotwork to the canvas'''
    def __init__(self, **kwargs):
        '''Initialise the object'''
        super(MyKnotworkWidget, self).__init__(**kwargs)
        self.bp = False  # Also currently drawing breaklines TODO Fix this!
        self.onBreaklines = False #curerntly drawing breaklines
        self.breaklines = [] #breaklines in the undo stack
        self.breaklinesf = [] #breaklines in the redo stack

    def setOnBreaklines(self, val):
        '''Set self.onbreaklines, indicating that breaklines are being drawn'''
        self.onBreaklines = val
        
    def getOnBreaklines(self):
        '''get self.onbreaklines'''
        return self.onBreaklines
    def getAddedBLS(self):
        '''Returns False if no breaklines have been added else returns true'''
        if (len(self.breaklines) == 0):
            return False
        else:
            return True

    def printGrid(self, data, gridUnits, offsetX, offsetY):
        '''Print the grid from data, with gridUnits indicating the size of the cell, and offsetX and offsetY indicating the offset from bottom left corner'''
        with self.canvas:
            for y in range (len(data)+1): # one more dots than squares
                if (y%2 == 0): #draw primary grid (Yellow)
                    Color(1,1,0)
                    Line(points= [gridUnits+offsetX, gridUnits+offsetY+y*gridUnits, gridUnits+offsetX+(len(data[0]))*gridUnits, gridUnits+offsetY+y*gridUnits], width = 1)
                    #Color(1, 1, 0)
                if (y%2 == 1): #draw secondary grid (Cyan)
                    Color(0, 1,1)
                    Line(points=[gridUnits+offsetX, gridUnits+offsetY+y*gridUnits, gridUnits+offsetX+(len(data[0]))*gridUnits, gridUnits+offsetY+y*gridUnits], width = 1)
            for x in range(len(data[0])+1):
                if (x%2 == 0): #draw primary grid (Yellow)
                    Color(1,1,0)
                    Line(points = [gridUnits+offsetX+ x*gridUnits, gridUnits+offsetY, gridUnits+offsetX+x*gridUnits, gridUnits+offsetY+len(data)*gridUnits], width = 1)
                if (x%2 == 1): #draw secondary grid (Cyan)
                    Color(0, 1,1)
                    Line(points = [gridUnits+offsetX+ x*gridUnits, gridUnits+offsetY, gridUnits+offsetX+x*gridUnits, gridUnits+offsetY+len(data)*gridUnits], width = 1)

    def printPoints (self, data, gridUnits, offsetX, offsetY):
        '''Print points from data, with gridUnits indicating the size of the cell, and offsetX and offsetY indicating the offset from bottom left corner'''
        size = gridUnits/10
        with self.canvas:
            for y in range (len(data)+1): # one more dots than squares
                for x in range(len(data[0])+1):
                    if (x%2 == 0 and y%2 == 0): # draw primary points (red)
                        Color(1,0,0)
                        Ellipse(pos = (gridUnits+offsetX+x*gridUnits-size/2, gridUnits+offsetY+y*gridUnits- size/2), size = (size,size))
                    if (x%2 == 1 and y%2 == 1): # draw secondary points (blue)
                        Color(0,0,1)
                        Ellipse(pos = (gridUnits+offsetX+x*gridUnits-size/2, gridUnits+offsetY+y*gridUnits-size/2), size = (size,size))

    def printBreaklines (self, data, gridUnits, offsetX, offsetY):
        '''Print breaklines (in white) from data, with gridUnits indicating the size of the cell, and offsetX and offsetY indicating the offset from bottom left corner'''
        with self.canvas:
            for y in range(len(data)):
                for x in range(len(data[0])):
                    if data[y][x]["breakline"]["1"]:
                        Color(1,1,1)
                        Line(points=[gridUnits+offsetX+x*gridUnits, gridUnits+offsetY+y*gridUnits, gridUnits+offsetX+(x+1)*gridUnits, gridUnits+offsetY+y*gridUnits], width = 1)

                    if data[y][x]["breakline"]["2"]:
                        Color(1,1,1)
                        Line(points =[gridUnits+offsetX+(x+1)*gridUnits, gridUnits+offsetY+y*gridUnits, gridUnits+offsetX+(x+1)*gridUnits, gridUnits+offsetY+(y+1)*gridUnits], width = 1)

                    if data[y][x]["breakline"]["3"]:
                        Color(1,1,1)
                        Line(points = [gridUnits+offsetX+(x)*gridUnits, gridUnits+offsetY+(y+1)*gridUnits, gridUnits+offsetX+(x+1)*gridUnits, gridUnits+offsetY+(y+1)*gridUnits], width = 1)

                    if data[y][x]["breakline"]["4"]:
                        Color(1,1,1)
                        Line(points = [gridUnits+offsetX+(x)*gridUnits, gridUnits+offsetY+y*gridUnits, gridUnits+offsetX+(x)*gridUnits, gridUnits+offsetY+(y+1)*gridUnits], width = 1)
                        
    def getColors(self,bandnumber):
        '''Randomly generates a set of bandnumber colours'''
        colors = []
        for i in range(bandnumber):
            colors.append([random.random(),random.random(),random.random()])
        return colors
    
    def getPointTo(self, a, x, y, gridUnits, even, space, offsetX, offsetY):
        '''Get the actual point "to" that corresponds to an a "from" point (the point is space units away from the actual point allowing for spacing in the skeleton and knot). x,y are the x, y positions in the array, gridUnits is the size of each grid cell, even is a boolean if the row is even, offsetX and offsetY are how much the knot is offset'''
        if (even==0):
            if (a == 1):
                return [gridUnits+offsetX+(x+1)*gridUnits-math.sqrt(space/2), gridUnits+offsetY+ y*gridUnits+math.sqrt(space/2)]
            if (a == 2):
                return [gridUnits+offsetX+(x+1)*gridUnits, gridUnits+offsetY+ (y+0.5)*gridUnits]
            if (a == 3):
                return [gridUnits+offsetX+(x+1)*gridUnits-math.sqrt(space/2), gridUnits+offsetY+ (y+1)*gridUnits-math.sqrt(space/2)]
            if (a == 4):
                return [gridUnits+offsetX+(x+0.5)*gridUnits, gridUnits+offsetY+ (y+1)*gridUnits]
            if (a == 5):
                return [gridUnits+offsetX+(x)*gridUnits, gridUnits+offsetY+ (y+1)*gridUnits]
            if (a == 6):
                return [gridUnits+offsetX+(x)*gridUnits, gridUnits+offsetY+ (y+0.5)*gridUnits]
            if (a == 7):
                return [gridUnits+offsetX+(x)*gridUnits, gridUnits+offsetY+ (y)*gridUnits]
            if (a == 8):
                return [gridUnits+offsetX+(x+0.5)*gridUnits, gridUnits+offsetY+ (y)*gridUnits]
        else:
            if (a == 1):
                return [gridUnits+offsetX+(x+1)*gridUnits, gridUnits+offsetY+ y*gridUnits]
            if (a == 2):
                return [gridUnits+offsetX+(x+1)*gridUnits, gridUnits+offsetY+ (y+0.5)*gridUnits]
            if (a == 3):
                return [gridUnits+offsetX+(x+1)*gridUnits, gridUnits+offsetY+ (y+1)*gridUnits]
            if (a == 4):
                return [gridUnits+offsetX+(x+0.5)*gridUnits, gridUnits+offsetY+ (y+1)*gridUnits]
            if (a == 5):
                return [gridUnits+offsetX+(x)*gridUnits+ math.sqrt(space/2), gridUnits+offsetY+ (y+1)*gridUnits- math.sqrt(space/2)]
            if (a == 6):
                return [gridUnits+offsetX+(x)*gridUnits, gridUnits+offsetY+ (y+0.5)*gridUnits]
            if (a == 7):
                return [gridUnits+offsetX+(x)*gridUnits+ math.sqrt(space/2), gridUnits+offsetY+ (y)*gridUnits + math.sqrt(space/2)]
            if (a == 8):
                return [gridUnits+offsetX+(x+0.5)*gridUnits, gridUnits+offsetY+ (y)*gridUnits]
    def getPoint(self, a, x, y, gridUnits, offsetX, offsetY):
        '''Get the actual point "to" that corresponds to an a "from" point. x,y are the x, y positions in the array, gridUnits is the size of each grid cell, even is a boolean if the row is even, offsetX and offsetY are how much the knot is offset'''
        if (a == 1):
            return [gridUnits+offsetX+(x+1)*gridUnits, gridUnits+ offsetY+ y*gridUnits]
        if (a == 2):
            return [gridUnits+offsetX+(x+1)*gridUnits, gridUnits+ offsetY+ (y+0.5)*gridUnits]
        if (a == 3):
            return [gridUnits+offsetX+(x+1)*gridUnits, gridUnits+ offsetY+ (y+1)*gridUnits]
        if (a == 4):
            return [gridUnits+offsetX+(x+0.5)*gridUnits, gridUnits+ offsetY+ (y+1)*gridUnits]
        if (a == 5):
            return [gridUnits+offsetX+(x)*gridUnits, gridUnits+ offsetY+ (y+1)*gridUnits]
        if (a == 6):
            return [gridUnits+offsetX+(x)*gridUnits, gridUnits+ offsetY+ (y+0.5)*gridUnits]
        if (a == 7):
            return [gridUnits+offsetX+(x)*gridUnits, gridUnits+ offsetY+ (y)*gridUnits]
        if (a == 8):
            return [gridUnits+offsetX+(x+0.5)*gridUnits, gridUnits+ offsetY+ (y)*gridUnits]

    def printKnot(self, data, gridUnits, width, spacing, offsetX, offsetY):
        '''Prints the skeleton knot from data, with gridUnits sized cells and spacing to show overlap, with bottom left corner at (offsetX, offsetY)'''
        with self.canvas:
            ##get the number of bands
            bandnumber = []
            for y in range(len(data)):
                for x in range(len(data[0])):
                    bandnumber.append(data[y][x]["bandnumber"])
                    
            bandnumber = max(bandnumber)+1
            color = self.getColors(bandnumber) #set the colours
            ##draw the knot
            for y in range(len(data)):
                for x in range(len(data[0])):
                    Color(color[data[y][x]["bandnumber"]][0], color[data[y][x]["bandnumber"]][1], color[data[y][x]["bandnumber"]][2])
                    Line(points = [self.getPointTo(data[y][x]["edgecode"]["from"], x, y, gridUnits,y%2, spacing, offsetX, offsetY)[0], self.getPointTo(data[y][x]["edgecode"]["from"], x, y, gridUnits,y%2, spacing, offsetX, offsetY)[1], self.getPointTo(data[y][x]["edgecode"]["to"], x, y, gridUnits, y%2, spacing, offsetX, offsetY)[0],  self.getPointTo(data[y][x]["edgecode"]["to"], x, y, gridUnits, y%2, spacing, offsetX, offsetY)[1]], width = width)

    def printFinalKnot(self, data, gridUnits, width, spacing, curve, offsetX, offsetY, cornerType):
        '''Prints the final knot from data, with cells of size gridUnits, spacing to show overlap, cornerType sets the type of corner (0 = right angle, 1 = curve, 2 = straight line), with bootom left corner at (offsetX, offsetY)'''
        with self.canvas:
            ##get the number of bands
            bandnumber = []
            for y in range(len(data)):
                for x in range(len(data[0])):
                    bandnumber.append(data[y][x]["bandnumber"])
                    
            bandnumber = max(bandnumber)+1
            color = self.getColors(bandnumber) #set the colours
            ##Draw the knot
            for y in range(len(data)):
                for x in range(len(data[0])):
                    y = len(data)-1-y
                    ##Draw Corner
                    if (data[y][x]["corner"]):
                        if (cornerType == 0): ##Right angle corner
                            Color(color[data[y][x]["bandnumber"]][0], color[data[y][x]["bandnumber"]][1], color[data[y][x]["bandnumber"]][2])
                            Line(points = [self.getPointTo(data[y][x]["edgecode"]["from"], x, y, gridUnits,y%2, spacing, offsetX, offsetY)[0], self.getPointTo(data[y][x]["edgecode"]["from"], x, y, gridUnits,y%2, spacing, offsetX, offsetY)[1],gridUnits+offsetX+(x+0.5)*gridUnits, gridUnits+offsetY+ (y+0.5)*gridUnits, self.getPointTo(data[y][x]["edgecode"]["to"], x, y, gridUnits, y%2, spacing, offsetX, offsetY)[0],  self.getPointTo(data[y][x]["edgecode"]["to"], x, y, gridUnits, y%2, spacing, offsetX, offsetY)[1]], width = width, cap ="square")
                        elif (cornerType == 1): ##Curve corner
                            Color(color[data[y][x]["bandnumber"]][0], color[data[y][x]["bandnumber"]][1], color[data[y][x]["bandnumber"]][2])
                            Line(bezier = [self.getPointTo(data[y][x]["edgecode"]["from"], x, y, gridUnits,y%2, spacing, offsetX, offsetY)[0], self.getPointTo(data[y][x]["edgecode"]["from"], x, y, gridUnits,y%2, spacing, offsetX, offsetY)[1],gridUnits+offsetX+(x+0.5)*gridUnits, gridUnits+offsetY+ (y+0.5)*gridUnits, self.getPoint(data[y][x]["edgecode"]["to"], x, y, gridUnits, offsetX, offsetY)[0],  self.getPoint(data[y][x]["edgecode"]["to"], x, y, gridUnits,  offsetX, offsetY)[1]], width = width, cap ="square")
                        elif (cornerType == 2): ##Straight line corner
                            Color(color[data[y][x]["bandnumber"]][0], color[data[y][x]["bandnumber"]][1], color[data[y][x]["bandnumber"]][2])
                            Line(points = [self.getPointTo(data[y][x]["edgecode"]["from"], x, y, gridUnits,y%2, spacing, offsetX, offsetY)[0], self.getPointTo(data[y][x]["edgecode"]["from"], x, y, gridUnits,y%2, spacing, offsetX, offsetY)[1], self.getPointTo(data[y][x]["edgecode"]["to"], x, y, gridUnits, y%2, spacing, offsetX, offsetY)[0],  self.getPointTo(data[y][x]["edgecode"]["to"], x, y, gridUnits, y%2, spacing, offsetX, offsetY)[1]], width = width, cap ="square")
                    ##Draw knot lines on border
                    elif (data[y][x]["border"]):
                        Color(color[data[y][x]["bandnumber"]][0], color[data[y][x]["bandnumber"]][1], color[data[y][x]["bandnumber"]][2])
                        Line(bezier = [self.getPointTo(data[y][x]["edgecode"]["from"], x, y, gridUnits,y%2, spacing, offsetX, offsetY)[0], self.getPointTo(data[y][x]["edgecode"]["from"], x, y, gridUnits,y%2, spacing, offsetX, offsetY)[1],gridUnits+offsetX+(x+0.5)*gridUnits, gridUnits+offsetY+ (y+0.5)*gridUnits, self.getPoint(data[y][x]["edgecode"]["to"], x, y, gridUnits, offsetX, offsetY)[0],  self.getPoint(data[y][x]["edgecode"]["to"], x, y, gridUnits,  offsetX, offsetY)[1]], width = width, cap ="square")
                    ##Draw interior knot lines
                    else:
                        Color(color[data[y][x]["bandnumber"]][0], color[data[y][x]["bandnumber"]][1], color[data[y][x]["bandnumber"]][2])
                        Line(points = [self.getPointTo(data[y][x]["edgecode"]["from"], x, y, gridUnits,y%2, spacing, offsetX, offsetY)[0], self.getPointTo(data[y][x]["edgecode"]["from"], x, y, gridUnits,y%2, spacing, offsetX, offsetY)[1], self.getPointTo(data[y][x]["edgecode"]["to"], x, y, gridUnits, y%2, spacing, offsetX, offsetY)[0],  self.getPointTo(data[y][x]["edgecode"]["to"], x, y, gridUnits, y%2, spacing, offsetX, offsetY)[1]], width = width, cap ="square")




    def resetVisited(self, data):
        '''Reset all cells in data to unvisited'''
        for i in range(len(data)):
            for j in range(len(data[0])):
                    data[i][j]["visited"] = False
        return data

    def getNextBlock(self, x, y, ec):
        '''Get the next block fron (x, y) from edgecode: ec'''
        if ec == 1:
            return [x+1, y-1]
        elif ec == 2:
            return [x+1, y]
        elif ec == 3:
            return [x+1, y+1]
        elif ec == 4:
            return [x, y+1]
        elif ec == 5:
            return [x-1, y+1]
        elif ec == 6:
            return [x-1, y]
        elif ec == 7:
            return [x-1, y-1]
        elif ec == 8:
            return [x, y-1]


    def getKnotPointsbyBand(self, data, n, gridUnits, offsetX, offsetY, cornerType, overlap):
        '''
        Get the points and angles for the 3D output grouped by band
        data: array representing the knot
        n: number of cylinders to break each line into (1 line per cell)
        gridUnits: the size of each cell
        (offsetX, offsetY): zero position of the knot (for use with other functions - the knot is normalised to have its center at (0,0))
        cornerType: The corner type (0: right angle, 1: curve, 2: straight line(broken))
        overlap: the distance between two knot bands at intersection
        '''
        #get number of band
        bandnumber = []
        for y in range(len(data)):
            for x in range(len(data[0])):
                bandnumber.append(data[y][x]["bandnumber"])
                
        bandnumber = max(bandnumber)+1
        
        data = self.resetVisited(data)#reset visited
        
        points = []
        c = 0
        #loop over the bands
        for y in range(len(data)):
            for x in range(len(data[0])):
                if (data[y][x]["visited"] == False):
                    points.append([])
                    co = self.getNextBlock(x, y, data[y][x]["edgecode"]["to"])
                    co = [x, y]
                    #culmulative angle for handling going round corners
                    if (data[co[1]][co[0]]["corner"]):
                        ca = math.pi/2
                    else:
                        ca = -math.pi/4
                    switch = False
                    #loop over current band
                    while (data[co[1]][co[0]]["visited"] == False):

                        data[co[1]][co[0]]["visited"] = True

                        ##Get the x,y,z points of the start/end points (thses will be transformed later with bezier curves)
                        x1 = self.getPoint(data[co[1]][co[0]]["edgecode"]["from"], co[0], co[1], gridUnits, offsetX, offsetY)[0]-(len(data[0])*gridUnits)/2-offsetX - gridUnits
                        y1 = self.getPoint(data[co[1]][co[0]]["edgecode"]["from"], co[0], co[1], gridUnits, offsetX, offsetY)[1] -(len(data)*gridUnits)/2-offsetY -gridUnits
                        z1 = 0
                        x2 = self.getPoint(data[co[1]][co[0]]["edgecode"]["to"], co[0], co[1], gridUnits, offsetX, offsetY)[0]-(len(data[0])*gridUnits)/2-offsetX - gridUnits
                        y2 = self.getPoint(data[co[1]][co[0]]["edgecode"]["to"], co[0], co[1], gridUnits, offsetX, offsetY)[1] -(len(data)*gridUnits)/2-offsetY - gridUnits
                        z2 = 0

                        ##Differences for use with finding the angles
                        mx = x2-x1
                        my = y2-y1
                        mz = z2-z1


                        ##Output Corner points
                        if (data[co[1]][co[0]]["corner"]):
                            ##Add point at center of cell
                            x3 = (co[0]+0.5)*gridUnits -(len(data[0])*gridUnits)/2
                            y3 = (co[1]+0.5)*gridUnits-(len(data)*gridUnits)/2
                            z3 = 0
                            mx = x2-x1
                            my = y2-y1
                            mz = z2-z1

                            ##Corner number circles from top right (0) to top left (3)
                            if data[co[1]][co[0]]["cornerNumber"] == 0:
                                angle1 = math.pi
                                angle2 = math.pi/2+math.pi
                            elif (data[co[1]][co[0]]["cornerNumber"] == 2):
                                angle1 = math.pi*2
                                angle2 = math.pi/2+math.pi*2
                                angle1 = 0
                            elif (data[co[1]][co[0]]["cornerNumber"] == 1):
                                angle1 = math.pi/2+math.pi
                                angle2 = math.pi*2
                            else:
                                angle1 = math.pi/2+math.pi*2
                                angle2 = math.pi


                            if (cornerType == 0): #right angle corner
                                points[c].append([x1, y1, z1, 0, math.pi/2,ca, False, False])
                                
                                if not switch:
                                    ca += math.pi/4
                                else:
                                    ca -= math.pi/4

                                points[c].append([x3, y3, z3, 0, math.pi/2,ca, True, data[co[1]][co[0]]["cornerNumber"]])
                                
                                if not switch:
                                    ca += math.pi/4
                                else:
                                    ca -= math.pi/4

                                points[c].append([x2, y2, z2, 0, math.pi/2,ca, False, False])
                                
                            if (cornerType == 1): #curve corner
                                for i in range(n+1):
                                    t = i/n
                                    a = [(1-t)*((1-t)*x1+t*x3)+t*((1-t)*x3+t*x2), (1-t)*((1-t)*y1+t*y3)+t*((1-t)*y3+t*y2), (1-t)*((1-t)*z1+t*z3)+t*((1-t)*z3+t*z2), 0,math.pi/2, math.pi/2, False, False] #parameterised bezier curve
                                    q0 = [(1-t)*x1+t*x3, (1-t)*y1+t*y3, (1-t)*z1+t*z3] #drop one point from the bezier curve for a better curve on the x-y plane
                                    q1 = [(1-t)*x3+t*x2, (1-t)*y3+t*y2, (1-t)*z3+t*z2] #drop one point from the bezier curve for a better curve on the x-y plane
                                    a[5] = math.atan2(q1[1]-q0[1], q1[0] - q0[0])+math.pi
                                    points[c].append(a)
                                if not switch:
                                    ca += math.pi/2
                                else:
                                    ca -= math.pi/2
                            if (cornerType == 2): #stright line corner (breaks 3D)
                                for i in range(n+1):
                                    if data[co[1]][co[0]]["cornerNumber"] == 2 or data[co[1]][co[0]]["cornerNumber"] == 0:
                                        a = [x1 + (i/n)*mx, y1 +(i/n)*my, z1 + (i/n)*mz, 0,math.pi/2, math.atan(my/mx)+ca, False, False]
                                    else:
                                        a = [x1 + (i/n)*mx, y1 +(i/n)*my, z1 + (i/n)*mz, 0,math.pi/2, -math.atan(my/mx)+ca, False, False]

                                    points[c].append(a)
                                if not switch:
                                    ca += math.pi/2
                                else:
                                    ca -= math.pi/2

                        ##Draw items that are on the border
                        elif (data[co[1]][co[0]]["border"]):

                            ##Set positions (start positions(1) and end positions (4) have their z values raised to account for overlap, middle positions (2+3) are created for smooth bezier curves (they have the same x, y points and z points set to overlap or 0))
                            x4 = x2
                            y4 = y2
                            z4 = z2

                            x2 = (co[0]+0.5)*gridUnits -(len(data[0])*gridUnits)/2
                            y2 = (co[1]+0.5)*gridUnits-(len(data)*gridUnits)/2
                            z2 = 0
                            x3 = (co[0]+0.5)*gridUnits -(len(data[0])*gridUnits)/2
                            y3 = (co[1]+0.5)*gridUnits-(len(data)*gridUnits)/2
                            z3 = 0
                            if (co[1]%2 == 0 and (data[co[1]][co[0]]["edgecode"]["from"] == 1 or data[co[1]][co[0]]["edgecode"]["from"] == 3)):
                                z1 = z1+overlap
                                z2 += 11
                            elif (co[1]%2 == 0 and (data[co[1]][co[0]]["edgecode"]["to"] == 1 or data[co[1]][co[0]]["edgecode"]["to"] == 3)):
                                z4 = z4 +overlap
                                z3+=11
                            elif (co[1]%2 == 1 and (data[co[1]][co[0]]["edgecode"]["to"] == 5 or data[co[1]][co[0]]["edgecode"]["to"] == 7)):
                                z4 = z4+overlap
                                z3 += 11
                            elif (co[1]%2 == 1 and (data[co[1]][co[0]]["edgecode"]["from"] == 5 or data[co[1]][co[0]]["edgecode"]["from"] == 7)):
                                z1 = z1 +overlap
                                z2 += 11

                            ##Loop over the points for this section
                            for i in range(n+1):
                                t = i/n
                                t2 = (i+0.01)/n
                                a = [(1-t)*((1-t)*x1+t*x2)+t*((1-t)*x2+t*x4), (1-t)*((1-t)*y1+t*y2)+t*((1-t)*y2+t*y4), (1-t)*(1-t)*(1-t)*z1+3*(1-t)*(1-t)*t*z2+3*(1-t)*t*t*z3+t*t*t*z4, 0,math.pi/2, math.pi/2, False, False]

                                ##For the angle
                                q0 = [(1-t)*x1+t*x2, (1-t)*y1+t*y2, (1-t)*z1+t*z2]
                                q1 = [(1-t)*x3+t*x4, (1-t)*y3+t*y4, (1-t)*z3+t*z4]
                                a[5] = math.atan2(q1[1]-q0[1], q1[0] - q0[0])+math.pi


                                points[c].append(a)


                            ca = a[5] #set the cumulative angle to the angle of the last point
                        else: ## Draw the interior lines
                            ##Check what positions are necessary
                            if (co[1]%2 == 0 and (data[co[1]][co[0]]["edgecode"]["from"] == 1 or data[co[1]][co[0]]["edgecode"]["from"] == 3)):
                                ##set positions
                                z1 = z1+overlap
                                x4 = x2
                                y4 = y2
                                z4 = z2
                                x3 = (co[0]+0.5)*gridUnits -(len(data[0])*gridUnits)/2
                                y3 = (co[1]+0.5)*gridUnits-(len(data)*gridUnits)/2
                                z3 = 0
                                x2 = (co[0]+0.5)*gridUnits -(len(data[0])*gridUnits)/2
                                y2 = (co[1]+0.5)*gridUnits-(len(data)*gridUnits)/2
                                z2 = overlap
                                ##loop over points in line
                                for i in range(n+1):
                                    t = i/n

                                    B4 = [(1-t)*(1-t)*(1-t)*x1+3*(1-t)*(1-t)*t*x2+3*(1-t)*t*t*x3+t*t*t*x4, (1-t)*(1-t)*(1-t)*y1+3*(1-t)*(1-t)*t*y2+3*(1-t)*t*t*y3+t*t*t*y4, (1-t)*(1-t)*(1-t)*z1+3*(1-t)*(1-t)*t*z2+3*(1-t)*t*t*z3+t*t*t*z4, 0, math.pi/2,ca, False, False]# math.atan(my/mx)+math.pi]

                                    points[c].append(B4)
                                    
                            elif (co[1]%2 == 0 and (data[co[1]][co[0]]["edgecode"]["to"] == 1 or data[co[1]][co[0]]["edgecode"]["to"] == 3)):
                                ##set Positions
                                z2 = z2+overlap
                                x4 = x2
                                y4 = y2
                                z4 = z2
                                x3 = (co[0]+0.5)*gridUnits -(len(data[0])*gridUnits)/2
                                y3 =  (co[1]+0.5)*gridUnits-(len(data)*gridUnits)/2
                                z3 = overlap
                                x2 =(co[0]+0.5)*gridUnits -(len(data[0])*gridUnits)/2
                                y2 =  (co[1]+0.5)*gridUnits-(len(data)*gridUnits)/2
                                z2 = 0
                                ##Loop over points in line
                                for i in range(n+1):
                                    t = i/n

                                    B4 = [(1-t)*(1-t)*(1-t)*x1+3*(1-t)*(1-t)*t*x2+3*(1-t)*t*t*x3+t*t*t*x4, (1-t)*(1-t)*(1-t)*y1+3*(1-t)*(1-t)*t*y2+3*(1-t)*t*t*y3+t*t*t*y4, (1-t)*(1-t)*(1-t)*z1+3*(1-t)*(1-t)*t*z2+3*(1-t)*t*t*z3+t*t*t*z4, 0, math.pi/2, ca, False, False]#math.atan(my/mx)+math.pi]

                                    points[c].append(B4)
                                    
                            elif (co[1]%2 == 1 and (data[co[1]][co[0]]["edgecode"]["to"] == 5 or data[co[1]][co[0]]["edgecode"]["to"] == 7)):
                                ##set positions
                                z2 = z2+overlap
                                x4 = x2
                                y4 = y2
                                z4 = z2
                                x3 = (co[0]+0.5)*gridUnits -(len(data[0])*gridUnits)/2
                                y3 =  (co[1]+0.5)*gridUnits-(len(data)*gridUnits)/2
                                z3 = overlap
                                x2 = (co[0]+0.5)*gridUnits -(len(data[0])*gridUnits)/2
                                y2 = (co[1]+0.5)*gridUnits-(len(data)*gridUnits)/2
                                z2 = 0
                                ##loop over points in line
                                for i in range(n+1):
                                    t = i/n
                                    
                                    B4 = [(1-t)*(1-t)*(1-t)*x1+3*(1-t)*(1-t)*t*x2+3*(1-t)*t*t*x3+t*t*t*x4, (1-t)*(1-t)*(1-t)*y1+3*(1-t)*(1-t)*t*y2+3*(1-t)*t*t*y3+t*t*t*y4, (1-t)*(1-t)*(1-t)*z1+3*(1-t)*(1-t)*t*z2+3*(1-t)*t*t*z3+t*t*t*z4, 0, math.pi/2, ca, False, False]#math.atan(my/mx)+math.pi]

                                    points[c].append(B4)
                                    
                            elif (co[1]%2 == 1 and (data[co[1]][co[0]]["edgecode"]["from"] == 5 or data[co[1]][co[0]]["edgecode"]["from"] == 7)):
                                ##set Positions
                                z1 = z1+overlap
                                x4 = x2
                                y4 = y2
                                z4 = z2
                                x3 = (co[0]+0.5)*gridUnits -(len(data[0])*gridUnits)/2
                                y3 =  (co[1]+0.5)*gridUnits-(len(data)*gridUnits)/2
                                z3 = 0
                                x2 = (co[0]+0.5)*gridUnits -(len(data[0])*gridUnits)/2
                                y2 =  (co[1]+0.5)*gridUnits-(len(data)*gridUnits)/2
                                z2 = overlap
                                ##loop over points in line
                                for i in range(n+1):
                                    t = i/n

                                    B4 = [(1-t)*(1-t)*(1-t)*x1+3*(1-t)*(1-t)*t*x2+3*(1-t)*t*t*x3+t*t*t*x4, (1-t)*(1-t)*(1-t)*y1+3*(1-t)*(1-t)*t*y2+3*(1-t)*t*t*y3+t*t*t*y4, (1-t)*(1-t)*(1-t)*z1+3*(1-t)*(1-t)*t*z2+3*(1-t)*t*t*z3+t*t*t*z4, 0, math.pi/2, ca, False, False]#math.atan(my/mx)+math.pi]

                                    points[c].append(B4)

                                
                        po = co ##Store previous block
                        co = self.getNextBlock(co[0], co[1], data[co[1]][co[0]]["edgecode"]["to"])
                    

                        ##set switch based on the corners                        
                        if data[po[1]][po[0]]["edgecode"]["to"] == 1 and (data[po[1]][po[0]+1]["edgecode"]["to"] == 7 or data[po[1]][po[0]+1]["edgecode"]["from"] == 7):
                            switch = not switch
                        if data[po[1]][po[0]]["edgecode"]["to"] == 3 and (data[po[1]][po[0]+1]["edgecode"]["to"] == 5 or data[po[1]][po[0]+1]["edgecode"]["from"] == 5):
                            switch = not switch
                        if data[po[1]][po[0]]["edgecode"]["to"] == 5 and (data[po[1]][po[0]-1]["edgecode"]["to"] == 3 or data[po[1]][po[0]-1]["edgecode"]["from"] == 3):
                            switch = not switch
                        if data[po[1]][po[0]]["edgecode"]["to"] == 7 and (data[po[1]][po[0]-1]["edgecode"]["to"] == 1 or data[po[1]][po[0]-1]["edgecode"]["from"] == 1):
                            switch = not switch
                    c += 1
                        
        return points
    
    def clearCanvas(self):
        '''Clear the canvas'''
        self.canvas.clear()


        

    def drawAddBreakline(self, data, gridUnits, offsetX, offsetY, width, spacing,curve, cornerType):
        '''
        Draws the brealine add/remove interface
        data: the matrix which describes the knot
        griduUnits: the size of each grid cell is gridUnits*gridUnits
        (offsetX, offsetY) the origin of the knot
        width: width of the knot lines
        spacing: the spacing to show overlap
        curve: unused - need to remove
        cornerType: the type of corner
        '''
        ##Store the values in self for later use in on_touch
        self.num = 0
        size = gridUnits/2
        self.gridUnits = gridUnits
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.grid = data
        self.points = []
        self.bp = True
        self.width2 = width
        self.spacing = spacing
        self.curve = curve
        self.cornerType = cornerType

        self.clearCanvas()

        ##Print the knot and the breaklines
        self.printFinalKnot(self.grid, self.gridUnits,self.width2,  self.spacing, curve,self.offsetX, self.offsetY, cornerType)
        self.printBreaklines(self.grid, self.gridUnits, self.offsetX, self.offsetY)
        

        ##Print the dots which indicate the breaklines        
        with self.canvas:
            for y in range (len(data)+1): # one more dots than squares
                for x in range(len(data[0])+1):
                    if (x%2 == 0 and y%2 == 0): # draw primary points (red)
                        Color(1,0,0)
                        Ellipse(pos = (gridUnits+offsetX+x*gridUnits-size/2, gridUnits+offsetY+y*gridUnits-size/2), size = (size, size))

                    if (x%2 == 1 and y%2 == 1): # draw secondary points (blue)
                        Color(0,0,1)
                        Ellipse(pos = (gridUnits+offsetX+x*gridUnits-size/2, gridUnits+offsetY+y*gridUnits-size/2), size = (size,size))
    
    def checkPoint(self, px, py, data):
        '''Check that the point (px, py) are acceptable points to join breaklines. Returns an array containg their position in the array'''
        gridUnits = self.gridUnits
        with self.canvas:
            for y in range (len(data)+1): # one more dots than squares
                for x in range(len(data[0])+1):
                    if (px<gridUnits+self.offsetX+x*gridUnits+gridUnits/2 and px>gridUnits+self.offsetX+x*gridUnits-gridUnits/2 and py<gridUnits+self.offsetY+y*gridUnits+gridUnits/2 and py>gridUnits+self.offsetY+y*gridUnits-gridUnits/2 and (x%2 == 0 and y%2 == 0 or x%2 == 1 and y%2 == 1)):
                        if (x%2 == 0 and y%2 == 0): # draw primary points (red)
                            Color(1,1,0)
                            Ellipse(pos = (gridUnits+self.offsetX+x*gridUnits-gridUnits/8, gridUnits+self.offsetY+y*gridUnits- gridUnits/8), size =(gridUnits/4, gridUnits/4))
                        if (x%2 == 1 and y%2 == 1): # draw secondary points (blue)
                            Color(1,1,0)
                            Ellipse(pos = (gridUnits+self.offsetX+x*gridUnits-gridUnits/8, gridUnits+self.offsetY+y*gridUnits- gridUnits/8), size = (gridUnits/4, gridUnits/4))


                        return [x,y] ##Position in the array
        print("fail") ##Points Failed the test
        return False

    def checkPoints(self, p1, p2, data):
        '''Check that the points p1 and p2 are points on the border'''
        if p1[0] == p2[0]:
            if p1[0] == 0:
                print("1")
                return False
            if p1[0] == len(data[0]):
                print("2")
                return False
        if p1[1] == p2[1]:
            if p1[1] == 0:
                print("3")
                return False
            if p1[1] == len(data):
                print("4")
                return False
        return True
    def getPoints(self):
        '''Returns self.points'''
        return self.points

    def checkCross(self, p1, p2, p3, p4):
        '''Check if the lines described by  [p1, p2] and [p3, p4] cross and whether they are on the same subgrid (primary/secondary)'''
        if (p1 == p3 and p2 == p4):
            print("test")
            return False
        if (p1[0]%2 == 0 and p3[0]%2 == 0 or p1[1]%2 == 0 and p3[1]%2 == 0):
            print("same subgrid")
            return False
        if (p1[0]%2 == 1 and p3[0]%2 == 1 or p1[1]%2 == 1 and p3[1]%2 == 1):
            print("same sec grid")
            return False
        if (p1[0] == p2[0]):
            if (p3[0] == p4[0]):
                return False
            elif(p3[1] == p4[1]):
                if (((p1[1]>=p3[1] and p2[1]<=p3[1]) or (p1[1]<=p3[1] and p2[1]>=p3[1])) and ((p1[0]<=p3[0] and p1[0]>=p4[0]) or (p1[0]>=p3[0] and p1[0]<=p4[0]))):
                    return True
        elif (p1[1] == p2[1]):
            if (p3[1] == p4[1]):
                return False
            elif(p3[0] == p4[0]):
                if (((p1[1]>=p3[1] and p2[1]<=p4[1]) or (p1[1]<=p3[1] and p2[1]>=p4[1])) and ((p1[0]<=p3[0] and p2[0]>=p3[0]) or (p1[0]>=p3[0] and p2[0]<=p3[0]))):
                    return True
        print("Fail")
        return False
    def backFuntion(self):
        '''Undoes the previously added breakline'''
        if (len(self.breaklines) != 0):
            points = self.breaklines.pop()
            self.breaklinesf.append(points)
            self.grid = grid().addBreakline(points[0], points[1], self.grid) ##Writes over breakline
            #recalculate the grid
            self.grid = grid().setProps(self.grid)
            self.grid = grid().detEdgecode(self.grid)
            self.grid = grid().setBandNumber(self.grid)
            #reprint Knot
            self.clearCanvas()
            self.printFinalKnot(self.grid, self.gridUnits,self.width2,  self.spacing,self.curve, self.offsetX, self.offsetY, self.cornerType)
            #undo is also possible outside of the breaklines interface
            if (self.onBreaklines):
                self.drawAddBreakline(self.grid, self.gridUnits, self.offsetX, self.offsetY, self.width2, self.spacing, self.curve, self.cornerType)
                self.printBreaklines(self.grid, self.gridUnits, self.offsetX, self.offsetY)
    
    def forwardFunction(self):
        '''Redo function'''
        if (len(self.breaklinesf) != 0):
            points = self.breaklinesf.pop()
            self.breaklines.append(points)
            self.grid = grid().addBreakline(points[0], points[1], self.grid) ##rewrites the breakline
            ##recalculate the grid
            self.grid = grid().setProps(self.grid)
            self.grid = grid().detEdgecode(self.grid)
            self.grid = grid().setBandNumber(self.grid)
            ##Redraw the knot
            self.clearCanvas()
            self.printFinalKnot(self.grid, self.gridUnits,self.width2,  self.spacing,self.curve, self.offsetX, self.offsetY, self.cornerType)
            ##Redo is also available outside of the breaklines interface
            if (self.onBreaklines):
                self.drawAddBreakline(self.grid, self.gridUnits, self.offsetX, self.offsetY, self.width2, self.spacing, self.curve, self.cornerType)
                self.printBreaklines(self.grid, self.gridUnits, self.offsetX, self.offsetY)
        
    def on_touch_down(self, touch):
        '''Called on mouse click, recieves touch object which contains the coordinates of the click'''
        if (self.bp): #if add breaklines interface is on
            if (self.num<2): ##if there are less than 2 points
                point = self.checkPoint(touch.x, touch.y, self.grid)
                if (point):
                    self.num += 1
                    self.points.append(point)
                if self.num == 2: ##When you have two points
                    pointTest = self.checkPoints(self.points[0], self.points[1], self.grid)
                    if (not pointTest): ##if the lines are on the border brekline (we dont want to remove this)
                        self.points = []
                        self.num = 0
                    else:
                        self.num = 0
                        ##Check that these breklines dont conflict with any current ones
                        blPoints = grid().getblPoints(self.grid)
                        for i in range(len(blPoints)):
                            if self.checkCross(blPoints[i][0], blPoints[i][1], self.points[0], self.points[1]):
                                self.points=[]
                                break
                        #add breaklines to list for undo
                        if self.points != []:
                            self.breaklines.append(self.points)
                        # add breaklines to grid
                        for j in range (len(self.points)//2):
                                
                            self.grid = grid().addBreakline(self.points[j*2], self.points[j*2+1], self.grid)
                    #recalculate grid and redraw breakline interface
                    self.grid = grid().setProps(self.grid)
                    self.grid = grid().detEdgecode(self.grid)
                    self.grid = grid().setBandNumber(self.grid)
                    self.clearCanvas()
                    self.printFinalKnot(self.grid, self.gridUnits,self.width2,  self.spacing,self.curve, self.offsetX, self.offsetY, self.cornerType)
                    self.drawAddBreakline(self.grid, self.gridUnits, self.offsetX, self.offsetY, self.width2, self.spacing, self.curve, self.cornerType)
                    self.printBreaklines(self.grid, self.gridUnits, self.offsetX, self.offsetY)
    

    
class MyKnotworkApp(App):

    def build(self):
        app = MyKnotworkWidget()
        self.grid = grid().createGrid(4,3)
        self.grid = grid().detEdgecode(self.grid)
        self.grid = grid().setBandNumber(self.grid)
        app.printGrid(self.grid, 50)
        app.printPoints(self.grid, 50)
        app.printBreaklines(self.grid, 50)
        app.printKnot(self.grid, 50, 10)
        return app

    
if __name__ == '__main__':
    MyKnotworkApp().run()

