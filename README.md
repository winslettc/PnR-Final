# PnR-Final
The final project for my Programming and Robotics class

### Methods Students Can Use

`self.rotate()`
Lets you change the encode value and choose the direction to turn. It will let you measure how many degrees each encode value will produce.

`self.isClear()`
Will perform a three point check around self.MIDPOINT and will return True if no distance is shorter than the stop dist.

`self.choosePath()`
Performs self.flushScan() and then self.wideScan() to scan the area in front. The method averages the distances and returns a string "right" or "left" depending on the average distance around the MIDPOINT.

`self.encR(x)`, `self.encL(x)`, `self.encF(x)`, `self.encB(x)`
Will set the encode value passed to the method and executes the rotate, fwd, or bwd

`self.wideScan()`
This will fill your self.scan array with distances self.MIDPOINT-60, self.MIDPOINT+60, +2

`self.flushScan()`
Resets the list that stores the distances of the ultrasonic sensor. 

`self.stop()`
A more reliable stop command. It repeats the GoPiGo's stop() method three times to assure that the command is not lost. 
