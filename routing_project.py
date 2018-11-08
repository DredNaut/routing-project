# Putting a gif image on a canvas with Tkinter
# tested with Python24 by  vegaseat  25jun2005
from Tkinter import *
import random

pixel_size = 32
canvas_height = 20 
canvas_width = 20


# create the canvas, size in pixels
canvas = Canvas(width = pixel_size*canvas_width, height = pixel_size*canvas_height, bg = 'yellow')
# pack the canvas into a frame/form
canvas.pack(expand = YES, fill = BOTH)
# load the .gif image file
# put in your own gif file here, may need to add full path
# like 'C:/WINDOWS/Help/Tours/WindowsMediaPlayer/Img/mplogo.gif'

# Route will be an over lay that is drawn over the map to indicate the route chosen
#class Route:
#    def __init__ (self, index):

class Zone:
    def __init__ (self, field, image, resistance, x, y, index):
        # Field will carry the color of the block
        self.field = field
        # Holds that actual bitmap image
        self.image = image
        # Resistance will hold the value of the value of transmissability
        self.resistance = resistance
        self.x = x
        self.y = y
        self.index = index
        self.node = None
        self.route = None
        self.crumb = False
    def installNode (self):
        self.node = Node(self.x, self.y, tower, self.index)
        canvas.create_image(self.x, self.y, image = self.node.image, anchor = NW)
    def installRoute (self):
        self.route = Route(self.x, self.y, route_ub)
        canvas.create_image(self.x, self.y, image = self.node.image, anchor = NW)

    def isNode (self):
        if (self.node != None):
            return True
        else:
            return False
    def getRight (self):
        return self.index+1
    def getLeft (self):
        return self.index-1
    def getUp (self):
        return self.index+canvas_width
    def getBelow (self):
        return self.index-canvas_width
    def resetCrumb (self):
        self.crumb = False
    def setCrumb (self):
        self.crumb = True
        print "Crumb set on " + str(self.index)

class Node:
    def __init__ (self, x, y, image, index):
        # Field will carry the color of the block
        #X and Y coordinates
        self.x = x 
        self.y = y
        self.index = index
        # Holds that actual bitmap image
        self.image = image
        
class Route:
    def __init__ (self, x, y, image):
        # Field will carry the color of the block
        #X and Y coordinates
        self.x = x 
        self.y = y
        # Holds that actual bitmap image
        self.image = image

red1 = PhotoImage(file = './assets/red1.gif')
red2 = PhotoImage(file = './assets/red2.gif')
red3 = PhotoImage(file = './assets/red3.gif')
red4 = PhotoImage(file = './assets/red4.gif')
red5 = PhotoImage(file = './assets/red5.gif')

tower = PhotoImage(file = './assets/tower.gif')

route_ub = PhotoImage(file = './assets/vertical.gif')
route_lr = PhotoImage(file = './assets/horizontal.gif')
route_ul = PhotoImage(file = './assets/up_left_elbow.gif')
route_ur = PhotoImage(file = './assets/up_right_elbow.gif')
route_bl = PhotoImage(file = './assets/below_left_elbow.gif')
route_br = PhotoImage(file = './assets/below_right_elbow.gif')

# put gif image on canvas
# pic's upper left corner (NW) on the canvas is at x=50 y=10

# Map containing an array of Zones
tkMap=[]

for y in range(canvas_width):
    for x in range(canvas_height):
        z = random.randint(1,5)
        if (z == 1):
            tkMap.append(Zone(1, red1, 0.2, x*pixel_size, y*pixel_size, x+y*canvas_width))
            canvas.create_image(x*pixel_size, y*pixel_size, image = red1, anchor = NW)
        elif (z == 2):
            tkMap.append(Zone(2, red2, 0.4, x*pixel_size, y*pixel_size, x+y*canvas_width))
            canvas.create_image(x*pixel_size, y*pixel_size, image = red2, anchor = NW)
        elif (z == 3):
            tkMap.append(Zone(3, red3, 0.6, x*pixel_size, y*pixel_size, x+y*canvas_width))
            canvas.create_image(x*pixel_size, y*pixel_size, image = red3, anchor = NW)
        elif (z == 4):
            tkMap.append(Zone(4, red4, 0.8, x*pixel_size, y*pixel_size, x+y*canvas_width))
            canvas.create_image(x*pixel_size, y*pixel_size, image = red4, anchor = NW)
        elif (z == 5):
            tkMap.append(Zone(5, red5, 1.0, x*pixel_size, y*pixel_size, x+y*canvas_width))
            canvas.create_image(x*pixel_size, y*pixel_size, image = red5, anchor = NW)

