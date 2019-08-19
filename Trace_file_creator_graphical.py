from tkinter import *
from tkinter import filedialog
import pygame
from pygame.locals import *
from random import randint
import os



def new_num_boxes():
    for i in range(len(height)):
        height["height{0}".format(i)].grid_forget()
    for i in range(0, int(num_boxes.get())):
        height["height{0}".format(i)].grid(row=i+2, column=3, columnspan=2, padx=10)
    make_rectangles()


def trace_change(a=1,b=1,c=1,):
    if num_box_default.get() and box_height.get() and delay_default.get() and time_default.get() and length_default.get():
        make_rectangles()
    
def change():
    make_rectangles()

def changes(val):
    make_rectangles()

def save():
    root.filename =  filedialog.asksaveasfilename(initialdir = "/",title = "Save File", defaultextension=".txt", filetypes=[("text files", "*.txt")])
    #print(root.filename)
    file = open(root.filename, "w")
    file.write(num_boxes.get())
    file.write(" ")
    file.write(delay.get())
    file.write(" ")
    file.write(height_boxes.get())
    file.write(" ")
    file.write(time.get())
    file.write(" ")
    file.write(box_lengths.get())
    file.write(" ")
    file.write(str(boxes_at_once_.get()))
    file.write(" ")
    for i in range(0,int(num_boxes.get())):
        file.write(str(height["height{0}".format(i)].get()))
        file.write(" ")
    file.close()
    
def random_pos():
    for i in range(0, 20):
        height["height{0}".format(i)].set(randint(10,100))

def reset_pos():
    for i in range(0, 20):
        height["height{0}".format(i)].set(50)

def quit_():
    pygame.quit()
    exit()

def load_():
    file_path = filedialog.askopenfilename()
    file = open(file_path, "r")
    with file as f:
        lines=f.read().split()
    file.close()
        
    num_box_default.set(lines[0])
    delay_default.set(lines[1])
    box_height.set(lines[2])
    time_default.set(lines[3])
    length_default.set(lines[4])
    boxes_at_once_.set(lines[5])

    for i in range(0,int(num_boxes.get())):
        height["height{0}".format(i)].set(lines[i+6])


    
    
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
resolution = (1780,1005)
DISPLAY=pygame.display.set_mode(resolution)        #,pygame.FULLSCREEN
WHITE=(255,255,255)
BLUE=(0,0,255)
RED=(255,0,0)
DISPLAY.fill(WHITE)
pygame.display.update()


def make_rectangles():
    DISPLAY.fill(WHITE)
    global box_length
    global next_box
    box_length = int(box_lengths.get())
    next_box = resolution[0]/(int(num_boxes.get()) + int(delay.get()))
    for i in range(0,int(num_boxes.get())):
        pygame.draw.rect(DISPLAY,RED,(float(delay.get())*next_box + i*next_box,
                                      resolution[1]-(float(height["height{0}".format(i)].get())*resolution[1])/100,
                                      box_length*(resolution[0]/1920),
                                      (float(height_boxes.get())*resolution[1])/100))
    pygame.display.update()



            
        

root = Tk()
root.title("Graphical Trace File Creator")

title = Label(root, text="Trace File Maker")
title.config(height = 3, width = 20, font = 20)
title.grid(row=0, column=0, padx=10, pady=0, columnspan=4)


num_boxes_l = Label(root,text="Number of boxes")
num_boxes_l.config(font=20)
num_boxes_l.grid(row=1, column=0)

num_box_default = StringVar(root)
num_box_default.set("6")
num_boxes = Spinbox(root, from_=1, to=20, font=0, command=new_num_boxes, textvariable=num_box_default)
num_boxes.grid(row=1, column=1, padx=10, pady=10)


height_boxes_l = Label(root, text="Height of boxes")
height_boxes_l.config(font=20)
height_boxes_l.grid(row=2, column=0)

box_height = StringVar(root)
box_height.set("10")
height_boxes = Spinbox(root, from_=0, to=100, font=0, command=change, textvariable=box_height)
height_boxes.grid(row=2, column=1, padx=10, pady=10)



delay_l = Label(root, text="Delay before start")
delay_l.config(font=20)
delay_l.grid(row=3, column=0)

delay_default = StringVar(root)
delay_default.set("1")
delay = Spinbox(root, from_=0, to=10, font=0, command=change, textvariable=delay_default)
delay.grid(row=3, column=1, padx=10, pady=10)


time_l = Label(root, text="Time to cross screen")
time_l.config(font=20)
time_l.grid(row=4, column=0)

time_default = StringVar(root)
time_default.set("10")
time = Spinbox(root, from_=1, to= 60, font=0, command=change, textvariable=time_default)
time.grid(row=4, column=1, padx=10, pady=10)


box_length_l = Label(root, text="Length of boxes")
box_length_l.config(font=20)
box_length_l.grid(row=5, column=0)

length_default = StringVar(root)
length_default.set("200")
box_lengths = Spinbox(root, from_=1, to=1000, command=change, textvariable=length_default)
box_lengths.config(font=20)
box_lengths.grid(row=5, column=1, padx=10, pady=10)


boxes_at_once_l = Label(root, text="Show only one box ahead")
boxes_at_once_l.config(font=20)
boxes_at_once_l.grid(row=6, column=0)

boxes_at_once_ = IntVar()
boxes_at_once_.set(0)
boxes_at_once = Checkbutton(root, variable=boxes_at_once_)
boxes_at_once.config(font=20)
boxes_at_once.grid(row=6, column=1, padx=10, pady=10)
boxes_at_once.var = boxes_at_once_


save = Button(root, text="save", command=save)
save.config(font=20)
save.grid(row=7, column=1, padx=10, pady=10)

load_b = Button(root, text="load", command=load_)
load_b.config(font=20)
load_b.grid(row=8, column=1, padx=10, pady=10)

quit_b = Button(root, text="quit", command=quit_)
quit_b.config(font=20)
quit_b.grid(row=9, column=1, padx=10, pady=5)

spacer = Label(root)
spacer.grid(row=1, column=2, padx=50)


reset = Button(root, text="reset", command=reset_pos)
reset.config(font=20)
reset.grid(row=1, column=4)

random = Button(root, text="random", command=random_pos)
random.config(font=20)
random.grid(row=1, column=3)


num_box_default.trace("w", trace_change)
box_height.trace("w", trace_change)
delay_default.trace("w", trace_change)
time_default.trace("w", trace_change)
length_default.trace("w", trace_change)
                 

global height
height={}
for i in range(0, 20):
    height["height{0}".format(i)] = Scale(root, from_=0, to=100,font=0, orient=HORIZONTAL, length=300, command=changes)
    height["height{0}".format(i)].grid(row=i+2, column=3, columnspan=2, padx=10)
    height["height{0}".format(i)].set(50)
for i in range(len(height)):
        height["height{0}".format(i)].grid_forget()
for i in range(0, int(num_boxes.get())):
        height["height{0}".format(i)].grid(row=i+2, column=3, columnspan=2, padx=10)







root.mainloop()
