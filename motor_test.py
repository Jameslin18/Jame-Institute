# This program will let you test your motor_1 and brushless motor.
# Make sure your battery is not connected if you are going to calibrate it at first.
# Since you are testing your motor, I hope you don't have your propeller attached to it otherwise you are in trouble my friend...?
# This program is made by AGT @instructable.com. DO NOT REPUBLISH THIS PROGRAM... actually the program itself is harmful                                             pssst Its not, its safe.

import pigpio  # importing GPIO library
import RPi.GPIO as GPIO
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

duty_cycle = 255
freq = 37500

pi = pigpio.pi()

pi.set_servo_pulsewidth(motor_1, 0)

max_value = 2000  # change this if your ESC's max value is different or leave it be
min_value = 1000  # change this if your ESC's min value is different or leave it be


def menu():
    print("| cal | set | man | con | arm | cs_on | stop | send |\n")

    inp = raw_input()
    if inp == "man":
        manual_drive()
    elif inp == "cal":
        calibrate()
    elif inp == "set":
        esc_settings()
    elif inp == "arm":
        arm()
    elif inp == "con":
        control()
    elif inp == "cs_on":
        cont_servo()
    elif inp == "send":
        send()
    elif inp == "stop":
        stop()
    else:
        print("cringe.")


def raw_input():
    print("Input:")
    inp = input()
    return inp


def send():
    pi.set_PWM_frequency(motor_1, freq)
    pi.set_PWM_dutycycle(motor_1, duty_cycle)
    pi.set_servo_pulsewidth(motor_1, 1700)
    #print("Freq: ", pi.get_PWM_frequency(motor_1), "Hz")
    menu()

def send_inp():
    pi.set_PWM_frequency(motor_1, freq)
    pi.set_PWM_dutycycle(motor_1, duty_cycle)
    pi.set_servo_pulsewidth(motor_1, raw_input())
    manual_drive()

def manual_drive():  # You will use this function to program your ESC if required
    print("You have selected manual option so give a value between 0 and you max value")
    while True:
        inp = raw_input()
        if str(inp) == "stop":
            stop()
            break
        elif str(inp) == "menu":
            menu()
            break
        elif str(inp) == "send":
            send()
            break
        elif int(inp) >= max_value:
            print("Maximum value is ", max_value)
            pi.set_PWM_frequency(motor_1, freq)
            pi.set_PWM_dutycycle(motor_1, duty_cycle)
            pi.set_servo_pulsewidth(motor_1, max_value)
        else:
            send_inp()
            break

        print("motor_1 status: ", pi.get_servo_pulsewidth(motor_1))

def esc_settings():
    pi.set_servo_pulsewidth(motor_1, 0)
    print("disconnect battery and press Enter")
    inp = raw_input()
    if inp == '':
        pi.set_servo_pulsewidth(motor_1, max_value)
        time.sleep(1)
        print(
            "Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
        time.sleep(1)
        print("press Enter at the intended sequence")
        if inp == '':
            pi.set_servo_pulsewidth(motor_1, 0)
            print("ESC is set and you can disconnect battery.")

def calibrate():  # This is the auto calibration procedure of a normal ESC
    pi.set_servo_pulsewidth(motor_1, 0)
    print("disconnect battery and press Enter")
    inp = raw_input()
    if inp == '':
        pi.set_servo_pulsewidth(motor_1, 1700)
        time.sleep(1)
        pi.set_servo_pulsewidth(motor_1, 0)
        time.sleep(1)
        pi.set_servo_pulsewidth(motor_1, 1500)
        time.sleep(1)
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
        elif inp == "menu":
            menu()
            break
        else:
            print("bruh")


def arm():  # This is the arming procedure of an ESC
    print("Connect the battery and press Enter")
    inp = raw_input()
    if inp == '':
        pi.set_servo_pulsewidth(motor_1, 1200)
        time.sleep(1)
        pi.set_servo_pulsewidth(motor_1, 0)
        time.sleep(1)
        pi.set_servo_pulsewidth(motor_1, max_value)
        time.sleep(1)
        pi.set_servo_pulsewidth(motor_1, min_value)
        time.sleep(1)
        pi.set_servo_pulsewidth(motor_1, 0)
        manual_drive()


def stop():  # This will stop every action your Pi is performing for ESC of course.
    pi.set_servo_pulsewidth(motor_1, 0)
    pi.stop()


def cont_servo():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_1, GPIO.OUT)
    inp = raw_input()
    p = GPIO.PWM(servo_1, 1000)  # GPIO 17 for PWM with 1000Hz
    p.start(5)  # Initialization

    p.ChangeDutyCycle(2.5)
    time.sleep(5)
    p.ChangeDutyCycle(11.5)  # may need to be adjusted

    if inp == "menu":
        GPIO.cleanup()
        menu()
    p = GPIO.PWM(servo_1, 1000)  # GPIO 17 for PWM with 50Hz
    p.start(2.5)  # Initialization
    try:
        while True:
            p.ChangeDutyCycle(5)
            time.sleep(0.5)
            p.ChangeDutyCycle(7.5)
            time.sleep(0.5)
            p.ChangeDutyCycle(10)
            time.sleep(0.5)
            p.ChangeDutyCycle(12.5)
            time.sleep(0.5)
            p.ChangeDutyCycle(10)
            time.sleep(0.5)
            p.ChangeDutyCycle(7.5)
            time.sleep(0.5)
            p.ChangeDutyCycle(5)
            time.sleep(0.5)
            p.ChangeDutyCycle(2.5)
            time.sleep(0.5)
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()

menu()
# This is the start of the program actually, to start the function it needs to be initialized before calling... stupid python.
