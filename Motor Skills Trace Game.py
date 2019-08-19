import nidaqmx
import time
from datetime import datetime
from random import uniform
import statistics
import pygame
import pygame.gfxdraw
from pygame.locals import *
import math
import statistics
from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox
import os
from functools import partial
from random import randint
import random





interval = 0.005                    #amount of time between samples in seconds
scores = []                         #list that will contain all the scores for each trial        
hits = []                           #list containing a 1 or 0 depending on if the target was hit or not. Used for adding up the score at the end of each trial
pygame.init()
resolution = (1920,1080)            #resolution can be adjusted to be any resolution. The game will size correctly for any size screen
num_points = 16                     #number of points to be drawn after the current point. Effectivly the length of the "tail"




'''
Start

Start initializes the pygame window and defines some parameters for the pygame window

Takes one parameter, either a 1 or 0 depending on if the game should be full screen or not.
'''

def Start(full_screen):
    global WHITE
    global RED
    global BLUE
    WHITE=(255,255,255)
    BLUE=(0,0,255)
    RED=(255,0,0)
        
    pygame.init()
    pygame.font.init()
    global DISPLAY
    if full_screen == 1:
        DISPLAY=pygame.display.set_mode(resolution, pygame.FULLSCREEN)        #,pygame.FULLSCREEN
        pygame.mouse.set_visible(0)
    else:
        DISPLAY=pygame.display.set_mode(resolution)
    DISPLAY.fill(WHITE)
    pygame.display.update()
    return


'''
Trace

Trace begins the trial, it first displays the countdown, then it starts the NI DAQ and begins collecting data
Trace continues until the trace file is finished, typically around 10 seconds

Trace takes one parameter, the path to the trace file. This path is then passed to get_trace where
the paramets of the trace file are extracted from the file
'''

def Trace(path):
    get_trace(path)

    disp_text("3")
    time.sleep(1)
    DISPLAY.fill(WHITE)
    pygame.display.update()
    disp_text("2")
    time.sleep(1)
    DISPLAY.fill(WHITE)
    pygame.display.update()
    disp_text("1")
    time.sleep(1)
    DISPLAY.fill(WHITE)
    pygame.display.update()



    #start recording on Lab Chart
    with nidaqmx.Task() as task:
        task.ao_channels.add_ao_voltage_chan("Dev1/ao0")
        task.write(10, auto_start=True)

            
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai"+str(device_input_e.get()))


        
        global xs
        global ys
        ys = []
        xs = []
        start_time = time.time()
        last_time = time.time()
        
        
        
        global newx1
        global newy1
        newx1 = 0
        newy1 = 0

        
        
        while True:
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    return
        
            if(last_time + interval < time.time()):
                last_time = time.time()
                data = task.read()
                ys.append(data)
                xs.append(time.time()-start_time)
                #print(data)
                #print(time.time()-start_time)
                DISPLAY.fill(WHITE)
                make_rectangles()
                for i in range(len(xs)-1):
                    if(i >= len(xs) - num_points):
                        #scale values to the size of screen
                        newy = resolution[1] - (ys[i] * resolution[1])/(float(mvc_val.get())*(int(percent_mvc_e.get())/100))
                        newx = (xs[i] * resolution[0])/time_per_test
                        newy1 = resolution[1] - (ys[i+1] * resolution[1])/(float(mvc_val.get())*(int(percent_mvc_e.get())/100))
                        newx1 = (xs[i+1] * resolution[0])/time_per_test

                        
                        pygame.draw.line(DISPLAY,BLUE,(newx, newy), (newx1, newy1), 2)
                hit()  

            if(start_time + time_per_test < time.time()):
                DISPLAY.fill(WHITE)
                pygame.display.update()
                #stop recording on Lab Chart
                with nidaqmx.Task() as task:
                    task.ao_channels.add_ao_voltage_chan("Dev1/ao0")
                    task.write(0, auto_start=True)
                return
            

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_q]:
                DISPLAY.fill(WHITE)
                pygame.display.update()
                pygame.quit()
                sys.exit()
                return
            
            pygame.display.update()

'''
test_device

test_device opens a full screen pygame window and displays a cursor that moves across the screen for 10 seconds.
This allows the device to be tested to ensure the participant can properly use the input device.
'''
def test_device():
    Start(1)
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai"+str(device_input_e.get()))

        global newx1
        global newy1
        ys = []
        xs = []
        newx1 = 0
        newy1 = 0
        start_time = time.time()
        last_time = time.time()
        time_per_test = 10
        
        while True:
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    return
        
            if(last_time + interval < time.time()):
                last_time = time.time()
                data = task.read()
                ys.append(data)
                xs.append(time.time()-start_time)
                #print(data)
                #print(time.time()-start_time)
                DISPLAY.fill(WHITE)
                for i in range(len(xs)-1):
                    if(i >= len(xs) - num_points):
                        #scale values to the size of screen

                        newy = resolution[1] - (ys[i] * resolution[1])/(float(mvc_val.get())*(int(percent_mvc_e.get())/100))
                        newx = (xs[i] * resolution[0])/time_per_test
                        newy1 = resolution[1] - (ys[i+1] * resolution[1])/(float(mvc_val.get())*(int(percent_mvc_e.get())/100))
                        newx1 = (xs[i+1] * resolution[0])/time_per_test

                        
                        pygame.draw.line(DISPLAY,BLUE,(newx, newy), (newx1, newy1), 2) 

            if(start_time + time_per_test < time.time()):
                DISPLAY.fill(WHITE)
                pygame.display.update()
                pygame.quit()
                return
            
            pygame.display.update()

