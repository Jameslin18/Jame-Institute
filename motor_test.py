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

# max and min REV smart servo pulsewidth
min_servo = 550
max_servo = 2450

motor_duty_cycle = 255
motor_freq = 16000

servo_duty_cycle = 255
servo_freq = 500

pi = pigpio.pi()

pi.set_servo_pulsewidth(motor_1, 0)

max_value = 2000  # change this if your ESC's max value is different or leave it be
min_value = 1000  # change this if your ESC's min value is different or leave it be


def menu():
    print("----------------------------------------------")
    print("| cal | set | start | man | cs | stop |")
    print("----------------------------------------------")

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
    elif inp == "cs":
        cont_servo()
    elif inp == "send":
        send()
    elif inp == "start":
        esc_startup()
    elif inp == "stop":
        stop()
    elif inp == "troll":
        troll()
    else:
        print("cringe.")
        menu()


def raw_input():
    print("\nInput:")
    inp = input()
    return inp


def esc_startup():
    pi.set_servo_pulsewidth(motor_1, min_value)
    menu()


def send():
    pi.set_PWM_frequency(motor_1, motor_freq)
    pi.set_PWM_dutycycle(motor_1, motor_duty_cycle)
    pi.set_servo_pulsewidth(motor_1, 1100)
    menu()


def manual_drive():  # You will use this function to program your ESC if required
    print("You have selected manual option, enter number to set throttle.")
    print("Enter 'menu' to return.")

    while True:
        throttle = raw_input()

        if int(throttle) > max_value:
            print("Maximum value is ", max_value, ".")
            pi.set_PWM_frequency(motor_1, motor_freq)
            pi.set_PWM_dutycycle(motor_1, motor_duty_cycle)
            pi.set_servo_pulsewidth(motor_1, max_value)

        elif 0 < int(throttle) < 1100:
            print("Minimum value is 1100.")
            pi.set_PWM_frequency(motor_1, motor_freq)
            pi.set_PWM_dutycycle(motor_1, motor_duty_cycle)
            pi.set_servo_pulsewidth(motor_1, 1100)

        elif int(throttle) == 0:
            pi.set_servo_pulsewidth(motor_1, min_value)

        elif throttle == "menu":
            menu()
            break

        elif int(throttle):
            pi.set_PWM_frequency(motor_1, motor_freq)
            pi.set_PWM_dutycycle(motor_1, motor_duty_cycle)
            pi.set_servo_pulsewidth(motor_1, throttle)

        else:
            print("cringe.")


def esc_settings():
    pi.set_servo_pulsewidth(motor_1, 0)
    print("You have selected esc setting.")
    print("Disconnect battery and press Enter.")
    inp = raw_input()
    if inp == '':
        pi.set_servo_pulsewidth(motor_1, max_value)
        time.sleep(1)
        print("Connect the battery now, press Enter at the intended sequence.")
        raw_input()
    else:
        print("bruh.")
        pi.set_servo_pulsewidth(motor_1, 0)
        menu()

        if inp == '':
            pi.set_servo_pulsewidth(motor_1, min_value)
            print("Press Enter again when different sequence runs again.")
            raw_input()
        else:
            print("bruh.")
            pi.set_servo_pulsewidth(motor_1, 0)
            menu()

            if inp == '':
                pi.set_servo_pulsewidth(motor_1, min_value)
                print("There should be two beeps as confirmation.")
                print("After this the ESC is set and you can disconnect battery.")
            else:
                print("bruh.")
                pi.set_servo_pulsewidth(motor_1, 0)
                menu()


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
    print("You have selected continous servo control.")
    print("Enter menu to return.")
    print("\n[left] [right] [stop] [off]")

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(servo_1, GPIO.OUT)

    while True:
        servo_inp = raw_input()

        if servo_inp == "left":
            cont = GPIO.PWM(servo_1, 100)
            cont.start(0)
            cont.ChangeDutyCycle(5)  # left -90 deg position

        elif servo_inp == "right":
            pi.set_PWM_frequency(motor_1, servo_freq)
            pi.set_PWM_dutycycle(motor_1, servo_duty_cycle)
            pi.set_servo_pulsewidth(servo_1, min_servo)

        elif servo_inp == "stop":
            pi.set_PWM_frequency(motor_1, servo_freq)
            pi.set_PWM_dutycycle(motor_1, servo_duty_cycle)
            pi.set_servo_pulsewidth(servo_1, 1500)

        elif servo_inp == "menu":
            menu()
            break

        else:
            print("cringe.")


