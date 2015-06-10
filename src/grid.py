class grid():
    '''Creates and manages the grid data'''
    
    def createGrid (self, x,y):
        '''Creates a grid of size 2*x by 2*y'''
        #Stores the grid data
        data = []
        #stores the breaklines for undo/redo
        self.blPoints = []
        for i in range (2*y):
            data.append([])
            for j in range (2*x):
                data[i].append({})
                # Add data to cells
                data[i][j]["breakline"] = {"1":False, "2":False, "3":False, "4":False} #top, right, bottom, left
                data[i][j]["visited"] = False
                data[i][j]["bandnumber"] = 0 #specify different bands with different colours
                data[i][j]["edgecode"] = {"from":0, "to": 0} #the two points the part of the knot connects from 1 (top right corner) to 8
                data[i][j]["corner"] = False
                data[i][j]["cornerNumber"] = -1 #not a corner else corners are numbered from 0 (top right) to 3
                data[i][j]["border"] = False

                #add breaklines along the border
                if (i == 0): #top row
                    data[i][j]["breakline"]["1"] = True
                elif (i == 2*y-1): #bottom row
                    data[i][j]["breakline"]["3"] = True
                if (j == 0): #leftmost col
                    data[i][j]["breakline"]["4"] = True
                elif (j == 2*x-1): #rightmost col
                    data[i][j]["breakline"]["2"] = True
        #set properties before returning
        return self.setProps(data)

    def detEdgecode (self, data):
        '''Set the edgecodes, which determine the points the knot joins in the cell, modifies and returns data created from createGrid()'''
        flip = 1
        #Flip the direction of the line for every cell
        for i in range (len(data)):
            if (i%2 == 0): #even rows
                flip = 1
            else:
                flip = 0
            for j in range (len(data[0])):
                if (data[i][j]["breakline"]["3"] and data[i][j]["breakline"]["2"]):
                    data[i][j]["edgecode"]["from"] = 6
                    data[i][j]["edgecode"]["to"] = 8
                elif (data[i][j]["breakline"]["1"] and data[i][j]["breakline"]["4"]):
                    data[i][j]["edgecode"]["from"] = 4
                    data[i][j]["edgecode"]["to"] = 2
                elif (data[i][j]["breakline"]["2"] and data[i][j]["breakline"]["4"]):
                    data[i][j]["edgecode"]["from"] = 4
                    data[i][j]["edgecode"]["to"] = 8
                elif (data[i][j]["breakline"]["1"] and data[i][j]["breakline"]["3"]):
                    data[i][j]["edgecode"]["from"] = 6
                    data[i][j]["edgecode"]["to"] = 2
                elif (data[i][j]["breakline"]["1"] and data[i][j]["breakline"]["3"]):
                    data[i][j]["edgecode"]["from"] = 6
                    data[i][j]["edgecode"]["to"] = 2
                elif (data[i][j]["breakline"]["1"] and data[i][j]["breakline"]["2"]):
                    data[i][j]["edgecode"]["from"] = 6
                    data[i][j]["edgecode"]["to"] = 4
                elif (data[i][j]["breakline"]["3"] and data[i][j]["breakline"]["4"]):
                    data[i][j]["edgecode"]["from"] = 8
                    data[i][j]["edgecode"]["to"] = 2
                elif (data[i][j]["breakline"]["1"]):
                    if (flip == 1):
                        data[i][j]["edgecode"]["from"] = 5
                        data[i][j]["edgecode"]["to"]= 2
                    else:
                        data[i][j]["edgecode"]["from"] = 6
                        data[i][j]["edgecode"]["to"]= 3
                elif (data[i][j]["breakline"]["2"]):
                    if (flip == 1):
                        data[i][j]["edgecode"]["from"] = 5
                        data[i][j]["edgecode"]["to"]= 8
                    else:
                        data[i][j]["edgecode"]["from"] = 7
                        data[i][j]["edgecode"]["to"]= 4
                elif (data[i][j]["breakline"]["3"]):
                    if (flip == 1):
                        data[i][j]["edgecode"]["from"] = 6
                        data[i][j]["edgecode"]["to"]= 1
                    else:
                        data[i][j]["edgecode"]["from"] = 2
                        data[i][j]["edgecode"]["to"]= 7
                elif (data[i][j]["breakline"]["4"]):
                    if (flip == 1):
                        data[i][j]["edgecode"]["from"] = 4
                        data[i][j]["edgecode"]["to"]= 1
                    else:
                        data[i][j]["edgecode"]["from"] = 8
                        data[i][j]["edgecode"]["to"]= 3                   
                elif (not (data[i][j]["breakline"]["1"] and data[i][j]["breakline"]["2"] and data[i][j]["breakline"]["3"] and data[i][j]["breakline"]["1"])):
                    if (flip == 1):
                        data[i][j]["edgecode"]["from"] = 5
                        data[i][j]["edgecode"]["to"]= 1
                    else:
                        data[i][j]["edgecode"]["from"] = 7
                        data[i][j]["edgecode"]["to"]= 3
                
                if (flip == 1):
                    flip = 0 #odd positions
                else:
                    flip = 1 #even positions
        return data
		
    def getNextBlock(self, x, y, ec):
        '''Get the next block from x, y in the band according to the edgecode'''
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

    def getNextEdgecode(self, ec):
        '''Get the edgecode "from" that corresponds to a given "to"'''
        if ec == 1:
            return 5
        elif ec == 2:
            return 6
        elif ec == 3:
            return 7
        elif ec == 4:
            return 8
        elif ec == 5:
            return 1
        elif ec == 6:
            return 2
        elif ec == 7:
            return 3
        elif ec == 8:
            return 4

    def resetVisited(self, data):
        '''Reset all cells to be unvisited'''
        for i in range(len(data)):
            for j in range(len(data[0])):
                    data[i][j]["visited"] = False
        return data
                    
                
    def setBandNumber(self, data):
        '''Set band numbers for each band to allow different coloured bands'''
        bandnumber = 0
        data = self.resetVisited(data) #set all cells to unvisited
        for i in range(len(data)):
            for j in range(len(data[0])):
                if (data[i][j]["visited"] == False): #find first unvisited block
                    co = self.getNextBlock(j, i, data[i][j]["edgecode"]["to"])
                    data[i][j]["visited"] = True
                    data[i][j]["bandnumber"] = bandnumber
                    ec = data[i][j]["edgecode"]["to"]

                    while (data[co[1]][co[0]]["visited"] == False): #loop over band

                        if (data[co[1]][co[0]]["edgecode"]["to"] == self.getNextEdgecode(ec)): #switch edgecodes so to always has corresponding from
                            temp = data[co[1]][co[0]]["edgecode"]["to"]
                            data[co[1]][co[0]]["edgecode"]["to"] = data[co[1]][co[0]]["edgecode"]["from"]
                            data[co[1]][co[0]]["edgecode"]["from"] = temp
                            
                        data[co[1]][co[0]]["bandnumber"] = bandnumber
                        data[co[1]][co[0]]["visited"] = True

                        ec = data[co[1]][co[0]]["edgecode"]["to"] #store to from previous cell
                        co = self.getNextBlock(co[0], co[1], data[co[1]][co[0]]["edgecode"]["to"]) #get next cell
                        

                    bandnumber +=1
        return data
                    


    def addBreakline(self, point1, point2, data):
        '''Flips breaklines between point1 and point2 in the data matrix'''

        if (point1[0] == point2[0]): #x's are the same
            if (point1[1]< point2[1]):
                for i in range(point2[1]-point1[1]):
                    if (point1[0] == len(data[0])):
                        data[point1[1]+i][point1[0]-1]["breakline"]["2"] = not data[point1[1]+i][point1[0]-1]["breakline"]["2"]
                    else:                   
                        data[point1[1]+i][point1[0]]["breakline"]["4"] = not data[point1[1]+i][point1[0]]["breakline"]["4"]
                    if (not point1[0] == 0):
                        data[point1[1]+i][point1[0]-1]["breakline"]["2"] = not data[point1[1]+i][point1[0]-1]["breakline"]["2"]

            else:
                for i in range(point1[1]-point2[1]):
                    if (point1[0] == len(data[0])):
                        data[point2[1]+i][point1[0]-1]["breakline"]["2"] = not data[point2[1]+i][point1[0]-1]["breakline"]["2"]
                    else:                   
                        data[point2[1]+i][point1[0]]["breakline"]["4"] = not data[point2[1]+i][point1[0]]["breakline"]["4"]
                    if (not point1[0] == 0):
                        data[point2[1]+i][point1[0]-1]["breakline"]["2"] = not data[point2[1]+i][point1[0]-1]["breakline"]["2"]
        elif (point1[1] == point2[1]): #y's are the same
            if (point1[0]< point2[0]):
                for i in range(point2[0]-point1[0]):
                    if (point1[1] == len(data)):
                        data[point1[1]-1][point1[0]+i]["breakline"]["3"] = not data[point1[1]-1][point1[0]+i]["breakline"]["3"]
                    else:                   
                        data[point1[1]][point1[0]+i]["breakline"]["1"] = not data[point1[1]][point1[0]+i]["breakline"]["1"]
                    if (not point1[1] == 0):
                        data[point1[1]-1][point1[0]+i]["breakline"]["3"] = not data[point1[1]-1][point1[0]+i]["breakline"]["3"]

            else:
                for i in range(point1[0]-point2[0]):
                    if (point1[1] == len(data)):
                        data[point1[1]-1][point2[0]+i]["breakline"]["3"] = not data[point1[1]-1][point2[0]+i]["breakline"]["3"]
                    else:                   
                        data[point1[1]][point2[0]+i]["breakline"]["1"] = not data[point1[1]][point2[0]+i]["breakline"]["1"]
                    if (not point1[1] == 0):
                        data[point1[1]-1][point2[0]+i]["breakline"]["3"] = not data[point1[1]-1][point2[0]+i]["breakline"]["3"]
        else:
            print("error")
        #return the matrix with properties set
        return self.setProps(data)
    
    def getblPoints(self, data):
        '''Get all the breaklines in data divided into one cell long lengths (for easy processing) NOTE repeats breaklines, but everything else works regardless'''
        self.blPoints =[]
        for i in range(len(data)):
            for j in range(len(data[0])):
                if (data[i][j]["breakline"]["1"]):
                    self.blPoints.append([[j,i], [j+1, i]])
                if (data[i][j]["breakline"]["2"]):
                    self.blPoints.append([[j+1,i], [j+1, i+1]])
                if (data[i][j]["breakline"]["3"]):
                    self.blPoints.append([[j,i+1], [j+1, i+1]])
                if (data[i][j]["breakline"]["4"]):
                    self.blPoints.append([[j,i], [j, i+1]])
        return self.blPoints


    def setProps(self, data):
        '''Set properties of data: whether elements are border or corner and their corner number'''
        for i in range(len(data)):
            for j in range(len(data[0])):
                if ((data[i][j]["breakline"]["1"] and data[i][j]["breakline"]["2"]) or (data[i][j]["breakline"]["2"] and data[i][j]["breakline"]["3"]) or (data[i][j]["breakline"]["3"] and data[i][j]["breakline"]["4"]) or (data[i][j]["breakline"]["4"] and data[i][j]["breakline"]["1"])):
                    data[i][j]["corner"] = True
                    data[i][j]["border"] = False
                elif ((data[i][j]["breakline"]["1"] and not (data[i][j]["breakline"]["2"] and data[i][j]["breakline"]["3"] and data[i][j]["breakline"]["4"])) or (data[i][j]["breakline"]["2"] and not (data[i][j]["breakline"]["1"] and data[i][j]["breakline"]["3"] and data[i][j]["breakline"]["4"])) or (data[i][j]["breakline"]["3"] and not (data[i][j]["breakline"]["2"] and data[i][j]["breakline"]["1"] and data[i][j]["breakline"]["4"])) or (data[i][j]["breakline"]["4"] and not (data[i][j]["breakline"]["2"] and data[i][j]["breakline"]["3"] and data[i][j]["breakline"]["1"]))):
                    data[i][j]["border"] = True
                    data[i][j]["corner"] = False
                else:
                    data[i][j]["corner"] = False
                    data[i][j]["border"] = False

                if ((data[i][j]["breakline"]["1"] and data[i][j]["breakline"]["2"])):
                    data[i][j]["cornerNumber"] = 0
                elif ((data[i][j]["breakline"]["2"] and data[i][j]["breakline"]["3"])):
                    data[i][j]["cornerNumber"] = 1
                elif (data[i][j]["breakline"]["3"] and data[i][j]["breakline"]["4"]):
                    data[i][j]["cornerNumber"] = 2
                elif (data[i][j]["breakline"]["4"] and data[i][j]["breakline"]["1"]):
                    data[i][j]["cornerNumber"] = 3
        #returns the modified data
        return data

    
                
        







                
        
