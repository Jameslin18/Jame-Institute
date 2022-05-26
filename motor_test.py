import pigpio  # importing GPIO library
import os  # importing os library to communicate with the system
import time


os.system("sudo pigpiod")  # Launching GPIO library
time.sleep(1)  # As i said it is too impatient and so if this delay is removed you will get an error


class MotorInfo:
    p1 = 17  # right
    p2 = 27  # left
    p3 = 22  # mid

    max = 2000  # change this if your ESC's max value is different
    min = 1000  # change this if your ESC's min value is different
    init = 1100  # min speed to make motor move

    f = 16000
    d = 255


motor = MotorInfo()


class ServoInfo:
    p1 = 13  # continuous servo
    p2 = 19  # horizontal servo
    p3 = 12  # vertical servo

    r = 1000
    f = 50

    cmin = 25  # maxREV smart servo pulsewidth
    cmid = 75
    cmax = 125  # min REV smart servo pulsewidth

    hmin = 25
    hmid = 75
    hmax = 125

    vmin = 25
    vmid = 75
    vmax = 125


servo = ServoInfo()

pi = pigpio.pi()

pi.set_servo_pulsewidth(motor.p1, 0)
pi.set_servo_pulsewidth(motor.p2, 0)
pi.set_servo_pulsewidth(motor.p3, 0)

print("For first time launch, select [set].\n"
      "For motor initialization, select [start].\n"
      "For manual pulse inputs, select [man].\n"
      "For specific shot configuration, select [ball].\n"
      "For continuous servo control, select [cs].\n"
      "For horizontal deflector control, select [hs].\n"
      "For vertical deflector control, select [vs].\n"
      "For shutdown of all motors, select [stop].\n")


def test_menu():
    print("--------------------------------------------------")
    print("| set | start | man | ball | cs | hs | vs | stop |")
    print("--------------------------------------------------")

    inp = raw_input()
    if inp == "set":
        esc_settings()
    elif inp == "start":
        esc_startup()
    elif inp == "man":
        choose_single_mult()
    elif inp == "cs":
        cont_servo()
    elif inp == "hs":
        horiz_servo()
    elif inp == "vs":
        vert_servo()
    elif inp == "ball":
        ball_config()
    elif inp == "stop":
        stop()
    elif inp == "troll":
        troll()
    elif inp == "psychosis":
        deep_state()
    else:
        print("Invalid input.")
        test_menu()


def raw_input():
    inp = input("\nInput: ")
    return inp


def esc_startup():
    pi.set_servo_pulsewidth(motor.p1, motor.min)
    pi.set_servo_pulsewidth(motor.p2, motor.min)
    pi.set_servo_pulsewidth(motor.p3, motor.min)
    test_menu()


def set_motor_pulse(wheel, throttle):
    pi.set_PWM_frequency(wheel, motor.f)
    pi.set_PWM_dutycycle(wheel, motor.d)
    pi.set_servo_pulsewidth(wheel, throttle)


def set_servo_duty(serv, duty):
    pi.set_PWM_frequency(serv, servo.f)
    pi.set_PWM_range(serv, servo.r)
    pi.set_PWM_dutycycle(serv, duty)


def choose_wheel(func):
    while True:
        print("Choose which wheel for ", func, ".")
        print("[right] [left] [middle]")
        inp = raw_input()

        if inp == "right":
            wheel = motor.p1
            print("The right wheel is selected.")
            return wheel
        elif inp == "left":
            wheel = motor.p2
            print("The left wheel is selected.")
            return wheel
        elif inp == "middle":
            wheel = motor.p3
            print("The middle wheel is selected.")
            return wheel
        elif inp == "menu":
            test_menu()
            break
        else:
            print("Invalid input.")


def esc_settings():
    pin = choose_wheel("ESC setting")

    pi.set_servo_pulsewidth(pin, 0)
    print("You have selected esc setting.")
    print("Disconnect battery and press Enter.")
    inp = raw_input()
    if inp == '':
        pi.set_servo_pulsewidth(pin, motor.max)
        time.sleep(1)
        print("Connect the battery now, press Enter at the intended sequence.")
        inp = raw_input()

        if inp == '':
            pi.set_servo_pulsewidth(pin, motor.min)
            print("Press Enter again when different sequence runs.")
            inp = raw_input()

            if inp == '':
                pi.set_servo_pulsewidth(pin, motor.min)
                print("There should be two beeps as confirmation.")
                print("After this the ESC is set and you can disconnect battery.")
            else:
                print("Invalid input.")
                pi.set_servo_pulsewidth(pin, 0)
                test_menu()
        else:
            print("Invalid input.")
            pi.set_servo_pulsewidth(pin, 0)
            test_menu()
    else:
        print("Invalid input.")
        pi.set_servo_pulsewidth(pin, 0)
        test_menu()


