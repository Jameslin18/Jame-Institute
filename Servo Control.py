import pigpio  # importing GPIO library
import os  # importing os library so as to communicate with the system
import time  # importing time library to make Rpi wait because its too impatient

os.system("sudo pigpiod")  # Launching GPIO library
time.sleep(1)

servo_1 = 5  # continuous servo GPIO pin

servo_duty_cycle = 255
servo_freq = 50

# max and min REV smart servo pulsewidth
min_servo = 500
max_servo = 2500


def raw_input():            # function that reads inputs
    inp = input("\nInput: ")
    return inp


def cont_servo():
    print("You have selected continuous servo control.")
    print("\n[left] [right] [stop] [exit]")

    while True:
        servo_inp = raw_input()

        if servo_inp == "left":
            pi.set_PWM_frequency(motor_1, servo_freq)
            pi.set_PWM_dutycycle(motor_1, servo_duty_cycle)
            pi.set_servo_pulsewidth(servo_1, max_servo)

        elif servo_inp == "right":
            pi.set_PWM_frequency(motor_1, servo_freq)
            pi.set_PWM_dutycycle(motor_1, servo_duty_cycle)
            pi.set_servo_pulsewidth(servo_1, min_servo)

        elif servo_inp == "stop":
            pi.set_PWM_frequency(motor_1, servo_freq)
            pi.set_PWM_dutycycle(motor_1, servo_duty_cycle)
            pi.set_servo_pulsewidth(servo_1, 1500)

        elif servo_inp == "exit":
            break

        else:
            print("Invalid input.\n")

cont_servo()
