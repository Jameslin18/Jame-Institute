import time
import pigpio
import os
from motor_test import esc_settings, stop, raw_input
from motor_op import set_start, set_all_wheels, set_cont_servo, set_horiz_servo, set_vert_servo
from comp_calc import comp_calc_pulse
from calc import angle_calc

os.system("sudo pigpiod")
time.sleep(1)


def menu():
    print("------------------------------------------")
    print("| start | config | set | test | sim | stop |")
    print("-----------------------------------------\n")

    inp = raw_input()

    if inp == "start":
        set_start()
    elif inp == "set":
        esc_settings()
    elif inp == "seq":
        ball_config()
    elif inp == "sim":
        angle_calc()
    elif inp == "stop":
        stop()
    else:
        print("Invalid input.")
        menu()


def ball_config():
    print("You are now able to configure the type of ball to practice with.\n")

    right, left, mid = comp_calc_pulse()
    throttles = right, left, mid

    set_horiz_servo()
    set_vert_servo()

    print("[go] [stop] [menu]\n")
    while True:
        inp = raw_input()
        if inp == "go":
            set_all_wheels(throttles, inp)
            set_cont_servo(inp)
        elif inp == "stop":
            set_all_wheels(throttles, inp)
            set_cont_servo(inp)
        elif inp == "menu":
            menu()
            break
        else:
            print("Invalid input.")


menu()
