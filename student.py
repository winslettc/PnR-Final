import pigo
import time
import random
from gopigo import *


'''
MR. A's Final Student Helper
'''

class GoPiggy(pigo.Pigo):

    ########################
    ### INSTANCE VARIABLES - we *instantiate* a class, each one gets these
    #### (you're an instance the Human class)
    ########################

    #Our servo turns the sensor. What angle of the servo( ) method sets it straight?
    MIDPOINT = 83
    #YOU DECIDE: How close can an object get (cm) before we have to stop?
    STOP_DIST = 30
    #YOU DECIDE: What left motor power helps straighten your fwd()?
    LEFT_SPEED = 140
    #YOU DECIDE: What left motor power helps straighten your fwd()?
    RIGHT_SPEED = 140
    #YOU DECIDE: How long does it take your robot to turn 1 degree?
    TIME_PER_DEGREE = 0.029
    #YOU DECIDE: What speed modifier should we use when turning?
    TURN_MODIFIER = .6
    #This one isn't capitalized because it changes during runtime, the others don't
    turn_track = 0
    #Our scan list! The index will be the degree and it will store distance
    scan = [None] * 180

    ########################
    ### CONTSTRUCTOR - this special method auto-runs when we instantiate a class
    #### (your constructor lasted about 9 months)
    ########################

    def __init__(self):
        print("Piggy has be instantiated!")
        # this method makes sure Piggy is looking forward and drives straight
        self.setSpeed(self.LEFT_SPEED, self.RIGHT_SPEED)
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
        # store the user's answer
        ans = input("Your selection: ")
        # activate the item selected
        menu.get(ans, [None, error])[1]()

    #YOU DECIDE: How does your GoPiggy dance?
    def dance(self):
        print("Piggy dance")
        ##### WRITE YOUR FIRST PROJECT HERE


    ########################
    ### TURN METHODS - they're passably accurate!
    ### (start a turn then pauses for the time needed to rotate to the given angle)
    ########################

    def turnR(self, deg):
        #a mediocre way to track how far we move from our ideal angle
        self.turn_track += deg
        print("The exit is " + str(self.turn_track) + " degrees away.")
        #use the setSpeed method to slow down our turns
        self.setSpeed(self.LEFT_SPEED * self.TURN_MODIFIER,
                      self.RIGHT_SPEED * self.TURN_MODIFIER)
        #start turning (using the GoPiGo API)
        right_rot()
        #wait the sec we found is neeeded to turn 1deg multiplied by the desired deg
        time.sleep(deg * self.TIME_PER_DEGREE)
        self.stop()
        #return power to the default values
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


    #use the GoPiGo API method to set the motor speeds to the given numbers
    def setSpeed(self, left, right):
        #let's keep the user informed.
        print("Left speed: " + str(left) + " // " + "Right speed: " + str(right))
        set_left_speed(int(left))
        set_right_speed(int(right))
        time.sleep(.05)

    ########################
    ### MAIN LOGIC LOOP - the core algorithm of my navigation
    ### (kind of a big deal)
    ########################

    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("[ Press CTRL + C to stop me, then run stop.py ]\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        # this is the loop part of the "main logic loop"
        while True:
            # if it's clear in front of me...
            if self.isClear():
                # drive until something's in front of me. Good idea? you decide.
                self.cruise()
            #YOU DECIDE: check to see if you should backup?
            self.backUp()
            # IF I HAD TO STOP, PICK A BETTER PATH
            turn_target = self.kenny()
            # a positive turn is right
            if turn_target > 0:
                self.turnR(turn_target)
            # negative degrees mean left
            else:
                # let's remove the negative with abs()
                self.turnL(abs(turn_target))

    # This method drives forward as long as nothing's in the way
    def cruise(self):
        # Extra credit: Upgrade this so it looks around while driving
        # Use the GoPiGo API's method to aim the sensor forward
        servo(self.MIDPOINT)
        #give the robot time to move
        time.sleep(.05)
        # start driving forward
        fwd()
        # start an infinite loop
        while True:
            # break the loop if the sensor reading is closer than our stop dist
            if us_dist(15) < self.STOP_DIST:
                break
            #YOU DECIDE: How many seconds do you wait in between a check?
            time.sleep(.05)
        # stop if the sensor loop broke
        self.stop()

    def backUp(self):
        if us_dist(15) < 10:
            print("Too close. Backing up for half a second")
            bwd()
            time.sleep(.5)
            self.stop()

    #################################
    ### THE KENNY METHOD OF SCANNING - experimental

    def kenny(self):
        #Activate our scanner!
        self.wideScan()
        # count will keep track of contigeous positive readings
        count = 0
        # list of all the open paths we detect
        option = [0]
        #YOU DECIDE: What do we add to STOP_DIST when looking for a path fwd?
        SAFETY_BUFFER = 30
        #YOU DECIDE: what increment do you have your wideScan set to?
        INC = 2

        ###########################
        ######### BUILD THE OPTIONS
        #loop from the 60 deg right of our middle to 60 deg left of our middle
        for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60):
            # ignore all blank spots in the list
            if self.scan[x]:
                # add 30 if you want, this is an extra safety buffer
                if self.scan[x] > (self.STOP_DIST + SAFETY_BUFFER):
                    count += 1
                # if this reading isn't safe...
                else:
                    # aww nuts, I have to reset the count, this path won't work
                    count = 0
                #YOU DECIDE: Is 16 degrees the right size to consider as a safe window?
                if count > (16 / INC) - 1:
                    # SUCCESS! I've found enough positive readings in a row
                    print("---FOUND OPTION: from " + str(x - 16) + " to " + str(x))
                    #set the counter up again for next time
                    count = 0
                    #add this option to the list
                    option.append(x - 8)

        ####################################
        ############## PICK FROM THE OPTIONS - experimental

        #The biggest angle away from our midpoint we could possibly see is 90
        bestoption = 90
        #the turn it would take to get us aimed back toward the exit - experimental
        ideal = -self.turn_track
        print("\nTHINKING. Ideal turn: " + str(ideal) + " degrees\n")
        # x will iterate through all the angles of our path options
        for x in option:
            # skip our filler option
            if x != 0:
                # the change to the midpoint needed to aim at this path
                turn = self.MIDPOINT - x
                # state our logic so debugging is easier
                print("\nPATH @  " + str(x) + " degrees means a turn of " + str(turn))
                # if this option is closer to our ideal than our current best option...
                if abs(ideal - bestoption) > abs(ideal - turn):
                    # store this turn as the best option
                    bestoption = turn
        if bestoption > 0:
            input("\nABOUT TO TURN RIGHT BY: " + str(bestoption) + " degrees")
        else:
            input("\nABOUT TO TURN LEFT BY: " + str(abs(bestoption)) + " degrees")
        return bestoption

    #########################################
    ### SCANNER - move head to take sensor readings

    def wideScan(self):
        #dump all values that might be in our list
        self.flushScan()
        #YOU DECIDE: What increment should we use when scanning?
        for x in range(self.MIDPOINT-60, self.MIDPOINT+60, +2):
            # move the sensor that's mounted to our servo
            servo(x)
            #give some time for the servo to move
            time.sleep(.1)
            #take our first measurement
            scan1 = us_dist(15)
            time.sleep(.1)
            #double check the distance
            scan2 = us_dist(15)
            #if I found a different distance the second time....
            if abs(scan1 - scan2) > 2:
                scan3 = us_dist(15)
                time.sleep(.1)
                #take another scan and average? the three together - you decide
                scan1 = (scan1+scan2+scan3)/3
            self.scan[x] = scan1
            print("Degree: "+str(x)+", distance: "+str(scan1))
            time.sleep(.01)

    #########################################
    ### QUICK CHECK - is it safe to drive forward?

    #This returns true or false
    def isClear(self) -> bool:
        #YOU DECIDE: What range from our midpoint should we check?
        for x in range((self.MIDPOINT - 20), (self.MIDPOINT + 20), 4):
            #move the sensor
            servo(x)
            #Give a little time to turn the servo
            time.sleep(.1)
            #Take our first measurement
            scan1 = us_dist(15)
            #Give a little time for the measurement
            time.sleep(.1)
            #Take the same measurement
            scan2 = us_dist(15)
            # Give a little time for the measurement
            time.sleep(.1)
            #if there's a significant difference between the measurements
            if abs(scan1 - scan2) > 2:
                #take a third measurement
                scan3 = us_dist(15)
                time.sleep(.1)
                #take another scan and average? the three together - you decide
                scan1 = (scan1 + scan2 + scan3) / 3
            #store the measurement in our list
            self.scan[x] = scan1
            #print the finding
            print("Degree: " + str(x) + ", distance: " + str(scan1))
            #If any one finding looks bad
            if scan1 < self.STOP_DIST:
                print("\n--isClear method returns FALSE--\n")
                return False
        print("\n--isClear method returns TRUE--\n")
        return True



####################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit

##################################################################
######## The app starts right here when we instantiate our GoPiggy

g = GoPiggy()
