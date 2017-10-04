import pigo
import time  # import just in case students need
import random

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
        # Our servo turns the sensor. What angle of the servo( ) method sets it straight?
        self.MIDPOINT = 84
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.SAFE_STOP_DIST = 30
        # YOU DECIDE: How close can an object get (cm) before we have to stop? immediately
        self.HARD_STOP_DIST = 15
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.LEFT_SPEED = 200
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
                "b": ("Break dance", self.break_dance),
                "c": ("Calibrate", self.calibrate),
                "s": ("Check status", self.status),
                "q": ("Quit", quit_now)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = raw_input("Your selection: ")
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

    def safety_check(self):
        """Checks for safe and hard stop distances, also stops 90 degrees and scans"""
        self.servo(self.MIDPOINT)   #Look straight ahead
        if self.dist() < self.SAFE_STOP_DIST:
            return False
        #Loop 4 times
        for x in range(2):
            if not self.is_clear():
                print("NOT GOING TO DANCE")
                return False
            print("SCANNING!")
            while self.right_rot():
                self.flush_scan()
            self.set_speed(80,80)
            self.right_rot(10)
            print("PREPARING!")
        return True
            # turn 90 degrees
        #Scan again

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

    def nav(self):
        """auto pilots and attempts to maintain original heading"""
        logging.debug("Starting the nav method")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")


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