def manual_drive():  # You will use this function to program your ESC if required
    print("\nYou have selected single manual option, enter number to set throttle.")
    print("Enter 'menu' to return.\n")
    pin = choose_wheel("manual control")

    while True:
        try:
            while True:
                str_inp = raw_input()
                throttle = int(str_inp)

                if throttle >= motor.max:
                    print("Maximum throttle is ", motor.max - 1, ".")
                    set_motor_pulse(pin, motor.max)
                elif 0 < throttle < motor.init:
                    print("Minimum throttle is ", motor.init, ".")
                    set_motor_pulse(pin, motor.init)

                elif throttle == 0:
                    pi.set_servo_pulsewidth(pin, motor.min)

                else:
                    set_motor_pulse(pin, throttle)
        except ValueError:
            if str_inp == "menu":
                test_menu()
                break
            else:
                print("Invalid input.")


def manual_drive_mult():
    print("\nYou have selected multiple manual option, enter numbers to set throttle.")
    print("Enter 'menu' to return.\n")

    while True:
        class WheelThrottles:
            def __init__(self):
                while True:
                    try:
                        print("Give right wheel throttle.")
                        int_inp1 = int(raw_input())

                        if int_inp1 >= motor.max:
                            print("Maximum right throttle is ", motor.max - 1, ".")
                            self.right = motor.max - 1
                        elif 0 < int_inp1 < motor.init:
                            print("Minimum right throttle is ", motor.init, ".")
                            self.right = motor.init
                        elif int_inp1 == 0:
                            self.right = motor.min
                        else:
                            self.right = int_inp1

                        print("Give left wheel throttle.")
                        int_inp2 = int(raw_input())
                        if int_inp2 >= motor.max:
                            print("Maximum left throttle is ", motor.max - 1, ".")
                            self.left = motor.max - 1
                        elif 0 < int_inp2 < motor.init:
                            print("Minimum left throttle is ", motor.init, ".")
                            self.left = motor.init
                        elif int_inp2 == 0:
                            self.left = motor.min
                        else:
                            self.left = int_inp2

                        print("Give middle wheel throttle.")
                        int_inp3 = int(raw_input())
                        if int_inp3 >= motor.max:
                            print("Maximum middle throttle is ", motor.max - 1, ".")
                            self.mid = motor.max - 1
                        elif 0 < int_inp3 < motor.init:
                            print("Minimum left throttle is ", motor.init, ".")
                            self.mid = motor.init
                        elif int_inp3 == 0:
                            self.mid = motor.min
                        else:
                            self.mid = int_inp3
                        break

                    except ValueError:
                        test_menu()

        throttle = WheelThrottles()

        set_motor_pulse(motor.p1, throttle.right)
        set_motor_pulse(motor.p2, throttle.left)
        set_motor_pulse(motor.p3, throttle.mid)


def choose_single_mult():
    while True:
        print("Choose single or multiple mode.")
        print("[s] [m]")
        inp = raw_input()

        if inp == "s":
            manual_drive()
            break
        elif inp == "m":
            manual_drive_mult()
            break
        else:
            print("Invalid input.")


def cont_servo():
    print("You have selected continuous servo control.")
    print("Enter menu to return.")
    print("\n[left] [right] [stop] [off]")

    while True:
        servo_inp = raw_input()

        if servo_inp == "left":
            set_servo_duty(servo.p1, servo.cmax)

        elif servo_inp == "right":
            set_servo_duty(servo.p1, servo.cmin)

        elif servo_inp == "stop":
            set_servo_duty(servo.p1, servo.cmid)

        elif servo_inp == "menu":
            test_menu()
            break

        else:
            print("Invalid input.")


def angle_servo(amin, amax):
    while True:
        ang = int(raw_input())

        if ang < amin:
            print("Minimum is ", amin, ".\n")
        elif ang > amax:
            print("Maximum is ", amax, ".\n")
        else:
            duty = float(ang + 135) * float(100 / 270) + 25
            print("Angle set at ", ang, "degrees.")
            break

    return duty


def horiz_servo():
    print("You have selected horizontal deflector control.")
    print("Enter menu to return.")
    print("Enter angle value from -20 to 20")

    while True:
        try:
            servo_inp = angle_servo(-20, 20)
            set_servo_duty(servo.p2, servo_inp)

        except ValueError:
            test_menu()


def vert_servo():
    print("You have selected vertical deflector control.")
    print("Enter menu to return.")
    print("Enter angle value from 0 to 30")

    while True:
        try:
            servo_inp = angle_servo(0, 30)
            set_servo_duty(servo.p3, servo_inp)

        except ValueError:
            test_menu()


def stop():  # This will stop every action your Pi is performing for ESC of course.
    pi.set_servo_pulsewidth(motor.p1, 0)
    pi.set_servo_pulsewidth(motor.p2, 0)
    pi.set_servo_pulsewidth(motor.p3, 0)
    pi.stop()


test_menu()
