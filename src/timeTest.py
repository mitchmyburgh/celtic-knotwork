import datetime
import time

from grid import *
from UI import *
from printSTL import *


##Instatiate the objects used to create the grid and generate the 3d points
gridFun = grid()
app = MyKnotworkWidget()

##run a test by generating a rxc grid
##r = number of rows
##c = number of columns
def testGrid(r, c):
    grid=[]
    time1 = time.clock()
    grid = gridFun.createGrid(r,c)
    grid = gridFun.detEdgecode(grid)
    grid = gridFun.setBandNumber(grid)
    time2 = time.clock()
    return time2-time1

##run n tests generating a rxc grid
##n = number of tests
##r = number of rows
##c = number of columns
def testGridMult(n, r, c):
    print("starting test Grid "+str(r)+"x"+str(c))
    time = []
    for i in range(n):
        time.append(testGrid(r, c))
        print("Trial "+str(i)+" Complete")
    #write data to file (down one column because excel is being weird)
    file = open("timeGrid"+str(r)+"x"+str(c)+".csv", "w")
    text =""
    for i in range (len(time)):
        text+=str(time[i])
        if (i%10 == 0 and not i==0):
            text +="\n"
        else:
            text+="\n"
    file.write(text)
    file.close()
    print("Done")

##run a test generating a 3D image of grid
##grid = grid from which 3d will be generated
def test3d(grid):
    time1 = time.clock()
    points = app.getKnotPointsbyBand(grid,10, 50, 10, 100, 0, 11)
    genCyl3(points, 10, 20, 3, 10, "test")
    time2 = time.clock()
    return time2-time1
##run n tests generating 3d model of rxc grid
##n = number of tests
##r = number of rows
##c = number of columns
def test3dMult(n, r, c):
    
    grid = gridFun.createGrid(r,c)
    grid = gridFun.detEdgecode(grid)
    grid = gridFun.setBandNumber(grid)
    print("starting test 3D"+str(r)+"x"+str(c))
    time = []
    for i in range(n):
        time.append(test3d(grid))
        print("Trial "+str(i)+" Complete")
    file = open("time3d"+str(r)+"x"+str(c)+".csv", "w")
    text =""
    for i in range (len(time)):
        text+=str(time[i])
        if (i%10 == 0 and not i==0):
            text +="\n"
        else:
            text+="\n"
    file.write(text)
    file.close()
    print("Done")
    
    


if __name__ == "__main__":
##    testGridMult(100, 100, 100)
##    testGridMult(100, 50, 50)
##    testGridMult(100, 10, 10)
##    testGridMult(100, 4, 4)
####    test3dMult(100, 100, 100)
##    
##    test3dMult(100, 10, 10)
##    test3dMult(100, 4, 4)
    test3dMult(3, 50, 50)