'''
zero_device

zero_device opens a new pygame window and displays raw values from the NI DAQ device.
These raw values allow the user to manually zero the device using the hardware on the DAQ device
'''
def zero_device():
    Start(0)
    last_time = time.time() 
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai"+str(device_input_e.get()))

        while True:
            for event in pygame.event.get():
                    if event.type==QUIT:
                        pygame.quit()
                        return
            if(last_time + 0.1 < time.time()):
                last_time = time.time()       
                disp_text_values(str(math.ceil(task.read()*10000)/10000))
            
        return


'''
get_MVC

get_MVC will get the participants maximum voluntary contraction
get_MVC will open a full screen pygame window, followed by a 3 second countdown
raw input values will be displayed for 5 seconds, after which the participants MVC will be displayed

MVC is calculated by finding the maximum input value, then getting a 500ms average around that value.
'''
def get_MVC():
    Start(1)

    disp_text("3")
    time.sleep(1)
    DISPLAY.fill(WHITE)
    pygame.display.update()
    disp_text("2")
    time.sleep(1)
    DISPLAY.fill(WHITE)
    pygame.display.update()
    disp_text("1")
    time.sleep(1)
    DISPLAY.fill(WHITE)
    pygame.display.update()
    
    start_time = time.time()
    last_time = time.time()
    max_val = 0
    max_pos = 0
    mvc = 0
    data = []
    time_data = []


    #start recording on Lab Chart
    with nidaqmx.Task() as task:
        task.ao_channels.add_ao_voltage_chan("Dev1/ao0")
        task.write(10, auto_start=True)
            
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai"+str(device_input_e.get()))

        while True:
            for event in pygame.event.get():
                    if event.type==QUIT:
                        pygame.quit()
                        return
            #take 50 samples per second
            if(last_time + 0.0199 < time.time()):
                last_time = time.time()
                data.append(task.read())
                time_data.append(time.time()-start_time)
                disp_text_values(str(math.ceil(data[-1]*10000)/10000))
                if data[-1] > max_val:
                    max_val = data[-1]
                    max_pos = len(data)

            #after 5 seconds stop sampling
            if(start_time + 5 < time.time()):
                DISPLAY.fill(WHITE)
                pygame.display.update()
                time.sleep(0.5)

                #get a 500ms average around the highest point
                for i in range(max_pos+25, len(data)):
                    data.pop(max_pos+25)

                for i in range(0, max_pos-25):
                    data.pop(0)

                #stop recording on Lab Chart
                with nidaqmx.Task() as task:
                    task.ao_channels.add_ao_voltage_chan("Dev1/ao0")
                    task.write(0, auto_start=True)
            
                mvc = statistics.mean(data)
                disp_text("MVC: " + str(math.ceil(mvc*10000)/10000))
                pygame.display.update()
                time.sleep(4)
                pygame.quit()
                mvc_val.set(str(math.ceil(mvc*1000000)/1000000))
                return

'''
get_trace

get_trace extracts parameters from the trace file
the parameters in trace files are separated by a single space
trace files are in .txt format

trace file parameters are in the following order:
number of boxes
delay before start
height of boxes
length of time per test
length of boxes
if all boxes are shown at the start or one at a time
all box positions are then listed in order

'''
def get_trace(path):
    file = open(path, "r")
    trace = file.read()
    trace = trace.split()
    file.close()

    global num_boxes
    global delay
    global box_height
    global box_positions
    global time_per_test
    global box_length
    global boxes_shown
    global trace_file_location_view
    
    trace_file_location_view=path
    num_boxes = int(trace[0])
    delay = int(trace[1])
    box_height = int(trace[2])
    time_per_test = int(trace[3])
    box_length = int(trace[4])
    boxes_shown = int(trace[5])
    box_positions = []
    for i in range(6, len(trace)):
        box_positions.append(int(trace[i]))

'''
make_rectangles

make_rectangles when called will draw the red rectangles on screen
this function will scale depending on the resolution of the screen.
'''
def make_rectangles():
    global next_box
    next_box = resolution[0]/(num_boxes + delay)
    for i in range(len(box_positions)):
        if boxes_shown == 0 or newx1 >= delay*next_box + (i-1)*next_box:
            pygame.draw.rect(DISPLAY,RED,(delay*next_box + i*next_box,
                                          resolution[1]-(box_positions[i]*resolution[1])/100,
                                          box_length,
                                          (box_height*resolution[1])/100))
        
'''
hit

hit is called each time a new data point is collected
hit will append a 1 to hits if the target is hit, and will append a 0 if the target was not hit
'''
def hit():
    hit_=[]
    for i in range(len(box_positions)):
        if(newx1 >= delay*next_box + i*next_box and newx1 < delay*next_box + i*next_box + box_length):
            if(newy1 >= resolution[1]-(box_positions[i]*resolution[1])/100 and newy1 <= resolution[1]-(box_positions[i]*resolution[1])/100 + (box_height*resolution[1])/100 ):
                hit_.append(1)
            else:
                hit_.append(0)
                
    if (len(hit_) > 0):
        if (hit_.count(1) > 0):
            hits.append(1)
        else:
            hits.append(0)

            
