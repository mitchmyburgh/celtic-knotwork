from __future__ import division

'''Kivy Imports'''
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelHeader
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.graphics import *
from kivy.uix.checkbox import CheckBox

'''Python Imports'''
import math
import datetime
import math
import re

'''Imports from other places in the software'''
from UI import *
from grid import *
from printSTL import *
import simplejson

##KV language representation of the save dialogue
savDia = '''<SaveDialog>:
    text_input: text_input
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserListView:
            id: filechooser
            on_selection: text_input.text = self.selection and self.selection[0] or ''

        TextInput:
            id: text_input
            size_hint_y: None
            height: 30
            multiline: False

        BoxLayout:
            size_hint_y: None
            height: 30
            Button:
                text: "Cancel"
                on_release: root.cancel()

            Button:
                text: "Save"
                on_press: root.save(filechooser.path, text_input.text)'''

##KV language representation of the load dialogue
loadDia = '''<LoadDialog>:
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserListView:
            id: filechooser

        BoxLayout:
            size_hint_y: None
            height: 30
            Button:
                text: "Cancel"
                on_release: root.cancel()

            Button:
                text: "Load"
                on_release: root.load(filechooser.path, filechooser.selection)'''

##KV language representation of the corner buttons (necessary to get images nicely)
cornerBUT = '''
<CornerButtons>:
    BoxLayout:
        Button:
            on_press: root.b1()
            Image:
                source: "corner1.PNG"
                center_x: self.parent.center_x
                center_y: self.parent.center_y
                allow_stretch: True
                size: 25, 25
        Button:
            on_press: root.b2()
            Image:
                source: "corner2.PNG"
                center_x: self.parent.center_x
                center_y: self.parent.center_y
                allow_stretch: True
                size: 25, 25
            
            '''

##KV language representation of the load/save buttons (necessary to get images nicely)
loadSave = '''
<LoadSaveButtons>:
    BoxLayout:
        Button:
            on_press: root.save()
            Image:
                source: "save.PNG"
                center_x: self.parent.center_x
                center_y: self.parent.center_y
                allow_stretch: True
                size: 25, 25
        Button:
            on_press: root.load()
            Image:
                source: "load.PNG"
                center_x: self.parent.center_x
                center_y: self.parent.center_y
                allow_stretch: True
                size: 25, 25
            
            '''

##KV language representation of the output 3D dialogue
output3DTemp = '''
<output3DPopup>:
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        BoxLayout:
            id: canvas3D_holder
            size_hint: 1, 0.79
            canvas:
                Rectangle:
                    pos: 200,200
                    size: 10,10
        BoxLayout:
            size_hint: 1, 0.07
            Label:
                text: "Width"
            TextInput:
                id: width_3d_input
                text: "10"
                multiline: False
                on_text_validate: root.plot(width_3d_input, height_3d_input,radius_3d_input,tri_3d_input,overlap_3d_input, cyl_3d_input)
            Label:
                text: "Height"
            TextInput:
                id: height_3d_input
                text: "20"
                multiline: False
                on_text_validate: root.plot(width_3d_input, height_3d_input,radius_3d_input,tri_3d_input,overlap_3d_input, cyl_3d_input)
            Label:
                text: "Radius"
            TextInput:
                id: radius_3d_input
                text: "3"
                multiline: False
                on_text_validate: root.plot(width_3d_input, height_3d_input,radius_3d_input,tri_3d_input,overlap_3d_input, cyl_3d_input)
        BoxLayout:
            size_hint: 1, 0.07
            Label:
                text: "Corner Smoothness"
            TextInput:
                id: tri_3d_input
                text: "10"
                multiline: False
                on_text_validate: root.plot(width_3d_input, height_3d_input,radius_3d_input,tri_3d_input,overlap_3d_input, cyl_3d_input)
            Label:
                text: "Overlap"
            TextInput:
                id: overlap_3d_input
                text: "11"
                multiline: False
                on_text_validate: root.plot(width_3d_input, height_3d_input,radius_3d_input,tri_3d_input,overlap_3d_input, cyl_3d_input)
            Label:
                text: "3D Smoothness"
            TextInput:
                id: cyl_3d_input
                text: "10"
                multiline: False
                on_text_validate: root.plot(width_3d_input, height_3d_input,radius_3d_input,tri_3d_input,overlap_3d_input, cyl_3d_input)
        BoxLayout:
            size_hint: 1, 0.07
            Button:
                on_press: root.cancel()
                text: "Cancel"
            Button:
                on_press:root.save(width_3d_input.text, height_3d_input.text,radius_3d_input.text,tri_3d_input.text,overlap_3d_input.text,cyl_3d_input.text)
                text: "Save"
'''
##KV language representation of the plot warning Dialogue
plotDia = '''<PlotDialog>:
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        Label:
            text: "You will lose your breaklines"
        BoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            height: 30
            Button:
                text: "Cancel"
                on_release: root.cancel()

            Button:
                text: "Plot"
                on_press: root.plot()'''


