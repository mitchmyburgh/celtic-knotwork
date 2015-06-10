import unittest

##Import files for testing
from grid import *
from UI import *
from printSTL import *

class Test(unittest.TestCase):

    ##Tests for grid.py
    ##Check correct sized grid is returned for various inputs
    def test_grid_size(self):
        self.assertEqual(len(grid().createGrid(4, 4)), 8)
        self.assertEqual(len(grid().createGrid(4, 4)[0]), 8)
    def test_grid_0(self):
        self.assertEqual(len(grid().createGrid(0, 0)), 0)
    def test_grid_neg(self):
        self.assertEqual(len(grid().createGrid(-10, -10)), 0)
    ##Test all types of data in grid are correct
    def test_grid_types_quick(self):
        self.assertEqual(type(grid().createGrid(4, 4)), list)
        self.assertEqual(type(grid().createGrid(4, 4)[0]), list)
        self.assertEqual(type(grid().createGrid(4, 4)[0][0]), dict)
    def test_grid_types_all(self):
        self.grid = grid().createGrid(4, 4)
        self.assertEqual(type(self.grid), list)
        for i in self.grid:
            self.assertEqual(type(i), list)
            for j in i:
                self.assertEqual(type(j), dict)
    ##Check Breaklines on base grid
    def test_grid_breaklines(self):
        self.grid = grid().createGrid(4, 4)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if (i == 0 and j == 0):
                    self.assertEqual(self.grid[i][j]["breakline"]["1"], True)
                    self.assertEqual(self.grid[i][j]["breakline"]["2"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["3"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["4"], True)
                elif (i == 0 and j == len(self.grid[i]) - 1):
                    self.assertEqual(self.grid[i][j]["breakline"]["1"], True)
                    self.assertEqual(self.grid[i][j]["breakline"]["2"], True)
                    self.assertEqual(self.grid[i][j]["breakline"]["3"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["4"], False)
                elif (i == len(self.grid)-1 and j == 0):
                    self.assertEqual(self.grid[i][j]["breakline"]["1"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["2"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["3"], True)
                    self.assertEqual(self.grid[i][j]["breakline"]["4"], True)
                elif (i == len(self.grid)-1 and j == len(self.grid[i]) - 1):
                    self.assertEqual(self.grid[i][j]["breakline"]["1"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["2"], True)
                    self.assertEqual(self.grid[i][j]["breakline"]["3"], True)
                    self.assertEqual(self.grid[i][j]["breakline"]["4"], False) 
                elif (i == 0):
                    self.assertEqual(self.grid[i][j]["breakline"]["1"], True)
                    self.assertEqual(self.grid[i][j]["breakline"]["2"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["3"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["4"], False)
                elif (i == len(self.grid)-1):
                    self.assertEqual(self.grid[i][j]["breakline"]["1"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["2"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["3"], True)
                    self.assertEqual(self.grid[i][j]["breakline"]["4"], False)
                elif (j == 0):
                    self.assertEqual(self.grid[i][j]["breakline"]["1"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["2"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["3"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["4"], True)
                elif (j == len(self.grid[i]) - 1):
                    self.assertEqual(self.grid[i][j]["breakline"]["1"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["2"], True)
                    self.assertEqual(self.grid[i][j]["breakline"]["3"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["4"], False)
                else:
                    self.assertEqual(self.grid[i][j]["breakline"]["1"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["2"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["3"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["4"], False)
    ##Test the generated edgecodes
    def test_edgecode(self):
        self.grid = grid().createGrid(4, 4)
        self.grid = grid().detEdgecode(self.grid)
        ##just check edgecodes on corners
        self.assertEqual(self.grid[0][0]["edgecode"]["to"], 2)
        self.assertEqual(self.grid[0][0]["edgecode"]["from"], 4)
        self.assertEqual(self.grid[7][7]["edgecode"]["to"], 8)
        self.assertEqual(self.grid[7][7]["edgecode"]["from"], 6)
        self.assertEqual(self.grid[0][7]["edgecode"]["to"], 4)
        self.assertEqual(self.grid[0][7]["edgecode"]["from"], 6)
        self.assertEqual(self.grid[7][0]["edgecode"]["to"], 2)
        self.assertEqual(self.grid[7][0]["edgecode"]["from"], 8)
    ##Test the number of bands generated
    def test_bandnumber(self):
        self.grid = grid().createGrid(4, 4)
        self.grid = grid().detEdgecode(self.grid)
        self.grid = grid().setBandNumber(self.grid)
        bandnumbers = []
        for i in self.grid:
            for j in i:
                bandnumbers.append(j["bandnumber"])
        self.assertEqual(max(bandnumbers), 3)
    ##Test adding breaklines
    def test_add_breakline(self):
        self.grid = grid().createGrid(4, 4)
        self.grid = grid().detEdgecode(self.grid)
        self.grid = grid().setBandNumber(self.grid)
        
        self.grid = grid().addBreakline([2, 0],[2, 4], self.grid)

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if (i>0 and i<4 and j == 1):
                    self.assertEqual(self.grid[i][j]["breakline"]["1"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["2"], True)
                    self.assertEqual(self.grid[i][j]["breakline"]["3"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["4"], False)
                elif (i ==0 and j ==1):
                    self.assertEqual(self.grid[i][j]["breakline"]["1"], True)
                    self.assertEqual(self.grid[i][j]["breakline"]["2"], True)
                    self.assertEqual(self.grid[i][j]["breakline"]["3"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["4"], False)
                elif (i>0 and i<4 and j == 2):
                    self.assertEqual(self.grid[i][j]["breakline"]["1"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["2"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["3"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["4"], True)
                elif (i ==0 and j ==2):
                    self.assertEqual(self.grid[i][j]["breakline"]["1"], True)
                    self.assertEqual(self.grid[i][j]["breakline"]["2"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["3"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["4"], True)                   
                elif (i == 0 and j == 0):
                    self.assertEqual(self.grid[i][j]["breakline"]["1"], True)
                    self.assertEqual(self.grid[i][j]["breakline"]["2"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["3"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["4"], True)
                elif (i == 0 and j == len(self.grid[i]) - 1):
                    self.assertEqual(self.grid[i][j]["breakline"]["1"], True)
                    self.assertEqual(self.grid[i][j]["breakline"]["2"], True)
                    self.assertEqual(self.grid[i][j]["breakline"]["3"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["4"], False)
                elif (i == len(self.grid)-1 and j == 0):
                    self.assertEqual(self.grid[i][j]["breakline"]["1"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["2"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["3"], True)
                    self.assertEqual(self.grid[i][j]["breakline"]["4"], True)
                elif (i == len(self.grid)-1 and j == len(self.grid[i]) - 1):
                    self.assertEqual(self.grid[i][j]["breakline"]["1"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["2"], True)
                    self.assertEqual(self.grid[i][j]["breakline"]["3"], True)
                    self.assertEqual(self.grid[i][j]["breakline"]["4"], False) 
                elif (i == 0):
                    self.assertEqual(self.grid[i][j]["breakline"]["1"], True)
                    self.assertEqual(self.grid[i][j]["breakline"]["2"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["3"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["4"], False)
                elif (i == len(self.grid)-1):
                    self.assertEqual(self.grid[i][j]["breakline"]["1"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["2"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["3"], True)
                    self.assertEqual(self.grid[i][j]["breakline"]["4"], False)
                elif (j == 0):
                    self.assertEqual(self.grid[i][j]["breakline"]["1"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["2"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["3"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["4"], True)
                elif (j == len(self.grid[i]) - 1):
                    self.assertEqual(self.grid[i][j]["breakline"]["1"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["2"], True)
                    self.assertEqual(self.grid[i][j]["breakline"]["3"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["4"], False)
                else:
                    self.assertEqual(self.grid[i][j]["breakline"]["1"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["2"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["3"], False)
                    self.assertEqual(self.grid[i][j]["breakline"]["4"], False)
    ##Test getting breaklines (make sure all breaklines are there)
    def test_get_breaklines(self):
        self.grid = grid().createGrid(4, 4)
        self.grid = grid().detEdgecode(self.grid)
        self.grid = grid().setBandNumber(self.grid)
        
        self.grid = grid().addBreakline([2, 0],[2, 4], self.grid)
        bls = grid().getblPoints(self.grid)
        for i in range(8):
            self.assertEqual([[i, 0], [i+1, 0]] in bls, True)
            self.assertEqual([[0, i], [0, i+1]] in bls, True)
            self.assertEqual([[i, 8], [i+1, 8]] in bls, True)
            self.assertEqual([[8, i], [8, i+1]] in bls, True)
        for i in range(4):
            self.assertEqual([[2, i], [2, i+1]] in bls, True)
    ##Tests for UI.py - not many because this deals with displaying the knot
    ##Test the function getKnotPointsByBand
    def test_getKnotPointsByBand(self):
        self.grid = grid().createGrid(4, 4)
        self.grid = grid().detEdgecode(self.grid)
        self.grid = grid().setBandNumber(self.grid)
        ##Initialise the app
        app = MyKnotworkWidget()
        points = app.getKnotPointsbyBand(self.grid,10, 50, 10, 100, 0, 11)
        ##Test number of bands
        self.assertEqual(len(points), 4)
        ##check types
        for i in points:
            self.assertEqual(type(i), list)
            for j in i:
                self.assertEqual(type(j), list)
                self.assertEqual(len(j), 8)
    ##Test the function checkCross
    def test_checkCross(self):
        ##Initialise the app
        app = MyKnotworkWidget()
        self.assertEqual(app.checkCross([1,1], [1,3], [0,2], [2,2]), True)
        self.assertEqual(app.checkCross([1,1], [1,2], [0,2], [2,2]), True)
        self.assertEqual(app.checkCross([1,0], [1,1], [0,2], [2,2]), False)

    ##Tests for knotwork.py
    ##No tests here because this is only for the UI

    ##Tests for printSTL.py
    ##a few functions in this file were just for testing so i didnt test them
    ##test the function genRoundedRectanglePoints
    def test_genRoundedRectanglePoints(self):
        points = genRoundedRectanglePoints(1,2, 10, 10, 3, 4)
        self.assertEqual(len(points), 6+4*4)
        self.assertEqual(type(points), list)
        for i in points:
            self.assertEqual(len(i), 4)
            self.assertEqual(type(i), list)
    ##test the function rotatePoints
    def test_rotatePoints(self):
        points = rotatePoints(1,2,3, 1,1,1,0,0,0)
        self.assertEqual(len(points), 3)
        self.assertEqual(type(points), list)
        points = rotatePoints(0,0,0, 1,1,1,0,0,0)
        self.assertEqual(points[0], 0)
        self.assertEqual(points[1], 0)
        self.assertEqual(points[2], 0)
        
    ##test the function genRoundedRectanglePointsRotate
    def test_genRoundedRectanglePointsRotate(self):
        points = genRoundedRectanglePointsRotate(1,2, 10, 10, 3, 4, 1, 1, 1)
        self.assertEqual(len(points), 6+4*4)
        self.assertEqual(type(points), list)
        for i in points:
            self.assertEqual(len(i), 4)
            self.assertEqual(type(i), list)
    ##test the function genRoundedRectanglePointsRotateSkel
    def test_genRoundedRectanglePointsRotateSkel(self):
        points = genRoundedRectanglePointsRotateSkel(1,2, 10, 10, 3, 4, 1, 1, 1)
        self.assertEqual(len(points), 4*4)
        self.assertEqual(type(points), list)
        for i in points:
            self.assertEqual(len(i), 4)
            self.assertEqual(type(i), list)
    
                
                
            


if __name__ == '__main__':
    unittest.main()
