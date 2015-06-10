# celtic-knotwork
An application for producing Celtic Knotwork on a square grid with 3D export functions


To run the software you need the Kivy Python library. Download it at: http://kivy.org/#download


Clone this repository, navigate to it in the terminal and run:

	```$kivy knotwork.py```

To run the main interface. To run the unit tests run:

	```$kivy tests.py```

To run the time tests (this may take a while) run:

	```$kivy timeTest.py```


# Documentation

Celtic Knotwork is a type of art style characterised by alternating weaving within a specified shape, this program produces Celtic Knotwork based on a square grid of an arbitrary size. The grid is divided into a sub-grid so a 4x4 knot is actually based on an 8x8 grid.

## Tabs

This program provides a tabbed interface so you can work on multiple apps at the same time. To add a tab click the “+” button in the right hand corner. The tab defaults to a 4x4 Knot.

## Left Menus

### Save (shortcut "ctrl"/"cmd"+"s")

Save the knotwork as a json array (you can save it in any format, and the program can load data in any format). (TODO describe structure of data)

### Load (shortcut "ctrl"/"cmd"+"o")

You can load a previously saved knot, any file extension is permissible

### Add Breaklines (shortcut “a”)

Add breadlines - breaklines are lines that the knot cannot cross, and are the main method of producing the knotwork patterns. You will be presented with a grid of Blue and red dots, you can connect any blue or red dots in a horizontal or vertical straight line, Blue and red breadlines cannot cross. To remove a breakline simply select the points on either end of it. Be sure to click Done (press “a”) when you are finished to finalise the breaklines

### Hide/Show Dots (shortcut "d")

Hides or shoes dots which indicate the primary (red) and secondary (blue) grids.

### Hide/Show Grid (shortcut "g")

Hides or shows the grid. The primary grid is in yellow and the secondary grid is in cyan

### Hide/Show Breaklines (shortcut "b")

Hides or shows breaklines, which are indicated in white

### Hide/Show Skeleton (shortcut "s")

Hides or shows the skeleton, the skeleton is a representation of the knot with just straight lines that can be useful if hand drawing the knotwork. Each band in the skeleton is randomly assigned a different colour.

### Hide/Show Knot (shortcut "k")

Hides or shows the final knot which is the knotwork displayed with curves and user-selected corners. Each band in the knot is randomly assigned a different colour.

## Right Menu

### X

The width of the knot, note that the secondary grid will be 2*X, hit enter to apply the change

### Y

The height of the knot, note the secondary grid will be 2*Y, hit enter to apply the change

### Grid Units

The size of each grid square in the secondary grid is grid_units*grid_units, note the primary grid will have grid size (2*grid_units)*(2*grid_units), hit enter to apply the change

### Width

This is the width of the knot, note the interface scales the displayed width based on the size of the window, hit enter to apply the change

### Corner

You can select from 3 corner options:
	Right Angle, 
	Curve, 
	Straight Line. 
The corners are immediately applied to the knotwork and are applied to the 3D output

### Output 3D (shortcut "o")

This allows you to output and STL file for 3D writing your knot. There are a number of options for customising your knot:

#### Width

This is the width of the rounded rectangle which is the cross section of the band, hit enter to apply the change to the displayed cross sections

#### Height

This is the height of the rounded rectangle which is the cross section of the band, hit enter to apply the change to the displayed cross sections

#### Radius

This is the radius of the corner of the rounded rectangle, set this to 0 for a normal rectangle and set Width = Height = 2*radius for a circle , hit enter to apply the change to the displayed cross sections

#### Num Triangles

The number of triangles that the corner is divided into, set this higher for a smoother curve, hit enter to apply the change to the displayed cross sections

#### Overlap

The distance between the centers of the rectangles, hit enter to apply the change to the displayed cross sections

#### Num cylinders

The number of slices in each grid position, set this higher to get smoother curves

#### Cancel

Close popup

#### Plot Template 

Plots an example of the cross sections above the inputs 

#### Save

Opens a save dialogue which lets you select a location to write the still file to. Note the file is automatically appended with “.stl” so putting an extension will be redundant but not disallowed 