class SaveDialog(FloatLayout):
    '''Class for the save dialogue'''
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)
    Builder.load_string(savDia)

class LoadDialog(FloatLayout):
    '''Class for the Load dialogue'''
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    Builder.load_string(loadDia)

class PlotDialog(FloatLayout):
    '''Class for Plot warning dialogue (when you plot a new knot but will lose breaklines)'''
    plot = ObjectProperty(None)
    cancel = ObjectProperty(None)
    Builder.load_string(plotDia)

class CornerButtons(BoxLayout):
    '''Class for the corner buttons'''
    b1 = ObjectProperty(None)
    b2 = ObjectProperty(None)
    Builder.load_string(cornerBUT)

class LoadSaveButtons(BoxLayout):
    '''Class for the load/save buttons'''
    save = ObjectProperty(None)
    load = ObjectProperty(None)
    Builder.load_string(loadSave)

class output3DPopup(GridLayout):
    '''Class for the ouput 3D popup'''
    plot = ObjectProperty(None)
    cancel = ObjectProperty(None)
    save = ObjectProperty(None)

    def checkValue(self, val, default, flt, allowz):
        '''Check that val is a positive number, else set it to the absolute value or default. If flt then the number returned a a float (else trailing decimal places are removed). if allowz then val can be zero'''
        if len(val) == 0:
            if flt:
                return default
            else:
                return default
        if (not allowz and val == "0"):
            return default
        if val.isdigit():
            if flt:
                return float(val)
            else:
                return int(val)

        try:
            return int(math.sqrt(int(float(val))**2))
        except:
            pass
        
        return default
    
    def plot(self, width, height, radius, tri, overlap, cyl):
        '''Plots a template to show how the cross sections of 2 bands will look'''
        self.canvas.add(Color(0.3,0.3,0.3))
        self.canvas.add(Rectangle(size=(Window.width*0.9 - 10,Window.height*0.9-Window.height*0.9*0.21-50), pos=(Window.width*0.05 +5, Window.height*0.05 + Window.height*0.9*0.21))) #add background
        self.canvas.add(Color(1,0,0))

        ##Check values
        width.text = str(self.checkValue(width.text, 10.0, True, False))
        width = float(width.text)
        height.text = str(self.checkValue(height.text, 20.0, True, False))
        height = float(height.text)
        radius.text = str(self.checkValue(radius.text, 3.0, True, True))
        rad2 = float(radius.text)
        if (rad2 > height/2 or rad2 > width/2):
            rad2 = min(width/2, height/2)
        radius.text = str(rad2)
        radius = rad2
        tri.text = str(self.checkValue(tri.text, 10, False, False))
        tri = int(tri.text)
        overlap.text = str(self.checkValue(overlap.text, 11.0, True, True))
        overlap = float(overlap.text)
        cyl.text = str(self.checkValue(cyl.text, 10, False, False))
        cyl = float(cyl.text)
        
        ##Generate the cross sections
        ring1 = genRoundedRectanglePointsRotateSkel(Window.width/2, Window.height/2, 0, float(width)*10, float(height)*10, float(radius)*10, int(tri), 0, 0, 0)
        ring2 = genRoundedRectanglePointsRotateSkel(Window.width/2+float(overlap)*10, Window.height/2, 0, float(width)*10, float(height)*10, float(radius)*10, int(tri), 0, 0, 0)
        ##Dropthe z-values and close the loop
        points = []
        for i in ring1:
            points.append(i[0])
            points.append(i[1])
        points.append(ring1[0][0])
        points.append(ring1[0][1])
        points2 = []
        for i in ring2:
            points2.append(i[0])
            points2.append(i[1])
        points2.append(ring2[0][0])
        points2.append(ring2[0][1])

        ##Draw the cross sections
        self.canvas.add(Line(points = points, width = 3))
        self.canvas.add(Color(0,0,1))
        self.canvas.add(Line(points = points2, width = 3))
        self.canvas.add(Color(1,0,0))

    def plot2(self, width, height, radius, tri, overlap, cyl):
        '''Plots a template to show how the cross sections of 2 bands will look, allows for plotting with prechecked values (i.e. first plot)'''
        self.canvas.add(Color(0.3,0.3,0.3))
        self.canvas.add(Rectangle(size=(Window.width*0.9 - 10,Window.height*0.9-Window.height*0.9*0.21-50), pos=(Window.width*0.05 +5, Window.height*0.05 + Window.height*0.9*0.21)))#add background
        self.canvas.add(Color(1,0,0))
        ##Generate the cross sections
        ring1 = genRoundedRectanglePointsRotateSkel(Window.width/2, Window.height/2, 0, float(width)*10, float(height)*10, float(radius)*10, int(tri), 0, 0, 0)
        ring2 = genRoundedRectanglePointsRotateSkel(Window.width/2+float(overlap)*10, Window.height/2, 0, float(width)*10, float(height)*10, float(radius)*10, int(tri), 0, 0, 0)
        ##Dropthe z-values and close the loop
        points = []
        for i in ring1:
            points.append(i[0])
            points.append(i[1])
        points.append(ring1[0][0])
        points.append(ring1[0][1])
        points2 = []
        for i in ring2:
            points2.append(i[0])
            points2.append(i[1])
        points2.append(ring2[0][0])
        points2.append(ring2[0][1])
        ##Draw the cross sections
        self.canvas.add(Line(points = points, width = 3))
        self.canvas.add(Color(0,0,1))
        self.canvas.add(Line(points = points2, width = 3))
    
    Builder.load_string(output3DTemp)
    
    


    

