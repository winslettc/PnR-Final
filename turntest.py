from gopigo import *
print("Hi Grace, you're so smart.")
while True:
    t = float(input("How much would you like to turn?"))
    rspeed = int(input("What would you like for your right speed?"))
    lspeed = int(input("What would you like for your left speed?"))

    set_left_speed(lspeed)
    set_right_speed(rspeed)

    #It seems the enc_tgt doesn't work. Let's try controlling using time
    enc_tgt(1, 1, turn)
    right_rot()

    time.sleep(t)

    stop()
    #left_rot(turn)
