# This program will let you test your motor_1 and brushless motor.
# Make sure your battery is not connected if you are going to calibrate it at first.
# Since you are testing your motor, I hope you don't have your propeller attached to it otherwise you are in trouble my friend...?
# This program is made by AGT @instructable.com. DO NOT REPUBLISH THIS PROGRAM... actually the program itself is harmful                                             pssst Its not, its safe.

import pigpio  # importing GPIO library
import os  # importing os library so as to communicate with the system
import time  # importing time library to make Rpi wait because its too impatient

os.system("sudo pigpiod")  # Launching GPIO library
time.sleep(1)  # As i said it is too impatient and so if this delay is removed you will get an error

print("For first time launch, select calibrate \n")

# Connect the ESC in this GPIO pin
motor_1 = 17  # left
motor_2 = 27  #
motor_3 = 22  #

servo_1 = 5  #
servo_2 = 6  #
servo_3 = 13  #

pi = pigpio.pi()

pi.set_servo_pulsewidth(motor_1, 0)

max_value = 2500  # change this if your ESC's max value is different or leave it be
min_value = 500  # change this if your ESC's min value is different or leave it be


def init():
    print("| cal | man | con | arm | cs_on | stop | send |\n")

    inp = raw_input()
    if inp == "man":
        manual_drive()
    elif inp == "cal":
        calibrate()
    elif inp == "arm":
        arm()
    elif inp == "con":
        control()
    elif inp == "cs_on":
        cont_servo()
    elif inp == "send":
        send_1000()
    elif inp == "stop":
        stop()
    else:
        print("cringe.")


def raw_input():
    print("Input:")
    inp = input()
    return inp


def send_1000():
    while True:
        #pi.set_mode(motor_1, pigpio.OUTPUT)
        #pi.set_servo_pulsewidth(motor_1, 1000)
        pi.set_PWM_frequency(motor_1, 60)
        pi.set_PWM_dutycycle(motor_1, 255)
        # pi.set_mode(motor_1, pigpio.INPUT)
        # print("motor_1 status: ", pi.get_servo_pulsewidth(motor_1))


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
        elif inp == "cs_on":
            cont_servo()
            break
        elif inp == "send":
            send_1000()
        elif int(inp) >= max_value:
            print("Maximum value is ", max_value)
            pi.set_servo_pulsewidth(motor_1, max_value)
        else:
            pi.set_servo_pulsewidth(motor_1, raw_input())

        print("motor_1 status: ", pi.get_servo_pulsewidth(motor_1))
        time.sleep(3)


def calibrate():  # This is the auto calibration procedure of a normal ESC
    pi.set_servo_pulsewidth(motor_1, 0)
    print("Disconnect the battery and press Enter")
    inp = raw_input()
    if inp == '':
        pi.set_servo_pulsewidth(motor_1, max_value)
        print(
            "Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
        raw_input()
        if inp == '':
            pi.set_servo_pulsewidth(motor_1, min_value)
            print("Weird eh! Special tone")
            time.sleep(7)
            print("Wait for it ....")
            time.sleep(5)
            print("Im working on it, DONT WORRY JUST WAIT.....")
            pi.set_servo_pulsewidth(motor_1, 0)
            time.sleep(2)
            print("Arming motor now...")
            pi.set_servo_pulsewidth(motor_1, min_value)
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
        pi.set_servo_pulsewidth(motor_1, speed)
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
        pi.set_servo_pulsewidth(motor_1, 0)
        time.sleep(1)
        pi.set_servo_pulsewidth(motor_1, max_value)
        time.sleep(1)
        pi.set_servo_pulsewidth(motor_1, min_value)
        time.sleep(1)
        manual_drive()


def stop():  # This will stop every action your Pi is performing for ESC of course.
    pi.set_servo_pulsewidth(motor_1, 0)
    pi.stop()


def cont_servo():
    pi.set_servo_pulsewidth(servo_1, 500)
    inp = raw_input()
    if inp == "s off":
        pi.set_servo_pulsewidth(servo_1, 0)
        init()


init()
# This is the start of the program actually, to start the function it needs to be initialized before calling... stupid python.