class CelticKnotwork(App):
    '''Main tabbed interface, each tab contains its own instance of CelticKnotwork2'''
    def build(self):
        ##Instance Variables
        self.showDots = True
        self.showGrid = True
        self.showBreaklines = True
        self.showSkeleton = True
        self.showKnot = True
        self.knotX = 4
        self.knotY = 4
        self.knotWidth = 8
        self.knotWidthView = 8
        self.gridUnits = 50
        self.gridUnitsView = 50
        self.offsetX = 150
        self.offsetY = 50
        self.totTabs = 1
        self.tabNo = 1
        
        
        ##Main Layout
        self.layout_main = AnchorLayout(anchor_x = "left", anchor_y="top")
        self.layout_tabs= FloatLayout(size=(Window.width, Window.height), size_hint=(0.1, 0.08))

        
        ##Top Tab Bar - allowing multiple knots
        self.tp = TabbedPanel()
        self.tp.default_tab_text = "Knot 1"
        self.layout_main.add_widget(self.tp)
        self.addTab = TabbedPanelHeader(text='+')
        self.addTab.bind(on_release = self.onPressAddTab)
        self.addTab = Button(text='+', pos =(Window.width*.9,Window.height*.92))
        self.addTab.bind(on_press = self.onPressAddTab)
        self.tp.default_tab_content = CelticKnotwork2().build() #get tab content from CelticKnotwork2
        self.layout_tabs.add_widget(self.addTab)
        self.layout_main.add_widget(self.layout_tabs)

        Window.bind(on_resize=self.on_resize)

        
        
        return self.layout_main
    def onPressAddTab(self, instance):
        '''Add a tab when "+" button pressed'''
        self.totTabs += 1
        self.tabNo = self.totTabs
        self.th = TabbedPanelHeader(text='Knot '+str(self.totTabs))
        self.th.content = CelticKnotwork2().build()
        self.tp.add_widget(self.th)
        
        self.tp.switch_to(self.th)
    def on_resize(self, window, height, somethingesle):
        '''Handles window resize'''
        self.layout_main.remove_widget(self.layout_tabs)
        self.layout_tabs= FloatLayout(size=(Window.width, Window.height), size_hint=(0.1, 0.05))
        self.addTab = Button(text='+', pos =(Window.width*.9,Window.height*.95))
        self.addTab.bind(on_press = self.onPressAddTab)
        self.layout_tabs.add_widget(self.addTab)
        self.layout_main.add_widget(self.layout_tabs)

    
