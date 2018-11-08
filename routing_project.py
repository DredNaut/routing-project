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

red1 = PhotoImage(file = './assets/red1.gif')
red2 = PhotoImage(file = './assets/red2.gif')
red3 = PhotoImage(file = './assets/red3.gif')
red4 = PhotoImage(file = './assets/red4.gif')
red5 = PhotoImage(file = './assets/red5.gif')
# put gif image on canvas
# pic's upper left corner (NW) on the canvas is at x=50 y=10
for x in range(canvas_width):
    for y in range(canvas_height):
        z = random.randint(1,5)
        if (z == 1):
            canvas.create_image(x*pixel_size, y*pixel_size, image = red1, anchor = NW)
        elif (z == 2):
            canvas.create_image(x*pixel_size, y*pixel_size, image = red2, anchor = NW)
        elif (z == 3):
            canvas.create_image(x*pixel_size, y*pixel_size, image = red3, anchor = NW)
        elif (z == 4):
            canvas.create_image(x*pixel_size, y*pixel_size, image = red4, anchor = NW)
        elif (z == 5):
            canvas.create_image(x*pixel_size, y*pixel_size, image = red5, anchor = NW)

canvas.create_oval(pixel_size*0+8, pixel_size*0+8, pixel_size-8+pixel_size*0, pixel_size-8+pixel_size*0, fill = "orange")
canvas.create_oval(pixel_size*0+8, pixel_size*(canvas_width-1)+8, pixel_size-8+pixel_size*0, pixel_size-8+pixel_size*(canvas_width-1), fill = "orange")
canvas.create_oval(pixel_size*(canvas_width-1)+8, pixel_size*(canvas_width-1)+8, pixel_size-8+pixel_size*(canvas_width-1), pixel_size-8+pixel_size*(canvas_width-1), fill = "orange")
canvas.create_oval(pixel_size*(canvas_width-1)+8, pixel_size*0+8, pixel_size-8+pixel_size*(canvas_width-1), pixel_size-8+pixel_size*0, fill = "orange")

# run it ...
mainloop()

class Plot:
    def __init__ (self, field, resistance):
        # Field will carry the color of the block
        self.field = field
        # Resistance will hold the value of the value of transmissability
        self.resistance = resistance