'''
kp

kp will display the participants knowledge of performance after each trial, if the option is selected.
'''
def kp():
    
    WHITE=(255,255,255)
    BLUE=(0,0,255)
    DISPLAY.fill(WHITE)
    time.sleep(0.5)

    make_rectangles()
        
    for i in range(len(xs)-1):
                        #scale values to the size of screen
                        newy = resolution[1] - (ys[i] * resolution[1])/(float(mvc_val.get())*(int(percent_mvc_e.get())/100))
                        newx = (xs[i] * resolution[0])/time_per_test
                        newy1 = resolution[1] - (ys[i+1] * resolution[1])/(float(mvc_val.get())*(int(percent_mvc_e.get())/100))
                        newx1 = (xs[i+1] * resolution[0])/time_per_test
                        pygame.draw.line(DISPLAY,BLUE,(newx, newy), (newx1, newy1), 2)
    pygame.display.update()
    time.sleep(float(feedback_time.get()))
 
'''
kr_quant

kr_quant will display the users quantitative score, if the option is selected
the score is a time on target percentage
'''
def kr_quant():
    disp_text("Time on Target: " + str(score) + "%")

'''
kr_qual

kr_qual will display the users qualitative score, if the option is selected.
this score is based on the time on target percentage.
'''
def kr_qual():
    global qual
    if(score < 20):
        qual="Poor"
    elif(score < 40):
        qual="Acceptable"
    elif(score < 60):
        qual="Satisfactory"
    elif(score < 80):
        qual="Good"
    else:
        qual="Excellent"
    if kr_qual_.get():  
        disp_text("Score:" + qual)
        time.sleep(float(feedback_time.get()))
    return

'''
disp_text

disp_text is a generic function used to display any text sent to it.
the text displayed will be automatically centered both vertically and horizontally.
'''
def disp_text(text):
    DISPLAY.fill(WHITE)
    pygame.display.update()
    myfont = pygame.font.SysFont("monospace", 115)
    label=myfont.render(text, 1,(0,0,0))
    text_size=label.get_rect()
    text_x=text_size[2]
    text_y=text_size[3]
    DISPLAY.blit(label, (resolution[0]/2 - text_x/2,resolution[1]/2 - text_y/2))
    pygame.display.update()
    return

'''
disp_text_values

disp_text_values will display values sent to it.
'''
def disp_text_values(text):
    myfont = pygame.font.SysFont("monospace", 115)
    label=myfont.render("Value: ", 1,(0,0,0))
    text_size=label.get_rect()
    text_y=text_size[3]
    DISPLAY.fill(WHITE)
    DISPLAY.blit(label, (400, resolution[1]/2 - text_y/2))
    label=myfont.render(text, 1,(0,0,0))
    DISPLAY.blit(label, (900, resolution[1]/2 - text_y/2))
    pygame.display.update()
    return

'''
results

results is able to calculate the score, it is called after each trial to get the participants score.
To calulate the score it divides the number of 1s in hits and divides it by the total number of 1s and 0s in hits.
This value is the score and it is also added to the scores list.
'''
def results():
    global score
    score = (hits.count(1)/len(hits))*100
    score = round(score,2)
    scores.append(score)
    del hits[:]
    return

'''
save_raw_data

save_raw_data will save all the raw data to a text file after each trial
the name entered will be used to create a new folder, if it doesn't already exist,
each trial will have its own text file which will contain some basic test information
as well as all the raw data (input value and time) fro the trial

input paramets include the trial number, block number, and the trace file location
'''
def save_raw_data(trial,block,file_location):
    save_folder = test_save_folder[:-4]
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    file2 = open(save_folder+"/trial"+str(trial+1)+"_block"+str(block+1)+".txt", "w")
    file2.write(str(file_location)+"\n")
    file2.write(str(datetime.now()))
    file2.write("\n")
    if rand_seq_block_.get() == 1:
            file2.write("Sequential structure")
    elif rand_seq_block_.get() == 2:
            file2.write("Blocked structure")
    elif rand_seq_block_.get() == 3:
            file2.write("Random structure")
    file2.write("\n")
    file2.write("MVC: "+mvc_val.get())
    file2.write("\n")
    file2.write("Percent of MVC: "+percent_mvc_e.get()+"%")
    file2.write("\n")
    file2.write("National Instruments input number: "+device_input_e.get())
    file2.write("\n")
    file2.write("Time on target: "+str(score)+"\n")
    file2.write("\n")
    file2.write("\n")
    file2.write("\n")
    for k in range(len(xs)):
        file2.write(str(ys[k]))
        file2.write("   ")
        file2.write(str(xs[k]))
        file2.write("\n")
    
    file2.close()

    if kp_.get():
        pygame.image.save(DISPLAY, save_folder+"/trial"+str(trial+1)+"_block"+str(block+1)+".png")
    return

