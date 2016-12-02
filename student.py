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
    MIDPOINT = 88
    STOP_DIST = 25
    LEFT_SPEED = 150
    RIGHT_SPEED = 150

    #0.0 is the heading of the exit, every turn changes this number
    turn_track = 0.0
    TIME_PER_DEGREE = 0.011
    TURN_MODIFIER = .5

    # CONSTRUCTOR
    def __init__(self):
        print("Piggy has be instantiated!")
        # this method makes sure Piggy is looking forward and drives straight
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

    ########################
    ###MY NEW TURN METHODS because encR and encL just don't cut it
    ########################
    #takes number of degress and turns right accordingly
    def turnR(self, deg):
        #blah blah blah
        self.turn_track += deg
        print("The exit is " + str(self.turn_track) + " degrees away.")
        self.setSpeed(self.LEFT_SPEED * self.TURN_MODIFIER,
                      self.RIGHT_SPEED * self.TURN_MODIFIER)
        right_rot()
        time.sleep(deg * self.TIME_PER_DEGREE)
        self.stop()
        self.setSpeed(self.LEFT_SPEED, self.RIGHT_SPEED)

    def turnL(self, deg):
        #adjust the tracker so we know how many degrees away our exit is
        self.turn_track -= deg
        print("The exit is " + str(self.turn_track) + " degrees away.")
        #slow down for more exact turning
        self.setSpeed(self.LEFT_SPEED * self.TURN_MODIFIER,
                      self.RIGHT_SPEED * self.TURN_MODIFIER)
        #do turn stuff
        left_rot()
        #use our experiments to calculate the time needed to turn
        time.sleep(deg*self.TIME_PER_DEGREE)
        self.stop()
        #return speed to normal cruise speeds
        self.setSpeed(self.LEFT_SPEED, self.RIGHT_SPEED)



    def setSpeed(self, left, right):
        print("Left speed: " + str(left))
        print("Right speed: " + str(right))
        set_left_speed(int(left))
        set_right_speed(int(right))
        time.sleep(.05)

    # Explain the purpose of the method
    # Central logic loop of my navigation
    def nav(self):
        print("Parent nav")

        # main app loop
        while True:
            # CRUISE FORWARD
            if self.isClear():
                self.cruise()
            # IF I HAD TO STOP, PICK A BETTER PATH
            turn_target = self.kenny()

            if turn_target < 0:
                self.turnR(abs(turn_target))
            else:
                self.turnL(turn_target)

    # replacement turn method. Find the best option to turn
    def kenny(self):
        # use the built-in wideScan
        self.wideScan()
        # count will keep track of contigeous positive readings
        count = 0
        # list of all the open paths we detect
        option = [0]
        SAFETY_BUFFER = 30
        # what increment do you have your widescan set to?
        INC = 2

        #############################################################
        ################### BUILD THE OPTIONS
        #############################################################
        for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60):
            if self.scan[x]:
                # add 30 if you want, this is an extra safety buffer
                if self.scan[x] > (self.STOP_DIST + SAFETY_BUFFER):
                    count += 1
                # if this reading isn't safe...
                else:
                    # aww nuts, I have to reset the count, this path won't work
                    count = 0
                if count == (20 / INC):
                    # SUCCESS! I've found enough positive readings in a row to count
                    print("Found an option from " + str(x - 20) + " to " + str(x))
                    count = 0
                    option.append(x - 10)

        ###############################################################
        ################### PICK FROM THE OPTIONS
        ###############################################################
        bestoption = 90
        winner = 0
        for x in option:
            # skip our filler option. Behold the magenta!
            if not x.__index__() == 0:
                print("Choice # " + str(x.__index__()) + " is@ " + str(x) + " degrees")
                ideal = self.turn_track + self.MIDPOINT
                print("My ideal choice would be " + str(ideal))
                if bestoption > abs(ideal - x):
                    bestoption = abs(ideal - x)
                    winner = x - self.MIDPOINT
        if winner > 0:
            print("I think we should turn left by " + str(winner))
        else:
            print("I think we should turn right by " + str(abs(winner)))
        return winner

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



####################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit


####################################################
######## THE ENTIRE APP IS THIS ONE LINE....
g = GoPiggy()
