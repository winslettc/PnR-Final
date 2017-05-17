import pigo
import time
import random
import logging

'''
MR. A's Final Project Student Helper
'''

class GoPiggy(pigo.Pigo):

    ########################
    ### CONTSTRUCTOR - this special method auto-runs when we instantiate a class
    #### (your constructor lasted about 9 months)
    ########################

    def __init__(self):
        # LOG_LEVEL = logging.INFO
        LOG_LEVEL = logging.DEBUG
        LOG_FILE = "/home/pi/PnR-Final/log_robot.log"
        LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
        logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)
        print("Your piggy has be instantiated!")
        # Our servo turns the sensor. What angle of the servo( ) method sets it straight?
        self.MIDPOINT = 90
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.STOP_DIST = 30
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.LEFT_SPEED = 140
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.RIGHT_SPEED = 140
        # This one isn't capitalized because it changes during runtime, the others don't
        self.turn_track = 0
        # Our scan list! The index will be the degree and it will store distance
        self.scan = [None] * 180
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        while True:
            self.stop()
            self.menu()


    ########################
    ### CLASS METHODS - these are the actions that your object can run
    #### (they can take parameters can return stuff to you, too)
    #### (they all take self as a param because they're not static methods)
    ########################


    ##### DISPLAY THE MENU, CALL METHODS BASED ON RESPONSE
    def menu(self):
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like to add an experimental method
        menu = {"n": ("Navigate forward", self.nav),
                "d": ("Dance", self.dance),
                "c": ("Calibrate", self.calibrate),
                "t": ("Turn test", self.turn_test),
                "s": ("Check status", self.status),
                "q": ("Quit", quit)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = raw_input("Your selection: ")
        # activate the item selected
        menu.get(ans, [None, error])[1]()

    def count_obstacles(self):
        # run a scan
        self.wide_scan()
        # count how many obstacles I've found
        counter = 0
        # starting state assumes no obstacle
        found_something = False
        # loop through all my scan data
        for x in self.scan:
            # if x is not None and really close
            if x and x <= self.STOP_DIST:
                # if I've already found something
                if found_something:
                    print("obstacle continues")
                # if this is a new obstacle
                else:
                    # switch my tracker
                    found_something = True
                    print("start of new obstacle")
            # if my data show safe distances...
            if x and x > self.STOP_DIST:
                # if my tracker had been triggered...
                if found_something:
                    print("end of obstacle")
                    # reset tracker
                    found_something = False
                    # increase count of obstacles
                    counter += 1
        print('Total number of obstacles in this scan: ' + str(counter))
        return counter


    def turn_test(self):
        while True:
            ans = raw_input('Turn right, left or stop? (r/l/s): ')
            if ans == 'r':
                val = int(raw_input('/nBy how much?: '))
                self.encR(val)
            elif ans == 'l':
                val = int(raw_input('/nBy how much?: '))
                self.encL(val)
            else:
                break
        self.restore_heading()

    def restore_heading(self):
        print("Now I'll turn back to the starting postion.")
        # make self.turn_track go back to zero
        self.set_speed(90,90)
        if self.turn_track > 0:
            print('I must have turned right a lot now I should turn left')
            self.encL(abs(self.turn_track))
        elif self.turn_track < 0:
            print('I must have turned left a lot and now I have to self.encR(??)')
            self.encR(abs(self.turn_track))
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)

    def maneuver(self):
        # I have turned right and need to check my left side
        if self.turn_track > 0:
            while self.is_clear():
                # go forward a little bit
                self.encF(5)
                # look left
                self.servo(self.MIDPOINT + 60)
                # see if it's above self.STOP_DIST + 20
                if self.dist() > self.STOP_DIST + 20:
                    self.restore_heading()
                    # shut this down and get ready to cruise forward
                    return
                # look straight ahead again
                self.servo(self.MIDPOINT)
        # I have turned left and need to check my right side
        else:

    def encR(self, enc):
        pigo.Pigo.encR(self, enc)
        self.turn_track += enc

    def encL(self, enc):
        pigo.Pigo.encL(self, enc)
        self.turn_track -= enc

    #YOU DECIDE: How does your GoPiggy dance?
    def dance(self):
        print("Piggy dance")
        ##### WRITE YOUR FIRST PROJECT HERE


    ########################
    ### MAIN LOGIC LOOP - the core algorithm of my navigation
    ### (kind of a big deal)
    ########################

    def nav(self):
        logging.debug("Starting the nav method")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("[ Press CTRL + C to stop me, then run stop.py ]\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        # this is the loop part of the "main logic loop"
        count = 0
        while True:
            while self.is_clear():
                self.encF(10)
                count += 1
                if count > 5 and self.turn_track != 0:
                    logging.info("Restoring heading, count at: " + str(count))
                    self.restore_heading()
                    count = 0
            answer = self.choose_path()
            # WISH: turn slowly until you see the path is clear the path is clear
            if answer == "left":
                self.encL(6)
            elif answer == "right":
                self.encR(6)



####################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit

##################################################################
######## The app starts right here when we instantiate our GoPiggy

try:
    g = GoPiggy()
except (KeyboardInterrupt, SystemExit):
    from gopigo import *
    stop()
except Exception as ee:
    logging.error(ee.__str__())