def save_results_data(trial, block, location):
    if not os.path.isfile(test_save_folder):
        global file
        file = open(test_save_folder, "w")
        file.write(str(datetime.now()))
        file.write("\n")
        if rand_seq_block_.get() == 1:
            file.write("Sequential structure")
        elif rand_seq_block_.get() == 2:
            file.write("Blocked structure")
        elif rand_seq_block_.get() == 3:
            file.write("Random structure")
        file.write("\n")
        file.write("MVC: "+mvc_val.get())
        file.write("\n")
        file.write("Percent of MVC: "+percent_mvc_e.get()+"%")
        file.write("\n")
        file.write("National Instruments input number: "+device_input_e.get())
        file.write("\n")
        file.write("\n")
        file.write("\n")

    file.write("Block number: "+str(block+1)+"  Trial number: "+str(trial+1)+"\n")
    file.write("Trace file: "+location+"\n")
    feedback="Type of feedback given:"
    if kp_.get():
        feedback = feedback + " kp "
    if kr_quant_.get():
        feedback = feedback + "  kr quantitative "
    if kr_qual_.get():
        feedback = feedback + "  kr qualitative "
    file.write(feedback+"\n")
    file.write("Time on target: "+str(score)+"\n")
    file.write("Qualitative score: "+str(qual)+"\n")
    file.write("\n")
    file.write("\n")

def save_csv_data(trial, block, location):
    global csv_file
    csv_test_save = test_save_folder[:-4]+".csv"
    if not os.path.isfile(csv_test_save):
        csv_file = open(csv_test_save, "w")
        csv_file.write("Block")
        csv_file.write(",")
        csv_file.write("Trial")
        csv_file.write(",")
        csv_file.write("Trace file")
        csv_file.write(",")
        csv_file.write("Feedback type")
        csv_file.write(",")
        csv_file.write("Time on Target")
        csv_file.write(",")
        csv_file.write("Qualitative score")
        csv_file.write(",")
        csv_file.write("Time")
        csv_file.write("\n")

    csv_file.write(str(block+1))
    csv_file.write(",")
    csv_file.write(str(trial+1))
    csv_file.write(",")
    csv_file.write(location)
    csv_file.write(",")
    feedback=""
    if kp_.get():
        feedback = feedback + "kp "
    if kr_quant_.get():
        feedback = feedback + "  kr quantitative "
    if kr_qual_.get():
        feedback = feedback + "  kr qualitative"
    csv_file.write(feedback)
    csv_file.write(",")
    csv_file.write(str(score))
    csv_file.write(",")
    csv_file.write(str(qual))
    csv_file.write(",")
    csv_file.write(str(datetime.now()))
    csv_file.write("\n")
    

