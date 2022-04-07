# This program will let you test your ESC and brushless motor.
# Make sure your battery is not connected if you are going to calibrate it at first.
# Since you are testing your motor, I hope you don't have your propeller attached to it otherwise you are in trouble my friend...?
# This program is made by AGT @instructable.com. DO NOT REPUBLISH THIS PROGRAM... actually the program itself is harmful                                             pssst Its not, its safe.

import pigpio  # importing GPIO library
import os  # importing os library so as to communicate with the system
import time  # importing time library to make Rpi wait because its too impatient

os.system("sudo pigpiod")  # Launching GPIO library
time.sleep(1)  # As i said it is too impatient and so if this delay is removed you will get an error

ESC = 2  # Connect the ESC in this GPIO pin

pi = pigpio.pi()

pi.set_servo_pulsewidth(ESC, 0)

max_value = 2500  # change this if your ESC's max value is different or leave it be
min_value = 500  # change this if your ESC's min value is different or leave it be
print("For first time launch, select calibrate \n")
print("cal OR man OR con OR arm OR stop \n")


def raw_input():
    print("Input:")
    inp = input()
    return inp



def manual_drive():  # You will use this function to program your ESC if required
    print("You have selected manual option so give a value between 0 and you max value")
    while True:
        inp = raw_input()

        if inp == "stop":
            stop()
            break
        elif inp == "con":
            control()
            break
        elif inp == "arm":
            arm()
            break
        elif int(inp) >= max_value:
            print("Maximum value is ", max_value)
            pi.set_servo_pulsewidth(ESC, max_value)
        else:
            pi.set_servo_pulsewidth(ESC, raw_input())

        print(pi.get_servo_pulsewidth(ESC))
        time.sleep(5)


def calibrate():  # This is the auto calibration procedure of a normal ESC
    pi.set_servo_pulsewidth(ESC, 0)
    print("Disconnect the battery and press Enter")
    inp = raw_input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC, max_value)
        print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
        raw_input()
        if inp == '':
            pi.set_servo_pulsewidth(ESC, min_value)
            print("Weird eh! Special tone")
            time.sleep(7)
            print("Wait for it ....")
            time.sleep(5)
            print("Im working on it, DONT WORRY JUST WAIT.....")
            pi.set_servo_pulsewidth(ESC, 0)
            time.sleep(2)
            print("Arming ESC now...")
            pi.set_servo_pulsewidth(ESC, min_value)
            time.sleep(1)
            print("See.... uhhhhh")
            manual_drive()  # You can change this to any other function you want


def control():
    print("I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'")
    time.sleep(1)
    speed = 1500  # change your speed if you want to.... it should be between 700 - 2000
    print(
        "Controls - a to decrease speed & d to increase speed OR q to decrease a lot of speed & e to increase a lot of speed")
    while True:
        pi.set_servo_pulsewidth(ESC, speed)
        inp = raw_input()

        if inp == "q":
            speed -= 100  # decrementing the speed like hell
            print("speed = %d" % speed)
        elif inp == "e":
            speed += 100  # incrementing the speed like hell
            print("speed = %d" % speed)
        elif inp == "d":
            speed += 10  # incrementing the speed
            print("speed = %d" % speed)
        elif inp == "a":
            speed -= 10  # decrementing the speed
            print("speed = %d" % speed)
        elif inp == "stop":
            stop()  # going for the stop function
            break
        elif inp == "man":
            manual_drive()
            break
        elif inp == "arm":
            arm()
            break
        else:
            print("bruh")


def arm():  # This is the arming procedure of an ESC
    print("Connect the battery and press Enter")
    inp = raw_input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC, 0)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, max_value)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, min_value)
        time.sleep(1)
        manual_drive()


def stop():  # This will stop every action your Pi is performing for ESC of course.
    pi.set_servo_pulsewidth(ESC, 0)
    pi.stop()


# This is the start of the program actually, to start the function it needs to be initialized before calling... stupid python.
u_inp = raw_input()
if u_inp == "man":
    manual_drive()
elif u_inp == "cal":
    calibrate()
elif u_inp == "arm":
    arm()
elif u_inp == "con":
    control()
elif u_inp == "stop":
    stop()
else:
    print("cringe.")