class CelticKnotwork2():
    '''The program content, each tab contains an instance of this'''
    def build(self):
        def checkValue(val, default, flt, allowz):
            '''Check that val is a positive number, else set it to the absolute value or default. If flt then the number returned a a float (else trailing decimal places are removed). if allowz then val can be zero'''
            if len(val) == 0:
                if flt:
                    return default
                else:
                    return default
            if (not allowz and val == "0"):
                return default
            if val.isdigit():
                if flt:
                    return float(val)
                else:
                    return int(val)

            try:
                return int(math.sqrt(int(float(val))**2))
            except:
                pass
            
            return default
                
        
        def plotButtonPressed(instance):
            '''Called on_text_validate when new text is entered in x, y, gridUnits, width. Redraws the knot'''
            plotKnotCheck()

        def plotKnotCheck():
            '''Check that no new breaklines have been addded (a warning is shown when you have breaklines that will be erased)'''
            if self.app.getAddedBLS():
                content = PlotDialog(cancel=dismiss_popup, plot=plotKnotAcc)#show warning
                self._popup = Popup(title="Plot new Knot", content=content, size_hint=(0.3, 0.3))
                self._popup.open()
            else:
                plotKnotAcc() #replot knot
                
            
        def plotKnotAcc():
            '''Replots the knot and validate any input'''
            try:
                dismiss_popup() #there may or may not be a popup
            except:
                pass
            self.app.clearCanvas()
            ##Validate datat
            self.gridUnits = checkValue(self.gridUnitsI.text, 50, False, False)
            self.gridUnitsI.text = str(self.gridUnits)
            self.X.text = str(checkValue(self.X.text, 4, False, False))
            self.Y.text = str(checkValue(self.Y.text, 4, False, False))
            self.WidthI.text = str(checkValue(self.WidthI.text, 8.0, True, False))
            
            #Create a new grid
            self.grid = grid().createGrid(int(self.X.text),int(self.Y.text))
            self.grid = grid().detEdgecode(self.grid)
            self.grid = grid().setBandNumber(self.grid)

            #set sizing so the knot doesnt cover interface elements
            self.knotX = int(self.X.text)*2
            self.knotY = int(self.Y.text)*2
            viewWidth = Window.width*0.52
            viewHeight = Window.height-110

            if ((viewWidth)/self.knotX < (viewHeight)/self.knotY):
                self.gridUnitsView = (viewWidth)/self.knotX
            else:
                self.gridUnitsView = (viewHeight)/self.knotY
            self.knotWidthView = (float(self.WidthI.text)/self.gridUnits)*self.gridUnitsView
            self.spacing = self.knotWidthView
            if self.knotWidthView < 1:
                self.knotWidthView = 1
            self.offsetX = Window.width*0.25 - self.gridUnitsView
            self.offsetY = Window.height*0.05 - self.gridUnitsView
            ##Print the new knot
            printKnot()
        
        def printKnot():
            '''Print knot (and additional elements such as the grid) based on various parameters'''
            self.app.clearCanvas()
            if (self.showDots):
                self.app.printPoints(self.grid, self.gridUnitsView, self.offsetX, self.offsetY)
            if (self.showGrid):
                self.app.printGrid(self.grid, self.gridUnitsView, self.offsetX, self.offsetY)
            if (self.showBreaklines):
                self.app.printBreaklines(self.grid, self.gridUnitsView, self.offsetX, self.offsetY)
            if (self.showSkeleton):
                self.app.printKnot(self.grid, self.gridUnitsView,2,  self.spacing,self.offsetX, self.offsetY)
            if (self.showKnot):
                time1 = datetime.datetime.now()
                self.app.printFinalKnot(self.grid, self.gridUnitsView,self.knotWidthView,  self.spacing,self.curve.value,self.offsetX, self.offsetY, self.cornerType)
                time2 = datetime.datetime.now()
                print("Time taken to draw knot: "+str(time2-time1)) #shows time taken to print the knot
                
        def toggleDotsPressed(instance, value):
            '''Toggles Dot display'''
            if (self.showDots):
                self.toggleDotsL.text = "Show (D)ots" #change label
                self.toggleDots.active = False #change value of checkbox (for keyboard input)
                self.showDots = False
            else:
                self.toggleDotsL.text = "Hide (D)ots"
                self.toggleDots.active = True
                self.showDots = True
            printKnot() #printKnot()
        
        def toggleGridPressed(instance, value):
            '''toggle grid display'''
            if (self.showGrid):
                self.toggleGridL.text = "Show (G)rid" #change label
                self.toggleGrid.active = False #change value of textbox (for keyboard input)
                self.showGrid = False
            else:
                self.toggleGridL.text = "Hide (G)rid"
                self.toggleGrid.active = True
                self.showGrid = True
            printKnot()
        
        def toggleBreaklinesPressed(instance, value):
            '''Toggle breaklines display'''
            if (self.showBreaklines):
                self.toggleBreaklinesL.text = "Show (B)reaklines" #change label
                self.toggleBreaklines.active = False #change value of textbox (for keyboard input)
                self.showBreaklines = False
            else:
                self.toggleBreaklinesL.text = "Hide (B)reaklines"
                self.toggleBreaklines.active = True
                self.showBreaklines = True
            printKnot()

        def toggleSkeletonPressed(instance, value):
            '''Toggle skeleton display'''
            if (self.showSkeleton):
                self.toggleSkeletonL.text = "Show (S)keleton" #change label
                self.toggleSkeleton.active = False #change value of textbox (for keyboard input)
                self.showSkeleton = False
            else:
                self.toggleSkeletonL.text = "Hide (S)keleton"
                self.toggleSkeleton.active = True
                self.showSkeleton = True
            printKnot()
            
        def toggleKnotPressed(instance, value):
            '''Toggle final knot display'''
            if (self.showKnot):
                self.toggleKnotL.text = "Show (K)not" #change label
                self.toggleKnot.active = False #change value of textbox (for keyboard input)
                self.showKnot = False
            else:
                self.toggleKnotL.text = "Hide (K)not"
                self.toggleKnot.active = True
                self.showKnot = True
            printKnot()
        
        def addBreaklinePressed(instance):
            '''Start the add breaklines interface'''
            self.addBreakline.unbind(on_press=addBreaklinePressed)
            self.addBreakline.bind(on_press=addBreaklinePressed2)
            self.addBreakline.text="(A) Done"#Change text label
            self.app.setOnBreaklines(True)
            ##Check values
            if (self.WidthI.text[0] == "-"):
                self.WidthI.text = self.WidthI.text[1:]
            if re.search('[a-zA-Z]+',self.WidthI.text):
                self.WidthI.text = "8"
            ##start draw breaklines interface
            self.app.drawAddBreakline(self.grid, self.gridUnitsView, self.offsetX, self.offsetY, self.knotWidthView,  self.spacing,self.curve.value, self.cornerType)

        def addBreaklinePressed2(instance):
            '''End the add breaklines interface'''
            self.addBreakline.unbind(on_press=addBreaklinePressed2)
            self.addBreakline.text="(A)dd Breaklines"
            ##reset grid properties
            self.grid = grid().detEdgecode(self.grid)
            self.grid = grid().setBandNumber(self.grid)
            printKnot()
            self.app.setOnBreaklines(False)
            self.addBreakline.bind(on_press=addBreaklinePressed)
            
        def output3DPressed(instance):
            '''Output 3D button pressed'''
            #unbind keyboard shortcuts
            try:
                self._keyboard.unbind(on_key_down=_on_keyboard_down)
                self._keyboard = None
            except:
                pass
            #display config popup
            content = output3DPopup(cancel=dismiss_popup, save=savePressed3D)
            content.plot2(10, 20, 3, 10, 11, 10)
            self._popup = Popup(title="Output 3D", content=content, size_hint=(0.9, 0.9))

            
            
            self._popup.open()

        def cornerButton1Pressed():
            '''Set corner type to 0 (right angle)'''
            self.cornerType = 0
            printKnot()
        def cornerButton2Pressed():
            '''Set corner type to 1 (curve)'''
            self.cornerType = 1
            printKnot()
            
        def on_resize(window, height, somethingesle):
            '''Called on window resize - sets size of knot to fit within screen'''
            self.knotX = int(self.X.text)*2
            self.knotY = int(self.Y.text)*2
            viewWidth = window.width*0.52
            viewHeight = window.height-110

            if ((viewWidth)/self.knotX < (viewHeight)/self.knotY):
                self.gridUnitsView = (viewWidth)/self.knotX
            else:
                self.gridUnitsView = (viewHeight)/self.knotY

            self.knotWidthView = (float(self.WidthI.text)/self.gridUnits)*self.gridUnitsView
            self.spacing = self.knotWidthView
            if self.knotWidthView < 1:
                self.knotWidthView = 1
            self.offsetX = window.width*0.25 - self.gridUnitsView
            self.offsetY = window.height*0.05 - self.gridUnitsView
            printKnot()
        def savePressed3D(width, height, radius, tri, overlap, cyl):
            '''Opens save 3D dialogue, and stores settings for the 3D model to be used on save'''
            dismiss_popup()

            
            ##Store variables to be used later
            self.tdwidth = checkValue(width, 10.0, True, False)
            self.tdheight = checkValue(height, 20.0, True, False)
            self.tdradius = checkValue(radius, 3.0, True, True)
            self.tdtri = checkValue(tri, 10, False, False)
            self.tdoverlap = checkValue(overlap, 11.0, True, False)
            self.tdcyl = checkValue(cyl, 10, False, False)

            ##open the save dialogue
            content = SaveDialog(save=save3D, cancel=dismiss_popup)
            
            self._popup = Popup(title="Save file", content=content,
                                size_hint=(0.9, 0.9))
            
            self._popup.open()
        def save3D(path, filename):
            '''Saves the 3D output to path/filename'''
            ##Generate the points
            points = self.app.getKnotPointsbyBand(self.grid,self.tdcyl, self.gridUnits, self.offsetX, self.offsetY, self.cornerType, self.tdoverlap)
            ##Generate the 3D model
            genCyl3(points, self.tdwidth, self.tdheight, self.tdradius, self.tdcyl, path+"/"+filename)
            dismiss_popup()
            
        def savePressed():
            '''Opens the save dialogue'''
            ##Unbind keyboard, so shortcuts no longer running
            self._keyboard.unbind(on_key_down=_on_keyboard_down)
            self._keyboard = None

            content = SaveDialog(save=save, cancel=dismiss_popup)
            self._popup = Popup(title="Save file", content=content,
                                size_hint=(0.9, 0.9))
            self._popup.open()
        def show_load():
            '''OPens the load dialogue'''
            ##Unbind keyboard, so shortcuts no longer running
            self._keyboard.unbind(on_key_down=_on_keyboard_down)
            self._keyboard = None

            content = LoadDialog(load=load, cancel=dismiss_popup)
            self._popup = Popup(title="Load file", content=content,
                                size_hint=(0.9, 0.9))
            self._popup.open()
        def dismiss_popup():
            '''Close popups'''
            ##initiate the keyboard fo rshortcuts
            self._keyboard = Window.request_keyboard(_keyboard_closed, self, 'text')
            if self._keyboard.widget:
                # If it exists, this widget is a VKeyboard object which you can use
                # to change the keyboard layout.
                pass
            self._keyboard.bind(on_key_down=_on_keyboard_down)
            
            self._popup.dismiss()
        def save(path, filename):
            '''Save the knot to path/filename'''
            f = open(path+"/"+filename, 'w')
            simplejson.dump(self.grid, f)
            f.close()

            dismiss_popup()
        def load(path, filename):
            '''load the knot from path/filename'''
            f = open(filename[0].replace("u", ""), 'r')
            self.grid = simplejson.load(f)
            f.close()

            ##Set sizing of knot
            self.knotX = len(self.grid[0])
            self.X.text = str(len(self.grid[0])//2)
            self.knotY = len(self.grid)
            self.Y.text = str(len(self.grid)//2)
            viewWidth = Window.width*0.52
            viewHeight = Window.height-110

            if ((viewWidth)/self.knotX < (viewHeight)/self.knotY):
                self.gridUnitsView = (viewWidth)/self.knotX
            else:
                self.gridUnitsView = (viewHeight)/self.knotY
            self.knotWidthView = (float(self.WidthI.text)/self.gridUnits)*self.gridUnitsView
            self.spacing = self.knotWidthView
            if self.knotWidthView < 1:
                self.knotWidthView = 1
            self.offsetX = Window.width*0.25 - self.gridUnitsView
            self.offsetY = Window.height*0.05 - self.gridUnitsView
            printKnot()

            dismiss_popup()
        def _keyboard_closed():
            '''Close the keyboard'''
            print('My keyboard have been closed!')
            try:
                self._keyboard.unbind(on_key_down=_on_keyboard_down)
                self._keyboard = None
            except:
                pass
            

        def _on_keyboard_down(keyboard, keycode, text, modifiers):
            '''Handles keyboard shortcuts'''
            print('The key', keycode, 'have been pressed')
            print(' - text is %r' % text)
            print(' - modifiers are %r' % modifiers)

            if keycode[1] == "d":
                toggleDotsPressed(self.toggleDots, 0)
            elif keycode[1] == "g":
                toggleGridPressed(self.toggleGrid, 0)
            elif keycode[1] == "b":
                toggleBreaklinesPressed(self.toggleBreaklines, 0)
            elif keycode[1] == "s" and len(modifiers) == 0:
                toggleSkeletonPressed(self.toggleSkeleton, 0)
            elif keycode[1] == "k":
                toggleKnotPressed(self.toggleKnot, 0)
            elif keycode[1] == "a":
                if self.addBreakline.text == "(A) Done":
                    addBreaklinePressed2(self.addBreakline)
                else:
                    addBreaklinePressed(self.addBreakline)
            elif keycode[1] == "o" and len(modifiers) == 0:
                output3DPressed(self.output3D)
            elif len(modifiers) == 1 and (keycode[1] == "z" and (modifiers[0]=="ctrl" or modifiers[0]=="meta")):
                self.app.backFuntion()
                if self.app.getOnBreaklines() == False:
                    printKnot()
                    
            elif len(modifiers)==2 and (keycode[1] == "z" and modifiers[0]=="shift" and (modifiers[1]=="ctrl" or modifiers[1]=="meta")):
                self.app.forwardFunction()
                if self.app.getOnBreaklines() == False:
                    printKnot()

            elif len(modifiers) == 1 and (keycode[1] == "s" and (modifiers[0]=="ctrl" or modifiers[0]=="meta")):
                 savePressed()
            elif len(modifiers) == 1 and (keycode[1] == "o" and (modifiers[0]=="ctrl" or modifiers[0]=="meta")):
                 show_load()

            
                            

            # Return True to accept the key. Otherwise, it will be used by
            # the system.
            return True

        ##Open the keyboard
        self._keyboard = Window.request_keyboard(_keyboard_closed, self, 'text')
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=_on_keyboard_down)

   

            
        
        
        ##Instance Variables
        self.showDots = True
        self.showGrid = True
        self.showBreaklines = True
        self.showSkeleton = True
        self.showKnot = True
        self.knotX = 4
        self.knotY = 4
        self.knotWidth = 8
        self.knotWidthView = 8
        self.gridUnits = 50
        self.gridUnitsView = 50
        self.spacing = 10
        self.offsetX = 150
        self.offsetY = 50
        self.totTabs = 1
        self.tabNo = 1
        self.cornerType = 0

        Window.bind(on_resize=on_resize)
        
        
        ##Main Layout
        layout_main = AnchorLayout(anchor_x = "left", anchor_y="top")


        ##Left hand bar - show/hide buttons and tools
        layout_left = AnchorLayout(anchor_x='left', anchor_y="top")
        layout_left_inner = BoxLayout(orientation= "vertical", size_hint=(0.2,1), padding =[0,0,0,0])
        ##Buttons on left layout
        #Save Load
        loadSaveButs = LoadSaveButtons(save = savePressed, load = show_load)
        layout_left_inner.add_widget(loadSaveButs)
        #Add Breakline
        self.addBreakline = Button(text='(A)dd Breaklines')
        self.addBreakline.bind(on_press=addBreaklinePressed)
        layout_left_inner.add_widget(self.addBreakline)
        #Show/Hide Dots
        layouttd = BoxLayout(orientation= "horizontal", size_hint=(1, 1), padding =[0,0,0,0])
        self.toggleDots = CheckBox(active = True)
        self.toggleDotsL = Label(text='Hide (D)ots')
        self.toggleDots.bind(active=toggleDotsPressed)
        layouttd.add_widget(self.toggleDots)
        layouttd.add_widget(self.toggleDotsL)
        layout_left_inner.add_widget(layouttd)
        #Show/Hide Grid
        layouttg = BoxLayout(orientation= "horizontal", size_hint=(1, 1), padding =[0,0,0,0])
        self.toggleGrid = CheckBox(active = True)
        self.toggleGridL = Label(text='Hide (G)rid')
        self.toggleGrid.bind(active=toggleGridPressed)
        layouttg.add_widget(self.toggleGrid)
        layouttg.add_widget(self.toggleGridL)
        layout_left_inner.add_widget(layouttg)
        #Show/Hide Breaklines
        layouttb = BoxLayout(orientation= "horizontal", size_hint=(1, 1), padding =[0,0,0,0])
        self.toggleBreaklines = CheckBox(active = True)
        self.toggleBreaklinesL = Label(text='Hide (B)reaklines')
        self.toggleBreaklines.bind(active=toggleBreaklinesPressed)
        layouttb.add_widget(self.toggleBreaklines)
        layouttb.add_widget(self.toggleBreaklinesL)
        layout_left_inner.add_widget(layouttb)
        #Show/Hide Skeleton
        layoutts = BoxLayout(orientation= "horizontal", size_hint=(1, 1), padding =[0,0,0,0])
        self.toggleSkeleton = CheckBox(active = True)
        self.toggleSkeletonL = Label(text='Hide (S)keleton')
        self.toggleSkeleton.bind(active=toggleSkeletonPressed)
        layoutts.add_widget(self.toggleSkeleton)
        layoutts.add_widget(self.toggleSkeletonL)
        layout_left_inner.add_widget(layoutts)
        #Show/Hide Final Knot
        layouttk = BoxLayout(orientation= "horizontal", size_hint=(1, 1), padding =[0,0,0,0])
        self.toggleKnot = CheckBox(active = True)
        self.toggleKnotL = Label(text='Hide (K)not')
        self.toggleKnot.bind(active=toggleKnotPressed)
        layouttk.add_widget(self.toggleKnot)
        layouttk.add_widget(self.toggleKnotL)
        layout_left_inner.add_widget(layouttk)
        ##Add Left Layout to scene
        layout_left.add_widget(layout_left_inner)
        layout_main.add_widget(layout_left)

        
        ##Right hand bar - knot settings
        layout_right = AnchorLayout(anchor_x='right', anchor_y="top")
        layout_right_inner = BoxLayout(orientation= "vertical", size_hint=(0.2,1), padding =[0,0,0,0])

        ##buttons for right layout
        #Grid Size
        #X
        self.labelX = Label(text='X =')
        self.X = TextInput(text = "4",multiline=False)
        self.X.bind(on_text_validate=plotButtonPressed)
        layout_x = BoxLayout(orientation= "horizontal", size_hint=(1, 1), padding =[0,0,0,0])
        layout_x.add_widget(self.labelX)
        layout_x.add_widget(self.X)
        layout_right_inner.add_widget(layout_x)
        #Y
        self.labelY = Label(text='Y =')
        self.Y = TextInput(text = "4", multiline=False)
        self.Y.bind(on_text_validate=plotButtonPressed)
        layout_y = BoxLayout(orientation= "horizontal", size_hint=(1, 1), padding =[0,0,0,0])
        layout_y.add_widget(self.labelY)
        layout_y.add_widget(self.Y)
        layout_right_inner.add_widget(layout_y)
        #Grid Units
        self.labelGU = Label(text='GridUnits =')
        self.gridUnitsI = TextInput(text = "50", multiline=False)
        self.gridUnitsI.bind(on_text_validate=plotButtonPressed)
        layout_gu = BoxLayout(orientation= "horizontal", size_hint=(1, 1), padding =[0,0,0,0])
        layout_gu.add_widget(self.labelGU)
        layout_gu.add_widget(self.gridUnitsI)
        layout_right_inner.add_widget(layout_gu)
        #Width
        self.labelWidth = Label(text='Width =')
        self.WidthI = TextInput(text = "8", multiline=False)
        self.WidthI.bind(on_text_validate=plotButtonPressed)
        layout_w = BoxLayout(orientation= "horizontal", size_hint=(1, 1), padding =[0,0,0,0])
        layout_w.add_widget(self.labelWidth)
        layout_w.add_widget(self.WidthI)
        layout_right_inner.add_widget(layout_w)
        #corner Option
        self.cornerLabel = Label(text="Corner")
        layout_c = BoxLayout(orientation= "horizontal", size_hint=(1, 1), padding =[0,0,0,0])
        cornerbuts = CornerButtons(b1 = cornerButton1Pressed, b2 = cornerButton2Pressed)
        layout_right_inner.add_widget(self.cornerLabel)
        layout_right_inner.add_widget(cornerbuts)
        #Curve Slider
        self.curveLabel = Label(text="Curvature")
        self.curve = Slider(min=-1, max=1, value=0)


        #Output 3D
        self.output3D = Button(text='(O)utput 3D')
        self.output3D.bind(on_press=output3DPressed)
        layout_right_inner.add_widget(self.output3D)
        ##Add right layout to scene
        layout_right.add_widget(layout_right_inner)
        layout_main.add_widget(layout_right)
        

        ##Print Initial knot
        self.app = MyKnotworkWidget()
        self.grid = grid().createGrid(4,4)
        self.grid = grid().detEdgecode(self.grid)
        self.grid = grid().setBandNumber(self.grid)
        
        
        self.gridUnits = checkValue(self.gridUnitsI.text, 50, False, False)
        self.gridUnitsI.text = str(self.gridUnits)
        self.X.text = str(checkValue(self.X.text, 4, False, False))
        self.Y.text = str(checkValue(self.Y.text, 4, False, False))
        self.WidthI.text = str(checkValue(self.WidthI.text, 8.0, True, False))



        self.grid = grid().createGrid(int(self.X.text),int(self.Y.text))
        
        self.grid = grid().detEdgecode(self.grid)
        self.grid = grid().setBandNumber(self.grid)
        
        self.knotX = int(self.X.text)*2
        self.knotY = int(self.Y.text)*2
        viewWidth = Window.width*0.52
        viewHeight = Window.height-110

        if ((viewWidth)/self.knotX < (viewHeight)/self.knotY):
            self.gridUnitsView = (viewWidth)/self.knotX
        else:
            self.gridUnitsView = (viewHeight)/self.knotY
        self.knotWidthView = (float(self.WidthI.text)/self.gridUnits)*self.gridUnitsView
        self.spacing = self.knotWidthView
        if self.knotWidthView < 1:
            self.knotWidthView = 1
        self.offsetX = Window.width*0.25 - self.gridUnitsView
        self.offsetY = Window.height*0.05 - self.gridUnitsView
        printKnot()        
        layout_main.add_widget(self.app)

        
        return layout_main


Factory.register('SaveDialog', cls=SaveDialog)
Factory.register('LoadDialog', cls=LoadDialog)

        
if (__name__ == "__main__"):
    CelticKnotwork().run()#.drawEllipse()