'''
start_traces

start_traces is the main function of the trace program. When the start trace button is pressed this function is called.


'''
def start_traces():
    #check if the save location is open
    if (save_results.get() == 1 and os.path.exists(test_save_folder)) or (save_raw.get() == 1 and os.path.exists(test_save_folder[:-4])) or (save_csv.get() == 1 and os.path.exists(test_save_folder[:-4]+".csv")):
        messagebox.showinfo("Error", "The save file already exists")
        return

    if (save_results.get() == 1 and test_save_folder == "") or (save_raw.get() == 1 and test_save_folder == "") or (save_csv.get() == 1 and test_save_folder == ""):
        messagebox.showinfo("Error", "No save location entered")
        return

    #generate list of random integers if using random order
    #the randomly generated list will ensure an even distribution of trials
    #the rendomly generated list will also not contain any of the same trial twice in a row
    if rand_seq_block_.get() == 3:
        rand_traces = []

        for i in range(0, int(blocks_per_test_.get())):
            rand_temp=[]
            two_in_row=0
            for i in range(0, int(math.ceil(float(trials_per_block_.get())/float(rand_num_trace_.get())))):
                for i in range(0, int(rand_num_trace_.get())):
                    rand_temp.append(i)

            for i in range(0,50000):
                random.shuffle(rand_temp)
                last=-1
                for k in range(len(rand_temp)):
                    if last == rand_temp[k]:
                        two_in_row=1
                    last = rand_temp[k]
                if two_in_row == 0:
                    break
                else:
                    two_in_row=0
                
            rand_temp = rand_temp[:int(trials_per_block_.get())]
            rand_traces.extend(rand_temp)
                
            
    Start(1)
    
    for i in range(0, int(blocks_per_test_.get())):
        disp_text("Press space to begin block "+str(i+1))
        event = pygame.event.wait()
        middle_pause = 0
        global block_scores
        global middle_block
        block_scores = []
            
        while not (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            event = pygame.event.wait()

            
        for j in range(0, int(trials_per_block_.get())):
            
            if rand_seq_block_.get() == 1:
                location=j
            elif rand_seq_block_.get() == 2:
                location=i
            elif rand_seq_block_.get() == 3:
                location = rand_traces.pop()

            file_location=trace_file_locations[location]
            Trace(file_location)

            results()
                
            time.sleep(0.2)
            
            if kp_.get():
                kp()
                
            if save_raw.get() == 1:
                save_raw_data(j,i,file_location)
            
            if kr_quant_.get():
                kr_quant() 
                time.sleep(float(feedback_time.get()))
            kr_qual()
            


            if save_results.get() == 1:
                save_results_data(j,i,file_location)

            if save_csv.get() == 1:
                save_csv_data(j,i,file_location)

            DISPLAY.fill(WHITE)
            pygame.display.update()
            time.sleep(1)

            block_scores.append(score)
            if int(trials_per_block_.get())/(j+1) <= 2 and middle_pause == 0 and average_.get() == 1 and int(trials_per_block_.get()) > 1:
                middle_block = j + 1
                middle_pause = 1
                middle_block_pause(i)

        if average_.get() == 1 and int(trials_per_block_.get()) > 1:
            end_block_pause(i)
        

    disp_text("Finished")
    time.sleep(2)
    if save_results.get() == 1:
        file.close()
    if save_csv.get() == 1:
        csv_file.close()
    pygame.quit()
    test_folder_exists()
    return



def view_trace():
    file_path = filedialog.askopenfilename()
    get_trace(file_path)
    Start(1)
    pygame.mouse.set_visible(1)

    next_box = resolution[0]/(num_boxes + delay)
    for i in range(len(box_positions)):
            pygame.draw.rect(DISPLAY,RED,(delay*next_box + i*next_box,
                                          resolution[1]-(box_positions[i]*resolution[1])/100,
                                          box_length,
                                          (box_height*resolution[1])/100))



    myfont = pygame.font.SysFont("monospace", 25)
    label3=myfont.render(str(time_per_test)+" seconds to cross screen", 1,(0,0,0))
    if boxes_shown:
        label2=myfont.render("One box shown at a time", 1,(0,0,0))
    else:
        label2=myfont.render("All boxes shown at start", 1,(0,0,0))
    label=myfont.render(trace_file_location_view, 1,(0,0,0))
    text_size=label.get_rect()
    text_x=text_size[2]
    text_y=text_size[3]
    DISPLAY.blit(label, (resolution[0] - text_x -5,resolution[1] - text_y))
    text_size=label2.get_rect()
    text_x=text_size[2]
    text_y=text_size[3]
    DISPLAY.blit(label2, (resolution[0] - text_x -5,resolution[1] - 40 - text_y))
    text_size=label3.get_rect()
    text_x=text_size[2]
    text_y=text_size[3]
    DISPLAY.blit(label3, (resolution[0] - text_x -5,resolution[1] - 80 - text_y))

    
    pygame.display.update()

    event = pygame.event.wait()
    while not (event.type == pygame.KEYDOWN or (pygame.mouse.get_pressed()==(0,0,1))):
            event = pygame.event.wait()
    pygame.quit()
    return



def middle_block_pause(block_number):
    myfont = pygame.font.SysFont("monospace", 75)
    label1=myfont.render("Halfway done block "+str(block_number+1), 1,(0,0,0))

    global half_way_average
    half_way_average = statistics.mean(block_scores)
    label2=myfont.render("Average first half score: "+str(math.ceil(half_way_average*100)/100) + "%", 1,(0,0,0))
    
    text_size=label1.get_rect()
    text_x=text_size[2]
    text_y=text_size[3]
    DISPLAY.blit(label1, (resolution[0]/2 - text_x/2, 200))
    text_size=label2.get_rect()
    text_x=text_size[2]
    text_y=text_size[3]
    DISPLAY.blit(label2, (resolution[0]/2 - text_x/2, 400))
    pygame.display.update()
    time.sleep(6)
    return

    
def end_block_pause(block_number):
    myfont = pygame.font.SysFont("monospace", 75)
    label1=myfont.render("Done block "+str(block_number+1), 1,(0,0,0))

    label2=myfont.render("Average first half score: "+str(math.ceil(half_way_average*100)/100) + "%", 1,(0,0,0))

    back_half = block_scores[middle_block:]
    second_half_average = statistics.mean(back_half)
    label3=myfont.render("Average second half score: "+str(math.ceil(second_half_average*100)/100) + "%", 1,(0,0,0))

    block_average = statistics.mean(block_scores)
    label4=myfont.render("Average block score: "+str(math.ceil(block_average*100)/100) + "%", 1,(0,0,0))
    
    text_size=label1.get_rect()
    text_x=text_size[2]
    text_y=text_size[3]
    DISPLAY.blit(label1, (resolution[0]/2 - text_x/2, 200))
    text_size=label2.get_rect()
    text_x=text_size[2]
    text_y=text_size[3]
    DISPLAY.blit(label2, (resolution[0]/2 - text_x/2, 400))
    text_size=label3.get_rect()
    text_x=text_size[2]
    text_y=text_size[3]
    DISPLAY.blit(label3, (resolution[0]/2 - text_x/2, 600))
    text_size=label4.get_rect()
    text_x=text_size[2]
    text_y=text_size[3]
    DISPLAY.blit(label4, (resolution[0]/2 - text_x/2, 800))
    pygame.display.update()
    time.sleep(10)
    return





def get_test_folder():
    global test_save_folder
    temp = filedialog.asksaveasfilename(initialdir = "/",title = "Save File", defaultextension=".txt", filetypes=[("text files", "*.txt")])
    if not temp == "":
        test_save_folder = temp
        test_folder_exists()
    return

def test_folder_exists():
    test_folder_l = Message(root, text=test_save_folder, font=font_text, width=250)
    test_folder_l.grid(row=15, column=2, pady=10)

    if os.path.exists(test_save_folder) or os.path.exists(test_save_folder[:-4]):
        exists_l.grid(row=17, column=2, pady=10, padx=10)
    else:
        exists_l.grid_forget()
    return


def trace_entry(a=1,b=1,c=1):
    if trials_per_block_.get() and blocks_per_test_.get() and rand_num_trace_.get():
        if rand_seq_block_.get() == 3:
            rand_num_trace_l.grid(row=5, column=10, pady=10)
            rand_num_trace_e.grid(row=5, column=11, padx=10, pady=10)
        else:
            rand_num_trace_l.grid_forget()
            rand_num_trace_e.grid_forget()
        num_trace_files=0
        if rand_seq_block_.get() == 1:
            num_trace_files=int(trials_per_block_.get())
        elif rand_seq_block_.get() == 2:
            num_trace_files=int(blocks_per_test_.get())
        elif rand_seq_block_.get() == 3:
            num_trace_files=int(rand_num_trace_.get())


        for i in range(len(trace_files)):
            trace_files["trace_files{0}_l".format(i)].grid_forget()
            trace_file_locations_b["trace_file_locations{0}_b".format(i)].grid_forget()
            trace_file_locations_l["trace_file_locations{0}_l".format(i)].grid_forget()


        for i in range(0,num_trace_files):
            trace_files["trace_files{0}_l".format(i)].grid(row=i*2, column=0, padx=10)
            trace_file_locations_b["trace_file_locations{0}_b".format(i)].grid(row=i*2, column=1)

        update_trace_files()
        return

def onFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))