#def plotPath(pathArray):
#    for z in range(len(pathArray)-2):
#        if (pathArray[z]+canvas_width+1 == pathArray[z+2] and pathArray[z+1] == pathArray[z]+1):
#            canvas.create_image(tkMap[pathArray[z+1]].x, tkMap[pathArray[z+1]].y, image = route_bl, anchor = NW)
#            canvas.create_image(tkMap[pathArray[z]].x, tkMap[pathArray[z]].y, image = route_lr, anchor = NW)
#        elif (pathArray[z]+canvas_width-1 == pathArray[z+2] and pathArray[z+1] == pathArray[z]-1):
#            canvas.create_image(tkMap[pathArray[z+1]].x, tkMap[pathArray[z+1]].y, image = route_br, anchor = NW)
#            canvas.create_image(tkMap[pathArray[z]].x, tkMap[pathArray[z]].y, image = route_lr, anchor = NW)
#        elif (pathArray[z]+canvas_width+1 == pathArray[z+2] and pathArray[z+1] == pathArray[z]+canvas_width):
#            canvas.create_image(tkMap[pathArray[z+1]].x, tkMap[pathArray[z+1]].y, image = route_ur, anchor = NW)
#            canvas.create_image(tkMap[pathArray[z]].x, tkMap[pathArray[z]].y, image = route_ub, anchor = NW)
#        elif (pathArray[z]+canvas_width-1 == pathArray[z+2] and pathArray[z+1] == pathArray[z]+canvas_width):
#            canvas.create_image(tkMap[pathArray[z+1]].x, tkMap[pathArray[z+1]].y, image = route_ul, anchor = NW)
#            canvas.create_image(tkMap[pathArray[z]].x, tkMap[pathArray[z]].y, image = route_ub, anchor = NW)
#        elif (pathArray[z+1] == pathArray[z]+1 and pathArray[z+2] == pathArray[z]+2):
#            canvas.create_image(tkMap[pathArray[z]].x, tkMap[pathArray[z]].y, image = route_lr, anchor = NW)
#        elif (pathArray[z]-1 == pathArray[z+1] and pathArray[z]-2 == pathArray[z+2]):
#            canvas.create_image(tkMap[pathArray[z]].x, tkMap[pathArray[z]].y, image = route_lr, anchor = NW)
#        elif (pathArray[z]-canvas_width == pathArray[z+1] and pathArray[z]-(2*canvas_width) == pathArray[z+2]):
#            canvas.create_image(tkMap[pathArray[z]].x, tkMap[pathArray[z]].y, image = route_ub, anchor = NW)
#        elif (pathArray[z]+canvas_width == pathArray[z+1] and pathArray[z]+(2*canvas_width) == pathArray[z+2]):
#            canvas.create_image(tkMap[pathArray[z]].x, tkMap[pathArray[z]].y, image = route_ub, anchor = NW)



def isInYBound (index):
    if ((index - canvas_width < 0) or (index + canvas_width > canvas_width*canvas_height)):
        return False
    else:
        return True

def isInRightBound (index):
    if (index + 1 % canvas_width == 0 or index > canvas_width*canvas_height):
        return False
    else:
        return True

def isInLeftBound (index):
    if (index % canvas_width == 0 or index == 0 or index < -1):
        return False
    else:
        return True

def checkSurrounding (index):
    if (tkMap[tkMap[index].getUp()].isNode()) and (tkMap[tkMap[index].getUp()].crumb == False):
        print ("Found Node Below of index: ", index )
        return True
    elif (tkMap[tkMap[index].getRight()].isNode()) and (tkMap[tkMap[index].getRight()].crumb == False):
        print ("Found Node Right of index: ", index)
        return True
    elif (tkMap[tkMap[index].getBelow()].isNode()) and (tkMap[tkMap[index].getBelow()].crumb == False) and isInYBound(index):
        print ("Found Node Above of index: ", index)
        return True
    elif (tkMap[tkMap[index].getLeft()].isNode()) and (tkMap[tkMap[index].getLeft()].crumb == False) and isInLeftBound(index):
        print ("Found Node Left of index: ", index)
        print tkMap[tkMap[index].getLeft()].crumb
        print tkMap[tkMap[index].getLeft()].index
        return True
    else:
        return False

def chooseNextRoute (index):
    path=[]
    path.append(index)
    tmp = -1
    tkMap[index].setCrumb()
    while not checkSurrounding (index):
#    for x in range(1,50): 
        cost = 10
        print index
        if (isInYBound(tkMap[index].getUp()) and not tkMap[tkMap[index].getUp()].crumb):
            if (tkMap[tkMap[index].getUp()].resistance < cost):
                cost = tkMap[tkMap[index].getUp()].resistance
                tmp = tkMap[index].getUp()
        if (isInRightBound(tkMap[index].getRight()) and not tkMap[tkMap[index].getRight()].crumb):
            if (tkMap[tkMap[index].getRight()].resistance < cost):
                cost = tkMap[tkMap[index].getRight()].resistance
                tmp = tkMap[index].getRight()
        if (isInYBound(tkMap[index].getBelow()) and  not tkMap[tkMap[index].getBelow()].crumb):
            if (tkMap[tkMap[index].getBelow()].resistance < cost):
                cost = tkMap[tkMap[index].getBelow()].resistance
                tmp = tkMap[index].getBelow()
        if (isInLeftBound(index) and not tkMap[tkMap[index].getLeft()].crumb):
            if (tkMap[tkMap[index].getLeft()].resistance < cost):
                cost = tkMap[tkMap[index].getLeft()].resistance
                tmp = tkMap[index].getLeft()
        print ("Index of next Zone: ", tmp)
        if (tmp == index):
            print "Stuck, Backtracking"
            tkMap[tmp].setCrumb()
            index = path[len(path)-3]
            print path[len(path)-3]
        else:
            tkMap[tmp].setCrumb()
            index = tmp
            path.append(tmp)
    for x in range(len(path)):
        print path[x]
#    plotPath(path)

#for x in range(0,len(tkMap)):
#    if (x % canvas_width == 0 and x>2):
#        print
#    print (tkMap[x].field),

tkMap[0].installNode()
tkMap[canvas_width-1].installNode()
tkMap[(canvas_width-1)*(canvas_height)].installNode()
tkMap[(canvas_width)*(canvas_height)-1].installNode()

chooseNextRoute(0)

# run it ...
mainloop()
