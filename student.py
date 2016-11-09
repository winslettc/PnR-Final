import pigo
import time
import random
from gopigo import *


'''
THIS IS THE TEACHER'S EXAMPLE. YOU (PROBABLY) SHOULD NOT BE SEEING THIS
'''

class GoPiggy(pigo.Pigo):
    # CUSTOM INSTANCE VARIABLES GO HERE. You get the empty self.scan array from Pigo
    # You may want to add a variable to store your default speed
    MIDPOINT = 90
    STOP_DIST = 25
    turn_track = 0
    #if I encR(1) how many degrees does it turn?
    DEG_PER_ENC = 15

    # CONSTRUCTOR
    def __init__(self):
        print("Piggy has be instantiated!")
        # this method makes sure Piggy is looking forward and drives straight
        self.calibrate()
        self.setSpeed(self.LEFT_SPEED, self.RIGHT_SPEED)
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        while True:
            self.stop()
            self.handler()

    ##### HANDLE IT
    def handler(self):
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like
        menu = {"1": ("Navigate forward", self.nav),
                "2": ("Rotate", self.rotate),
                "3": ("Dance", self.dance),
                "4": ("Calibrate", self.calibrate),
                "s": ("Check status", self.status),
                "q": ("Quit", quit)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        #
        ans = input("Your selection: ")
        menu.get(ans, [None, error])[1]()

    # A SIMPLE DANCE ALGORITHM
    def dance(self):
        print("Piggy dance")
        ##### WRITE YOUR FIRST PROJECT HERE


    # AUTONOMOUS DRIVING
    def nav(self):

        while True:
            #Go forward while you can, look for options if you can't
            if(self.isClear()):
                print("It looks clear ahead of me. Starting cruise")
                self.cruise()

            #Choose the best path
            options = self.findOptions()
            ideal_turn = self.MIDPOINT + (self.turn_track * self.DEG_PER_ENC)
            #if there is an option other than the filler [0]
            if options[1]:
                print("I've go a few options to consider")
                best_option = options[1]
                for x in options:
                    if abs(x - ideal_turn) < best_option:
                        best_option = x
                print("My best option is at "+str(best_option)+" degrees.")
                change = self.MIDPOINT - best_option
                print("That means I need to turn by "+str(change)+ "degrees.")
                if change > 0:
                    self.encR(change * self.DEG_PER_ENC)
                else:
                    self.encL(abs(change) * self.DEG_PER_ENC)
            else:
                print("No options. Going to back up.")
                self.encB(18)
                if self.turn_track > 0:
                    self.encR(self.turn_track)
                elif self.turn_track < 0:
                    self.encL(abs(self.turn_track))

    #Drive forward as long as nothing's in the way
    def cruise(self):
        #aim forward
        servo(self.MIDPOINT)
        time.sleep(.05)
        #start moving forward
        fwd()
        #start an infinite loop
        while True:
            #break the loop if the sensor reading is closer than our stop dist
            if us_dist(15) < self.STOP_DIST:
                break
            #break every now and then
            time.sleep(.05)
        #stop if the sensor loop broke
        self.stop()

    #Kenny's method to identify options, builds a list of 20 deg. options
    def findOptions(self):
        #erase anything saved in the scan array
        self.flushScan()
        #move the servo, take sensor reading, and store in scan array
        for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60, 2):
            servo(x)
            time.sleep(.1)
            #TODO: Add a double-check
            self.scan[x] = us_dist(15)
            time.sleep(.05)
        #count will be used to find 20 degrees of contigeous open space
        count = 0
        #this list will keep track of windows of free space
        option = [0]
        #looping through the scan array to think about our options
        for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60, 2):
            #if the distance is far enough away, count this spot
            if self.scan[x] > self.STOP_DIST:
                count += 1
            #if there was a spot that wasn't safe, reset counter
            else:
                count = 0
            #if we've found 10 in a row, let's bookmark the spot
            if count > 9:
                print("Found an option from " + str(x - 20) + " to " + str(x) + " degrees")
                count = 0
                option.append(x-10)
        #we're done finding spots, now let's list the options
        for x in option:
            #skip the 0 option, that was just filler
            if not x.__index__() == 0:
                print(" Choice # " + str(x.__index__()) + " is@ " + str(x) + " degrees. ")
        #return the list of options we've found
        return option

    #modifying the parent's turn to also track the difference from original heading
    def encR(self, enc):
        self.turn_track -= enc
        if(self.turn_track > 0):
            print("The exit is to my right by " + str(self.turn_track) + "units")
        else:
            print("The exit is to my left by " + str(abs(self.turn_track)) + "units")
        super(pigo.Pigo, self).encR(enc)

    def encL(self, enc):
        self.turn_track += enc
        if(self.turn_track > 0):
            print("The exit is to my right by " + str(self.turn_track) + "units")
        else:
            print("The exit is to my left by " + str(abs(self.turn_track)) + "units")
        super(pigo.Pigo, self).encL(enc)



####################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit


####################################################
######## THE ENTIRE APP IS THIS ONE LINE....
g = GoPiggy()