def get_trace_files(i):
    file_path = filedialog.askopenfilename()
    if not file_path == "":
        trace_file_locations[i]=(file_path)
        update_trace_files()
    return

def update_trace_files():
    num_trace_files=0
    if rand_seq_block_.get() == 1:
        num_trace_files=int(trials_per_block_.get())
    elif rand_seq_block_.get() == 2:
        num_trace_files=int(blocks_per_test_.get())
    elif rand_seq_block_.get() == 3:
        num_trace_files=int(rand_num_trace_.get())
        
    for i in range(0,40):
        trace_file_locations_l["trace_file_locations{0}_l".format(i)].grid_forget()
        
    for i in range(0,num_trace_files):
        trace_file_locations_l["trace_file_locations{0}_l".format(i)] = Label(frame, text=trace_file_locations[i], font=font_text, width=25)
        trace_file_locations_l["trace_file_locations{0}_l".format(i)].grid(row=i*2+1, column=0, columnspan=2)
    return


def save_configuration():
    global save_configuration_folder
    save_configuration_folder = filedialog.asksaveasfilename(initialdir = "/",title = "Save Configuration File", defaultextension=".txt", filetypes=[("text files", "*.txt")])
    file = open(save_configuration_folder, "w")
    file.write(str(datetime.now()))
    file.write("\n")
    file.write(str(save_results.get()))
    file.write("\n")
    file.write(str(save_csv.get()))
    file.write("\n")
    file.write(str(save_raw.get()))
    file.write("\n")
    file.write(str(default_in.get()))
    file.write("\n")
    file.write(str(default_mvc.get()))
    file.write("\n")
    file.write(str(kp_.get()))
    file.write("\n")
    file.write(str(kr_qual_.get()))
    file.write("\n")
    file.write(str(kr_quant_.get()))
    file.write("\n")
    file.write(str(average_.get()))
    file.write("\n")
    file.write(str(trials_per_block_.get()))
    file.write("\n")
    file.write(str(blocks_per_test_.get()))
    file.write("\n")
    file.write(str(rand_num_trace_.get()))
    file.write("\n")
    file.write(str(rand_seq_block_.get()))

    num_trace_files=0
    if rand_seq_block_.get() == 1:
        num_trace_files=int(trials_per_block_.get())
    elif rand_seq_block_.get() == 2:
        num_trace_files=int(blocks_per_test_.get())
    elif rand_seq_block_.get() == 3:
        num_trace_files=int(rand_num_trace_.get())
    for i in range(0,num_trace_files):
        file.write("\n")
        file.write(str(trace_file_locations[i]))

    file.close()
    return

def load_configuration():
    file_path = filedialog.askopenfilename()
    if not file_path == "":
        file = open(file_path, "r")
        with file as f:
            lines=f.read().splitlines()
        file.close()
        global test_save_folder
        
        save_results.set(lines[1])
        save_csv.set(lines[2])
        save_raw.set(lines[3])
        default_in.set(lines[4])
        default_mvc.set(lines[5])
        kp_.set(lines[6])
        kr_qual_.set(lines[7])
        kr_quant_.set(lines[8])
        average_.set(lines[9])
        trials_per_block_.set(lines[10])
        blocks_per_test_.set(lines[11])
        rand_num_trace_.set(lines[12])
        rand_seq_block_.set(lines[13])
        
        
        num_trace_files=0
        if rand_seq_block_.get() == 1:
            num_trace_files=int(trials_per_block_.get())
        elif rand_seq_block_.get() == 2:
            num_trace_files=int(blocks_per_test_.get())
        elif rand_seq_block_.get() == 3:
            num_trace_files=int(rand_num_trace_.get())
        for i in range(0,num_trace_files):
            trace_file_locations[i] = lines[i+14]

        test_folder_exists()
        trace_entry()
    
    return