def troll():
    print("\n"
          "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⠶⠶⣶⠶⠶⠶⠶⠶⠶⠶⠶⠶⢶⠶⠶⠶⠤⠤⠤⠤⣄⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n",
          "⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠋⠀⠀⠊⠀⠀⠀⠀⠀⠀⠀⠀⠒⠒⠒⠀⠀⠀⠀⠤⢤⣤⣄⠉⠉⠛⠛⠷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n",
          "⠀⠀⠀⠀⠀⠀⠀⣰⠟⠀⠀⠀⠀⠀⠐⠋⢑⣤⣶⣶⣤⡢⡀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣄⡂⠀⠀⠶⢄⠙⢷⣤⠀⠀⠀⠀⠀⠀⠀⠀\n",
          "⠀⠀⠀⠀⠀⠀⣸⡿⠚⠉⡀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⢢⠀⠀⡀⣰⣿⣿⣿⣿⣦⡀⠀⠀⠡⡀⢹⡆⠀⠀⠀⠀⠀⠀⠀\n",
          "⠀⠀⠀⠀⢀⣴⠏⠀⣀⣀⣀⡤⢤⣄⣠⣿⣿⣿⣿⣻⣿⣿⣷⠀⢋⣾⠈⠙⣶⠒⢿⣿⣿⣿⣿⡿⠟⠃⠀⡀⠡⠼⣧⡀⠀⠀⠀⠀⠀⠀\n",
          "⠀⠀⢀⣴⣿⢃⡴⢊⢽⣶⣤⣀⠀⠊⠉⠉⡛⢿⣿⣿⣿⠿⠋⢀⡀⠁⠀⠀⢸⣁⣀⣉⣉⣉⡉⠀⠩⡡⠀⣩⣦⠀⠈⠻⣦⡀⠀⠀⠀⠀\n",
          "⠀⢠⡟⢡⠇⡞⢀⠆⠀⢻⣿⣿⣷⣄⠀⢀⠈⠂⠈⢁⡤⠚⡟⠉⠀⣀⣀⠀⠈⠳⣍⠓⢆⢀⡠⢀⣨⣴⣿⣿⡏⢀⡆⠀⢸⡇⠀⠀⠀⠀\n",
          "⠀⣾⠁⢸⠀⠀⢸⠀⠀⠀⠹⣿⣿⣿⣿⣶⣬⣦⣤⡈⠀⠀⠇⠀⠛⠉⣩⣤⣤⣤⣿⣤⣤⣴⣾⣿⣿⣿⣿⣿⣧⠞⠀⠀⢸⡇⠀⠀⠀⠀\n",
          "⠀⢹⣆⠸⠀⠀⢸⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣟⣛⠛⠛⣛⡛⠛⠛⣛⣋⡉⠉⣡⠶⢾⣿⣿⣿⣿⣿⣿⡇⠀⠀⢀⣾⠃⠀⠀⠀⠀\n",
          "⠀⠀⠻⣆⡀⠀⠈⢂⠀⠀⠀⠠⡈⢻⣿⣿⣿⣿⡟⠁⠈⢧⡼⠉⠙⣆⡞⠁⠈⢹⣴⠃⠀⢸⣿⣿⣿⣿⣿⣿⠃⠀⡆⣾⠃⠀⠀⠀⠀\n",
          "⠀⠀⠀⠈⢻⣇⠀⠀⠀⠀⠀⠀⢡⠀⠹⣿⣿⣿⣷⡀⠀⣸⡇⠀⠀⣿⠁⠀⠀⠘⣿⠀⠀⠘⣿⣿⣿⣿⣿⣿⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀\n",
          "⠀⠀⠀⠀⠀⠹⣇⠀⠠⠀⠀⠀⠀⠡⠐⢬⡻⣿⣿⣿⣿⣿⣷⣶⣶⣿⣦⣤⣤⣤⣿⣦⣶⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀\n",
          "⠀⠀⠀⠀⠀⠀⠹⣧⡀⠡⡀⠀⠀⠀⠑⠄⠙⢎⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⢿⡇⠀⠀⠀⠀⠀⠀\n",
          "⠀⠀⠀⠀⠀⠀⠀⠈⠳⣤⡐⡄⠀⠀⠀⠈⠂⠀⠱⣌⠻⣿⣿⣿⣿⣿⣿⣿⠿⣿⠟⢻⡏⢻⣿⣿⣿⣿⣿⣿⣿⠀⢸⡇⠀⠀⠀⠀⠀⠀\n",
          "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⢮⣦⡀⠂⠀⢀⠀⠀⠈⠳⣈⠻⣿⣿⣿⡇⠘⡄⢸⠀⠀⣇⠀⣻⣿⣿⣿⣿⣿⡏⠀⠸⡇⠀⠀⠀⠀⠀⠀\n",
          "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⢶⣤⣄⡑⠄⠀⠀⠈⠑⠢⠙⠻⢷⣶⣵⣞⣑⣒⣋⣉⣁⣻⣿⠿⠟⠱⠃⡸⠀⣧⠀⠀⠀⠀⠀⠀\n",
          "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⣷⣄⡀⠐⠢⣄⣀⡀⠀⠉⠉⠉⠉⠛⠙⠭⠭⠄⠒⠈⠀⠐⠁⢀⣿⠀⠀⠀⠀⠀⠀\n",
          "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠷⢦⣤⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣒⡠⠄⣠⡾⠃⠀⠀⠀⠀⠀⠀\n",
          "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠷⠶⣦⣤⣭⣤⣬⣭⣭⣴⠶⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀\n"
          )
    print("Trolled.")
    menu()


menu()
# This is the start of the program actually, to start the function it needs to be initialized before calling... stupid python.
