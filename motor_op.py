import pigpio
from motor_test import motor, servo
from motor_test import set_motor_pulse, set_servo_duty, angle_servo


def set_start():
    pi.set_servo_pulsewidth(motor.p1, motor.min)
    pi.set_servo_pulsewidth(motor.p2, motor.min)
    pi.set_servo_pulsewidth(motor.p3, motor.min)


def set_all_wheels(right, left, mid, indicator):
    if indicator == "go":

        set_motor_pulse(motor.p1, right)
        set_motor_pulse(motor.p2, left)
        set_motor_pulse(motor.p3, mid)
    elif indicator == "stop":
        set_start()


def set_cont_servo(indicator):
    if indicator == "go":
        set_servo_duty(servo.p1, servo.cmax)
    elif indicator == "stop":
        set_servo_duty(servo.p1, servo.cmid)


def set_horiz_servo():
    print("Enter horizontal deflector angle values from -20 to 20.")

    while True:
        try:
            servo_inp = angle_servo(-20, 20)
            set_servo_duty(servo.p2, servo_inp)
            break

        except ValueError:
            print("Invalid type input.")


def set_vert_servo():
    print("Enter horizontal deflector angle values from 0 to 30.")

    while True:
        try:
            servo_inp = angle_servo(0, 30)
            set_servo_duty(servo.p3, servo_inp)
            break

        except ValueError:
            print("Invalid type input.")