root = Tk()
root.title('Trace Game')
font_button = font.Font(family="freesansbold", size=24)
font_text = font.Font(family="freesansbold", size=12)
font_warning = font.Font(family="freesansbold", size=12)

test_b = Button(root, text="Test Device", width=15, font=font_button, command=test_device)
test_b.grid(row=1, column=0, columnspan=3, padx=10, pady=10)


zero_b = Button(root, text="Zero Device", width=15, font=font_button, command=zero_device)
zero_b.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

mvc_b = Button(root, text="Get MVC", width=15, font=font_button, command=get_MVC)
mvc_b.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

trace_b = Button(root, text="Start Trace Tests", width=15, font=font_button, command=start_traces)
trace_b.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

view_trace_b = Button(root, text="View Trace File", width=15, font=font_button, command=view_trace)
view_trace_b.grid(row=8, column=0, columnspan=3, padx=10, pady=10)


spacer = Label(root)
spacer.grid(row=9, column=1, padx=50, pady=10)

save_results_l = Label(root, text="Save results as text file", font=font_text, width=25)
save_results_l.grid(row=10, column=2, pady=10, sticky="W")

save_results = IntVar()
save_results.set(0)
save_results_c = Checkbutton(root, variable=save_results)
save_results_c.config(font=20)
save_results_c.grid(row=10, column=1, padx=10, pady=10, sticky="E")
save_results_c.var = save_results


save_raw_l = Label(root, text="Save all raw data", font=font_text, width=25)
save_raw_l.grid(row=12, column=2, pady=10, sticky="W")

save_raw = IntVar()
save_raw.set(0)
save_raw_c = Checkbutton(root, variable=save_raw)
save_raw_c.config(font=20)
save_raw_c.grid(row=12, column=1, padx=10, pady=10, sticky="E")
save_raw_c.var = save_raw


save_csv_l = Label(root, text="Save results as csv file", font=font_text, width=25)
save_csv_l.grid(row=11, column=2, pady=10, sticky="W")

save_csv = IntVar()
save_csv.set(0)
save_csv_c = Checkbutton(root, variable=save_csv)
save_csv_c.config(font=20)
save_csv_c.grid(row=11, column=1, padx=10, pady=10, sticky="E")
save_csv_c.var = save_csv

test_folder_b = Button(root, text="Change Save Location", font=font_text, width=25, command=get_test_folder)
test_folder_b.grid(row=14, column=2, pady=10, padx=10)

test_folder_l_1 = Label(root, text="Save Location:", font=font_text, width=25)
test_folder_l_1.grid(row=15, column=1, pady=10)

global test_save_folder
test_save_folder = ""
test_folder_l = Message(root, text=test_save_folder, font=font_text)
test_folder_l.grid(row=15, column=2)

exists_l = Label(root, text="Already Exists", font=font_warning, foreground="red")
exists_l.grid(row=18, column=2, pady=10, padx=10)
exists_l.grid_forget()





spacer = Label(root)
spacer.grid(row=8, column=3, padx=50, pady=20)

device_input_l = Label(root, text="Device Input Number", font=font_text)
device_input_l.grid(row=1, column=5, padx=10, pady=10)

default_in = StringVar()
device_input_e = Entry(root, font=font_text, textvariable=default_in)
device_input_e.grid(row=1, column=6, padx=10, pady=10)
default_in.set("1")

percent_mvc_l = Label(root, text="Percent of MVC", font=font_text)
percent_mvc_l.grid(row=3, column=5, padx=10, pady=10)

default_mvc = StringVar()
percent_mvc_e = Entry(root, font=font_text, textvariable=default_mvc)
percent_mvc_e.grid(row=3, column=6, padx=10, pady=10)
default_mvc.set("20")

current_mvc_l = Label(root, text="Current MVC:", font=font_text)
current_mvc_l.grid(row=5, column=5, padx=10, pady=10)

mvc_val = StringVar()
percent_mvc_val_e = Entry(root, font=font_text, textvariable=mvc_val)
percent_mvc_val_e.grid(row=5, column=6, padx=10, pady=10)
mvc_val.set("3")

feedback_time_l = Label(root, text="Feedback display time", font=font_text)
feedback_time_l.grid(row=7, column=5, padx=10, pady=10)

feedback_time = StringVar()
feedback_time_e = Entry(root, font=font_text, textvariable=feedback_time)
feedback_time_e.grid(row=7, column=6, padx=10, pady=10)
feedback_time.set("2")


kp_l = Label(root, text="kp", font=font_text, width=25)
kp_l.grid(row=8, column=6, pady=10, sticky="W")

kp_ = IntVar()
kp_.set(0)
kp_c = Checkbutton(root, variable=kp_)
kp_c.config(font=20)
kp_c.grid(row=8, column=5, padx=10, pady=10, sticky="E")
kp_c.var = kp_


kr_qual_l = Label(root, text="kr qualitative", font=font_text, width=25)
kr_qual_l.grid(row=9, column=6, pady=10, sticky="W")

