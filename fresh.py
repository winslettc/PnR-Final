from gopigo import *
import time

class Fresh:
    def __init__(self):
        print("\n-----This better work!-------\n")
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
        self.nav()

    def nav(self):
        print("\n-----STARTING NAVIGATION-------\n")
        count = 0  # keep track of how many loops we've done without moving
        while True:
            count += 1
            if self.is_clear():
                count = 0  # reset the frustration counter
                raw_input("press ENTER to start driving")
                self.fwd()
                while self.checkAhead():
                    pass
                #self.checkRight()
                #self.checkLeft()
            else:  # it hasn't been clear for a while. let's turn out of here
                if count > 3:
                    self.encR(10)

    def checkAhead(self):
        # do stuff so long as we need to avoid obstacles
        while self.dist() < self.STOP_DIST:
            # check if we're touching something
            if self.dist() < 2:
                self.stop()
                # restore default speeds before shutting down
                self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
                return False  # give up
            # check if something is REALLY close
            elif self.dist() < int(self.STOP_DIST * .5):
                # HARD TURN
                self.set_speed(self.LEFT_SPEED, int(self.RIGHT_SPEED*.2))
            # check if something is close
            elif self.dist() < self.STOP_DIST:
                # SOFTER TURN
                self.set_speed(self.LEFT_SPEED, int(self.RIGHT_SPEED*.5))
        # restore default speeds now that we're successful
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
        return True  # we look cool for now, roll on



    ##############################################
    ##### FUNCTIONS NOT INTENDED TO BE OVERWRITTEN
    def fwd(self):
        fwd()

    def set_speed(self, left, right):
        set_left_speed(left)
        set_right_speed(right)
        print('Left speed set to: ' + str(left) + ' // Right set to: ' + str(right))

    def encF(self, enc):
        print('Moving ' + str((enc / 18)) + ' rotation(s) forward')
        enc_tgt(1, 1, enc)
        fwd()
        time.sleep(1 * (enc / 18) + .4)

    def encR(self, enc):
        print('Moving ' + str((enc / 18)) + ' rotation(s) right')
        enc_tgt(1, 1, enc)
        right_rot()
        time.sleep(1 * (enc / 18) + .4)
        # UPDATE THE TURN TRACKER SO I KNOW MY HEADING
        self.turn_track += enc

    def encL(self, enc):
        print('Moving ' + str((enc / 18)) + ' rotation(s) left')
        enc_tgt(1, 1, enc)
        left_rot()
        time.sleep(1 * (enc / 18) + .4)
        # UPDATE THE TURN TRACKER SO I KNOW MY HEADING
        self.turn_track -= enc

    def encB(self, enc):
        print('Moving ' + str((enc / 18)) + ' rotations(s) backwards')
        enc_tgt(1, 1, enc)
        bwd()
        time.sleep(1 * (enc / 18) + .4)

    def servo(self, val):
        print('Moving servo to ' + str(val) + 'deg')
        servo(val)
        time.sleep(.1)

    def dist(self):
        measurement1 = us_dist(15)
        time.sleep(.01)
        measurement2 = us_dist(15)
        time.sleep(.01)
        if abs(measurement1 - measurement2) > 5:
            measurement1 = int((measurement1 + measurement2 + us_dist(15)) / 3)
        print('I see something ' + str(measurement1) + "cm away")
        return measurement1

    # DUMP ALL VALUES IN THE SCAN ARRAY
    def flush_scan(self):
        self.scan = [None] * 180

    # SEARCH 120 DEGREES COUNTING BY 2's
    def wide_scan(self, count=2):
        # dump all values
        self.flush_scan()
        for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60, count):
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

    def is_clear(self):
        self.stop()
        print("Running the is_clear method.")
        for x in range((self.MIDPOINT - 15), (self.MIDPOINT + 15), 5):
            servo(x)
            time.sleep(.1)
            scan1 = us_dist(15)
            time.sleep(.1)
            # double check the distance
            scan2 = us_dist(15)
            time.sleep(.1)
            # if I found a different distance the second time....
            if abs(scan1 - scan2) > 2:
                scan3 = us_dist(15)
                time.sleep(.1)
                # take another scan and average the three together
                scan1 = (scan1 + scan2 + scan3) / 3
            self.scan[x] = scan1
            print("Degree: " + str(x) + ", distance: " + str(scan1))
            if scan1 < self.STOP_DIST:
                print("Doesn't look clear to me")
                return False
        return True

    # DECIDE WHICH WAY TO TURN
    def choose_path(self):
        print('Considering options...')
        if self.is_clear():
            return "fwd"
        else:
            self.wide_scan()
        avgRight = 0
        avgLeft = 0
        for x in range(self.MIDPOINT - 60, self.MIDPOINT):
            if self.scan[x]:
                avgRight += self.scan[x]
        avgRight /= 60
        print('The average dist on the right is ' + str(avgRight) + 'cm')
        for x in range(self.MIDPOINT, self.MIDPOINT + 60):
            if self.scan[x]:
                avgLeft += self.scan[x]
        avgLeft /= 60
        print('The average dist on the left is ' + str(avgLeft) + 'cm')
        if avgRight > avgLeft:
            return "right"
        else:
            return "left"

    def stop(self):
        print('All stop.')
        for x in range(3):
            stop()
            time.sleep(0.1)

    def calibrate(self):
        print("Calibrating...")
        servo(self.MIDPOINT)
        response = raw_input("Am I looking straight ahead? (y/n): ")
        if response == 'n':
            while True:
                response = raw_input("Turn right, left, or am I done? (r/l/d): ")
                if response == "r":
                    self.MIDPOINT += 1
                    print("Midpoint: " + str(self.MIDPOINT))
                    servo(self.MIDPOINT)
                    time.sleep(.01)
                elif response == "l":
                    self.MIDPOINT -= 1
                    print("Midpoint: " + str(self.MIDPOINT))
                    servo(self.MIDPOINT)
                    time.sleep(.01)
                else:
                    print("Midpoint now saved to: " + str(self.MIDPOINT))
                    break
        response = raw_input("Do you want to check if I'm driving straight? (y/n)")
        if response == 'y':
            while True:
                set_left_speed(self.LEFT_SPEED)
                set_right_speed(self.RIGHT_SPEED)
                print("Left: " + str(self.LEFT_SPEED) + "//  Right: " + str(self.RIGHT_SPEED))
                self.encF(18)
                response = raw_input("Reduce left, reduce right or drive? (l/r/d): ")
                if response == 'l':
                    self.LEFT_SPEED -= 10
                elif response == 'r':
                    self.RIGHT_SPEED -= 10
                elif response == 'd':
                    self.encF(18)
                else:
                    break


try:
    f = Fresh()
except (KeyboardInterrupt, SystemExit):
    stop()
