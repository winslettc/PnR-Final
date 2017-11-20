import pigo
import time  # import just in case students need
import random
from gopigo import *
import datetime

# setup logs
import logging
LOG_LEVEL = logging.INFO
LOG_FILE = "/home/pi/PnR-Final/log_robot.log"  # don't forget to make this file!
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)


class Piggy(pigo.Pigo):
    """Student project, inherits teacher Pigo class which wraps all RPi specific functions"""

    def __init__(self):
        """The robot's constructor: sets variables and runs menu loop"""
        print("I have been instantiated!")
        self.start_time = datetime.datetime.utcnow()
        # Our servo turns the sensor. What angle of the servo( ) method sets it straight?
        self.MIDPOINT = 84
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.SAFE_STOP_DIST = 40
        # YOU DECIDE: How close can an object get (cm) before we have to stop? immediately
        self.HARD_STOP_DIST = 15
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.LEFT_SPEED = 195
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.RIGHT_SPEED = 200
        # This one isn't capitalized because it changes during runtime, the others don't
        self.turn_track = 0
        # Our scan list! The index will be the degree and it will store distance
        self.scan = [None] * 180
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        while True:
            self.stop()
            self.menu()

    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like to add an experimental method
        menu = {"n": ("Navigate forward", self.nav),
                "cs": ("Cupid Shuffle", self.cupid_shuffle),
                #"b": ("Break dance", self.break_dance),
                #"fc": ("Full Count", self.full_count),
                #"c": ("Calibrate", self.calibrate),
                #"s": ("Check status", self.status),
                "tr": ("Test Restore Method", self.test_restore),
                "c": ("Cruise", self.cruise),
                "sc": ("Smart Cruise", self.smart_cruise),
                "q": ("Quit", quit_now)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = raw_input("\n----Your selection:----\n ")
        # activate the item selected
        menu.get(ans, [None, error])[1]()

    # YOU DECIDE: How does your GoPiggy dance?
    def cupid_shuffle(self):
        """executes a series of methods that add up to a cupid shuffle"""
        print("\n---- LET'S CUPID SHUFFLE ----\n")
        ##### WRITE YOUR FIRST PROJECT HERE
        if self.safety_check():
            self.to_the_right()
            self.to_the_left()
            self.now_kick()
            self.cha_cha()
            self.walk_it_by_youself()

    def to_the_right(self):
        """subroutine of dance method/ turns right and then pulses for times"""
        for x in range(1):
            self.encR(10)
            for x in range(4):
                self.encF(10)
                self.stop()
                time.sleep(.2)

    def to_the_left(self):
        """subroutine of dance method/ turns left and then pulses four times"""
        for x in range(1):
            self.encL(32)
            for x in range(4):
                self.encF(10)
                self.stop()
                time.sleep(.2)

    def now_kick(self):
        """subroutine of dance/ moves robot back and forth"""
        for x in range(1):
            self.encR(10)
            for x in range (4):
                self.set_speed(250,250)
                self.encF(5)
                self.encB(5)

    def cha_cha(self):
        """Subroutine of dance/ moves right, left, shakes servo"""
        for x in range(2):
            self.encR(3)
            self.servo_shake()
            self.encL(3)
            self.servo_shake()
            self.set_speed(255,255)
            self.encR(32)
            self.encL(32)

    def walk_it_by_yourself(self):
        """Moves in a full circle to the right then to the left"""
        for x in range(2):
            self.set_speed(80,80)
            self.encR(40)
            self.stop()
            time.sleep(.2)

    def servo_shake(self):
        """Subroutine of dance function/ moves servo head back and forth"""
        for x in range(2):
            self.servo(70)
            self.servo(120)

    def break_dance(self):
        """Dance routine for robot"""
        print("\n---- LET'S BREAK DANCE ----\n")
        self.circle_spin()
        self.wheelie()
        self.circle_spin()
        self.servo_bob()
        self.square()
        self.robot()

    def robot(self):
        """subroutine of break dance/ broken up moves with servo and driving"""
        pass

    def circle_spin(self):
        """Makes the robot spin in a 360 motion/ subroutine of break_dance"""
        for x in range (1):
            self.set_speed(255,255)
            self.encL(40)

    def wheelie(self):
        """Makes the robot do a wheelie"""
        for x in range (1):
            self.set_speed(255,255)
            self.encF(5)
            self.encB(5)

    def servo_bob(self):
        """Moves servo like a full scan - like a head bob/scan"""
        for x in range (3):
            self.servo(30)
            self.stop()
            time.sleep(.5)
            self.servo(150)

    def square(self):
        """Drives the robot in a square"""
        self.encF(10)
        self.encR(10)
        self.encB(10)
        self.encL(10)
        self.encR(10)

    #END OF DANCE METHODS##########################################################################################################
    #BEGINNING OF NAVIGATION METHODS

    def safety_check(self):
        #HOW to make continuous scanning??? while rotating
        """Checks for safe and hard stop distances, also stops 90 degrees and scans"""
        self.servo(self.MIDPOINT)   #Look straight ahead
        if self.dist() < self.SAFE_STOP_DIST:
            print("NOT GOING TO DANCE")
            return False
        #Loop 4 times
        for x in range(3):
            if not self.is_clear():
                return False
            print("SCANNING")
            is_safe = True
            self.right_rot()
            for x in range(5):
                if self.dist()< self.SAFE_STOP_DIST:
                    break
                time.sleep(.5)
            self.stop()
            return is_safe
            while self.right_rot():
                self.right_rot()
                self.wide_scan()
                self.set_speed(80,80)
                print("FINISHING!")
        return True
            # turn 90 degrees
        #Scan again

    def cruise(self):
        """Drives robot forward while the coast is clear and scans continuously"""
        self.servo(self.MIDPOINT)
        print("\n----Aligning servo to Midpoint----\n")
        self.set_speed(120, 120)
        print("\n----Setting speed----\n")
        while self.dist() > self.SAFE_STOP_DIST:
            print("\n----DRIVING, ready to go!----\n")
            self.fwd()
            time.sleep(.1)

    #Counts obstacles in a 360 using right turns (90 degree angle)
    def full_count(self):
        """360 degree view of obstacles around"""
        count=0
        for x in range(4):
            count += self.obstacle_count()
            self.right_turn()
        print(count)

    #widescan counter
    def obstacle_count(self):
        """Scans and estimates the numbers of obstacles within sight in a 360 view"""
        self.wide_scan(count = 6)
        found_something = False
        counter = 0
        threshold = 50
        for distance in self.scan:
            if distance and distance < threshold and not found_something:
                found_something = True
                counter +=1
                print ("\n----Object # %d found, I think----\n" % counter)
            if distance and distance > threshold and found_something:
                found_something = False
                counter += 0
        print("\n----I see %d objects----\n" % counter)
        return counter

    def right_turn(self):
        """"90 degree right turn"""
        self.encR(12)

    def left_turn(self):
        """"90 degree left turn"""
        self.encL(12)

    def restore_heading(self):
        """returns robot to original heading/ straightens out to original orientation"""
        if self.turn_track > 0:
            self.encL(abs(self.turn_track))
            #Turn left to the absolute value or turn track
        elif self.turn_track < 0:
            self.encR(abs(self.turn_track))
            #Turn right to ab value of turn track
        print("\n----Turn track is currently: %d----\n" % self.turn_track)
        print("\n----Restoring Heading----\n")

    def datetime(self):
        """Datetime function, how long it takes to run a function"""
        right_now = datetime.datetime.utcnow()
        difference = (right_now - self.start_time).seconds
        print("\n----It took you %d seconds to run this----\n" % difference)

    def test_restore(self):
        """Tests restore heading method to determine usability"""
        print("Turn track is currently: %d" % self.turn_track)
        self.set_speed(80,80)
        self.servo(self.MIDPOINT)
        #Set speed and move servo to midpoint
        print("\n---Moving Right---\n")
        self.encR(12)
        print("\n---Moving Left---\n")
        self.encL(5)
        time.sleep(1)
        #Move robot so restore method can be tested
        print("\n----Testing Restore Method...----\n")
        self.restore_heading()
        #Run restore method
        print("\n---Restored to original heading----\n")

    def nav(self):
        """auto pilots and attempts to maintain original heading"""
        logging.debug("Starting the nav method")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        self.datetime()
        while True:
            if self.is_clear():
                time.sleep(1)
                self.smart_turn()
                self.servo(self.MIDPOINT)
                print("\n----Setting Midpoint----\n")
                self.cruise()
                time.sleep(.4)
            else:
                print("\n----Something is blocking my path----\n")
                self.right_turn()
                self.encB(5)
                if self.is_clear():
                    time.sleep(1)
                    self.servo(self.MIDPOINT)
                    self.cruise()
                    time.sleep(.4)
                else:
                    self.left_turn()
                    if self.is_clear():
                        time.sleep(1)
                        self.cruise()
                        time.sleep(.4)

    def smart_turn(self):
        """Find angle with greatest distance"""
        ang = 0
        largest_dist = 0
        print("\n----Scanning the Area----\n")
        self.servo(self.MIDPOINT)
        self.wide_scan(count = 5)
        for index, distance in enumerate(self.scan):
            if distance > largest_dist:
                largest_dist = distance
                ang = index
        print("\n----The best angle is %d----\n" % ang)
        turn = 7 * abs(ang - self.MIDPOINT) / 90   ##calculate how much it should turn to the valid direction.
        print("\n----Turning to the best angle----\n")
        if ang <= self.MIDPOINT:
            self. encR(turn)
        if ang > self.MIDPOINT:
            self.encL(turn)

    def smooth_turn(self):
        """Rotates to find free space and records time to limit spins by robot"""
        self.right_rot()
        start = datetime.datetime.utcnow()
        self.servo(self.MIDPOINT)
        print("\n----Servo is set to the midpoint----\n")
        self.set_speed(80,80)
        while True:
            if self.dist() > 100:
                self.stop()
                print("\n----I think I have found a safe place to go!----\n")
            elif datetime.datetime.utcnow() - start > datetime.timedelta(seconds = 10):
                self.stop()
                print("\n----I give up, it has been too long----\n")
            time.sleep(.2)

    def smart_cruise(self):
        """Cruise function that slows down as the robot approaches an object"""
        MAX_SPEED = 200
        MID_SPEED = 150
        LOW_SPEED = 100
        self.fwd()
        while True:
            dis = self.dist()
            if dis < self.HARD_STOP_DIST:
                print("\n----Hard stop triggered----\n")
                break
            elif dis > 200:
                print("\n----Obstacle not near----\n")
                self.set_speed(MAX_SPEED-5, MAX_SPEED)
            elif dis > 100:
                print("\n----Obstacle nearing----\n")
                self.set_speed(MID_SPEED-4, MID_SPEED)
            else:
                print("\n----Obstacle very close----\n")
                self.set_speed(LOW_SPEED-3, LOW_SPEED)
            time.sleep(.1)  # just to slow down the loop a bit
        self.stop()
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)

    def mid_scan(self, count=2):
        """moves servo 120 degrees and fills scan array, default count=2"""
        self.flush_scan()
        for x in range(self.MIDPOINT-20, self.MIDPOINT+20, count):
            servo(x)
            time.sleep(.1)
            scan1 = us_dist(15)
            time.sleep(.1)
            #double check the distance
            scan2 = us_dist(15)
            #if I found a different distance the second time....
            if abs(scan1 - scan2) > 2:
                scan3 = us_dist(15)
                time.sleep(.1)
                #take another scan and average the three together
                scan1 = (scan1+scan2+scan3)/3
            self.scan[x] = scan1
            print("Degree: "+str(x)+", distance: "+str(scan1))
            time.sleep(.01)

    def semi_scan(self, count=2):
        """moves servo 120 degrees and fills scan array, default count=2"""
        self.flush_scan()
        for x in range(self.MIDPOINT-40, self.MIDPOINT+40, count):
            servo(x)
            time.sleep(.1)
            scan1 = us_dist(15)
            time.sleep(.1)
            #double check the distance
            scan2 = us_dist(15)
            #if I found a different distance the second time....
            if abs(scan1 - scan2) > 2:
                scan3 = us_dist(15)
                time.sleep(.1)
                #take another scan and average the three together
                scan1 = (scan1+scan2+scan3)/3
            self.scan[x] = scan1
            print("Degree: "+str(x)+", distance: "+str(scan1))
            time.sleep(.01)

    def quick_scan(self, count=2):
        """moves servo 120 degrees and fills scan array, default count=2"""
        self.flush_scan()
        for x in range(self.MIDPOINT-5, self.MIDPOINT+5, count):
            servo(x)
            time.sleep(.1)
            scan1 = us_dist(15)
            time.sleep(.1)
            #double check the distance
            scan2 = us_dist(15)
            #if I found a different distance the second time....
            if abs(scan1 - scan2) > 2:
                scan3 = us_dist(15)
                time.sleep(.1)
                #take another scan and average the three together
                scan1 = (scan1+scan2+scan3)/3
            self.scan[x] = scan1
            time.sleep(.01)

    def straight_scan(self):
        """moves servo 120 degrees and fills scan array, default count=2"""
        self.flush_scan()
        for x in range(self.MIDPOINT, count):
            servo(x)
            time.sleep(.1)
            scan1 = us_dist(15)
            time.sleep(.1)
            # double check the distance
            scan2 = us_dist(15)
            # if I found a different distance the second time....
            if abs(scan1 - scan2) > 2:
                scan3 = us_dist(15)
                time.sleep(.1)
                # take another scan and average the three together
                scan1 = (scan1 + scan2 + scan3) / 3
            self.scan[x] = scan1
            print("Degree: " + str(x) + ", distance: " + str(scan1))
            time.sleep(.01)

    def safest_path(self):
        """find the safest way to travel; safest is the way with most space btwn obstacles"""\
        """create all lists and set variables to be overwritten"""
        angle_go = []
        width = []
        free_space = 0
        largest_angle = 0
        init_space = 360
        """scan it 18 encoders"""
        for x in range(3):
             """take the distances first"""
             self.wide_scan(count = 6)
             print ("\n----Scanning for free space...----\n")
             for dist in enumerate(self.scan):
                 #In terms of angles (fix this?)
                 if dist:
                     """if it's a free space"""
                     if distance > 90:
                         print("\n----There is free space ahead----\n")
                         """and it's the start of said space"""
                         #Print if there is free space
                     if free_space == 0:
                        """declare where the space starts"""
                        init_space = distance
                     """add width of space"""
                     free_space += 1
                     """but if it is an object, not a free space"""
                     #Print if there is an object
                     if distance < 90:
                        print("\n----There is no free space ahead----\n")
                        """the space has ended; width and angle measurement added to the list"""
                        free_space = 0
                        width.append(distance - init_space)
                        angle_go.append(int(angle + init_space) / 2)
                 """90 right turn to scan space"""
                 self.encL(10)
                 print("\n----Turning Right to Scan----\n")
                 #Previously an encode left (10) function was here important?
             """Compares angle measurements to determine which width = largest"""
             for number, ang in enumerate(width):
                    """if there's a newly discovered largest angle"""
                    if ang > largest_angle:
                        """set a the largest angle to be that newly found one"""
                        largest_angle = ang
                        """definitive largest angle is named"""
        self.servo(self.MIDPOINT)
        print("\n----Setting Midpoint----\n")
        self.encL(int(angle_go[largest_angle] / 12))
        print("\n----Turning to greatest free space----\n")
        self.cruise()
        print("\n----Cruising----\n")
#Moving in an infinite circle-- fix this

###################################################
############### STATIC FUNCTIONS

def error():
    """records general, less specific error"""
    logging.error("ERROR")
    print('ERROR')


def quit_now():
    """shuts down app"""
    raise SystemExit

##################################################################
######## The app starts right here when we instantiate our GoPiggy


try:
    g = Piggy()
except (KeyboardInterrupt, SystemExit):
    pigo.stop_now()
except Exception as ee:
    logging.error(ee.__str__())