kr_qual_ = IntVar()
kr_qual_.set(0)
kr_qual_c = Checkbutton(root, variable=kr_qual_)
kr_qual_c.config(font=20)
kr_qual_c.grid(row=9, column=5, padx=10, pady=10, sticky="E")
kr_qual_c.var = kr_qual_


kr_quant_l = Label(root, text="kr quantitative", font=font_text, width=25)
kr_quant_l.grid(row=10, column=6, pady=10, sticky="W")

kr_quant_ = IntVar()
kr_quant_.set(0)
kr_quant_c = Checkbutton(root, variable=kr_quant_)
kr_quant_c.config(font=20)
kr_quant_c.grid(row=10, column=5, padx=10, pady=10, sticky="E")
kr_quant_c.var = kr_quant_

average_l = Label(root, text="Average", font=font_text, width=25)
average_l.grid(row=11,column=6, pady=10, sticky="W")

average_ = IntVar()
average_.set(0)
average_c = Checkbutton(root, variable=average_)
average_c.config(font=20)
average_c.grid(row=11, column=5, padx=10, pady=10, sticky="E")
average_c.var = average_


save_config_b = Button(root, text="Save Configuration", font=font_text, width=15, command=save_configuration)
save_config_b.grid(row=14, column=5, pady=10, padx=10)

load_config_b = Button(root, text="Load Configuration", font=font_text, width=15, command=load_configuration)
load_config_b.grid(row=14, column=6, pady=10, padx=10)






spacer_ = Label(root)
spacer_.grid(row=8, column=8, padx=50, pady=20)


trials_per_block_l = Label(root, text="Trials per Block", font=font_text, width = 25)
trials_per_block_l.grid(row=1, column=10, pady=10)

trials_per_block_ = StringVar()
trials_per_block_e = Entry(root, font=font_text, textvariable=trials_per_block_)
trials_per_block_e.grid(row=1, column=11, padx=10, pady=10)
trials_per_block_.set("1")


blocks_per_test_l = Label(root, text="Blocks per Test", font=font_text, width = 25)
blocks_per_test_l.grid(row=3, column=10, pady=10)

blocks_per_test_ = StringVar()
blocks_per_test_e = Entry(root, font=font_text, textvariable=blocks_per_test_)
blocks_per_test_e.grid(row=3, column=11, padx=10, pady=10)
blocks_per_test_.set("1")


rand_num_trace_l = Label(root, text="Number of trace files", font=font_text, width = 25)
#rand_num_trace_l.grid(row=5, column=10, pady=10)

rand_num_trace_ = StringVar()
rand_num_trace_e = Entry(root, font=font_text, textvariable=rand_num_trace_)
#rand_num_trace_e.grid(row=5, column=11, padx=10, pady=10)
rand_num_trace_.set("1")



rand_seq_block_ = IntVar()
rand_seq_block_.set(1)
Radiobutton(root, text="Sequential", variable=rand_seq_block_, value=1, font=font_text, command=trace_entry).grid(row=7, column=10)
Radiobutton(root, text="Blocked", variable=rand_seq_block_, value=2, font=font_text, command=trace_entry).grid(row=7, column=11)
Radiobutton(root, text="Random", variable=rand_seq_block_, value=3, font=font_text, command=trace_entry).grid(row=7, column=12, padx=20)

trials_per_block_.trace('w', trace_entry)
blocks_per_test_.trace('w', trace_entry)
rand_num_trace_.trace('w', trace_entry)


canvas = Canvas(root, borderwidth=0)
frame= Frame(canvas)
vsb = Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)

vsb.grid(row=8, column=12, columnspan=10, rowspan=20)
canvas.grid(row=8, column=10, rowspan=20)
canvas.create_window((4,4), window=frame, anchor="nw")

frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))




global trace_file_locations
trace_file_locations=[]
for i in range(0,40):
    trace_file_locations.append("")

global trace_files
trace_files={}
for i in range(0,40):
    trace_files["trace_files{0}_l".format(i)] = Label(frame, text="Trace file " + str(i+1), font=font_text)
    trace_files["trace_files{0}_l".format(i)].grid(row=i*2, column=0, padx=10)

for i in range(len(trace_files)):
    trace_files["trace_files{0}_l".format(i)].grid_forget()


global trace_file_locations_b
trace_file_locations_b={}
for i in range(0,40):
    trace_file_locations_b["trace_file_locations{0}_b".format(i)] = Button(frame, text="Select trace file " + str(i+1), font=font_text, command=partial(get_trace_files, i))
    trace_file_locations_b["trace_file_locations{0}_b".format(i)].grid(row=i*2, column=1)


for i in range(len(trace_files)):
    trace_file_locations_b["trace_file_locations{0}_b".format(i)].grid_forget()


global trace_file_locations_l
trace_file_locations_l={}
for i in range(0,40):
    trace_file_locations_l["trace_file_locations{0}_l".format(i)] = Label(frame, text=trace_file_locations[i], font=font_text)
    trace_file_locations_l["trace_file_locations{0}_l".format(i)].grid(row=i*2+1, column=0, columnspan=2)

for i in range(len(trace_files)):
    trace_file_locations_l["trace_file_locations{0}_l".format(i)].grid_forget()

trace_entry()






root.mainloop()






