import pigpio  # importing GPIO library
import os  # importing os library to communicate with the system
import time
from calc import calc_pulse


os.system("sudo pigpiod")  # Launching GPIO library
time.sleep(1)  # As i said it is too impatient and so if this delay is removed you will get an error


class MotorInfo:
    p1 = 17  # right
    p2 = 27  # left
    p3 = 22  # mid

    max = 2000  # change this if your ESC's max value is different
    min = 1000  # change this if your ESC's min value is different
    init = 1200  # min speed to make motor move

    f = 16000
    d = 255


motor = MotorInfo()


class ServoInfo:
    p1 = 13  # continuous servo
    p2 = 6  #
    p3 = 13  #

    r = 1000
    f = 50

    cmin = 25  # maxREV smart servo pulsewidth
    cmid = 75
    cmax = 125  # min REV smart servo pulsewidth


servo = ServoInfo()

pi = pigpio.pi()

pi.set_servo_pulsewidth(motor.p1, 0)
pi.set_servo_pulsewidth(motor.p2, 0)
pi.set_servo_pulsewidth(motor.p3, 0)

print("For first time launch, select [set]."
      "For motor initialization, select [start]."
      "For manual pulse inputs, select [man]."
      "For specific shot configuration, select [ball]."
      "For continuous servo control, select [cs]."
      "For shutdown of all motors, select [stop].")


def menu():
    print("----------------------------------------")
    print("| set | start | man | ball | cs | stop |")
    print("----------------------------------------")

    inp = raw_input()
    if inp == "set":
        esc_settings()
    elif inp == "start":
        esc_startup()
    elif inp == "man":
        choose_single_mult()
    elif inp == "cs":
        cont_servo()
    elif inp == "ball":
        ball_config()
    elif inp == "stop":
        stop()
    elif inp == "troll":
        troll()
    elif inp == "psychosis":
        deep_state()
    else:
        print("cringe.")
        menu()


def raw_input():
    inp = input("\nInput: ")
    return inp


def esc_startup():
    pi.set_servo_pulsewidth(motor.p1, motor.min)
    pi.set_servo_pulsewidth(motor.p2, motor.min)
    pi.set_servo_pulsewidth(motor.p3, motor.min)
    menu()


def set_motor_pulse(wheel, throttle):
    pi.set_PWM_frequency(wheel, motor.f)
    pi.set_PWM_dutycycle(wheel, motor.d)
    pi.set_servo_pulsewidth(wheel, throttle)


def set_servo_duty(serv, duty):
    pi.set_PWM_frequency(serv, servo.f)
    pi.set_PWM_range(serv, servo.r)
    pi.set_PWM_dutycycle(serv, duty)


def ball_config():
    right, left, mid = calc_pulse()

    set_motor_pulse(motor.p1, right)
    set_motor_pulse(motor.p2, left)
    set_motor_pulse(motor.p3, mid)

    menu()


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
            menu()
            break
        else:
            print("cringe.")


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
                print("bruh.")
                pi.set_servo_pulsewidth(pin, 0)
                menu()
        else:
            print("bruh.")
            pi.set_servo_pulsewidth(pin, 0)
            menu()
    else:
        print("bruh.")
        pi.set_servo_pulsewidth(pin, 0)
        menu()


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
                menu()
                break
            else:
                print("cringe.")


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
                        if self.right or self.left or self.mid == "menu":
                            menu()
                            break
                        else:
                            print("cringe.")

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
            print("cringe.")


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
            menu()
            break

        else:
            print("cringe.")


def stop():  # This will stop every action your Pi is performing for ESC of course.
    pi.set_servo_pulsewidth(motor.p1, 0)
    pi.set_servo_pulsewidth(motor.p2, 0)
    pi.set_servo_pulsewidth(motor.p3, 0)
    pi.stop()


def troll():
    print("\n",
          "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&######BBBBGGGGGGGGBBBBBBB##&@@&&&&&&@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&B5Y55YYJJ?7~^^^::^7?????7?777!!!~~^   .^!!~^~7J?!~:^~?G&@@@@@@@@@@@@@@@@\n",
          "@@@@@@@@@@@@@@@@@@@&BPY?!~^~!!77?JYYJJYYYJJJJJJJ???????????77!~^:.   ..:~77~:.^!7:   ^J#@@@@@@@@@@@@@@\n",
          "@@@@@@@@@@@@@@@&GJ~^   .~7JPB#BG5JJ?7!~^:...             . :::^~!777?YJ?!^:~7?~. .     .J&@@@@@@@@@@@@\n",
          "@@@@@@@@@@@@@G?: :?J~?YYJPGY!^.         :!7!!7^.^~~^. ~!!7??~7YYYJJ7???JJJY?~:~?7        ^G@@@@@@@@@@@\n",
          "@@@@@@@@@@&5^  ~YGP5J~.^Y7~JG#BG5?^     :~^^::7!~: ^!!^~?7!5&@@@@@@@@#5~~~.^:~: ^.     !!:.Y@@&@@@@@@@\n",
          "@@@@@@@&@#^  ^5J7J?.   .~Y&@@@@@@@@Y   ^7!!~Y7^77J?:  ^7.7&@@@@@@@@@@@@&7:~:..^:       !YPP5#@@&@@@@@@\n",
          "@@@@@@@&@B  7G7J??5P:^5#@@@@@@@@@@@@P. ~7!  ^BY.J?7?.   Y@@@@@@@@@@@@@@@@J ....:.    ::.  .~?G@@&@@@@@\n",
          "@@@@@@@@@J ^G: :7?Y#&@@@@@@@@@@@@@@@@G^Y775PBY:!5~YG^  ?@@@@@@@@@@@@@@@@@@?  .::.... ::^^^^.  7@@&@@@@\n",
          "@@@@@@@@B7J5J..J?:^~7P&@@@@@@@@@@@@@#Y^~?@G7. .G5P!!7.:&@@@@@@@@@@@@@@@@@@@7~!?PPJJY!^^^^^::   !&@@@@@\n",
          "@@@@@@&Y!GGJY5GP77?!!~75B&&#&&@@@&B?. .!#&.   .!P5~7: ^#@@@@@@@@@@@@@@@@@@BGG&G?J:.JJJJJJPG5Y7: :5&@@@\n",
          "&@@&J~~.BP^YGJ~!^7J7~^^::^^~~7???~.   .~@P      :. ..   !G&@@@@@@@@@@@@@&5:  ^?~   :^!?YP&#YJYBP^ ~#@@\n",
          "@@Y. 7:P#.^@@@#Y!:^!7!~:.!77!!!!!JPB#G5#@7        ^Y55YJ!~!?5G#&&&&#BGBP~.      :YB&@@@@@&BJPJ.?#5.:@@\n",
          "@P  ?7:@J  B@@@@@&GJ!~!!^.     !GG5?JYG#5.          .:^5@5YPY^ .::..~7~  .~~. .J&@@@@@@@#^5~ GY.:G#:@@\n",
          "@P :G .#B. J@@@@@@@@@#PY?7!~~^!B?. ?@P!:     YGP5J7~.  !@~ .JBY~    .  :~~. ^?#@@@@@@@@B:^G. .#?~ 5#@@\n",
          "@P ^G  ^BB^^@@@@@@@@@@@@@&B5J7!^   ?@7   .. .?JJ5GB&#: ~@!   .~!..:^!?J?77YB@@@@@@@@@@P. P!   JP~~ Y@@\n",
          "@G :G^:  J&?B@@@@@@@@@@@@@@@@@&&#G55&@#BBBGGP5J7   :!..:?.    ~J5B&@&&&@@@@@@@@@@@@@&?  JY    ^#:?  @@\n",
          "@@!.G^5 ..^~B@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&#&&@&5YY5PGG5Y5PPGB&@@@@@@@@@@@@@@@@@@@@5:  ?5     .#^7: @@\n",
          "&@@J~ Y!:B. B@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#!   ?5  ..  ^#.!^ @@\n",
          "@&@@7 ^P GY G@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@5. . ^7  !!.  P? ?: @@\n",
          "@@&@@J G^!# Y@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#!  7^   ~J~  ^57 .?  @@\n",
          "@@@&@@!Y7:&^7@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@5.  Y!  ~J!.  ~?:  7~:7@@\n",
          "@@@@&@GY?.&~~@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#7   JJ  .~.        .^.J@@@\n",
          "@@@@&@&P? #7^@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@5^.  JY   ^.   :!     ~G@@@@\n",
          "@@@@@@@B? BY^@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&577?:.YJ   ~?    :5    !@@@@@@\n",
          "@@@@@@@#! PP~@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@BJ7JY~ ^P7   :Y.    Y!   ^&@&@@@@\n",
          "@@@@&@@&: J#G@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&P7!5Y~  ?5^    Y^   .57   !&@&@@@@@\n",
          "@@@@&@@P  !@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&J:~P5^  ~57     J!   ~5~  :Y@@&@@@@@@\n",
          "@@@@&@&^  !@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#J:~PP~  ^YJ:.~  .J~   ?Y. :J#@@@@@@@@@@\n",
          "@@@@&@P   ~@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#?.~PG!  :JJ: ~!. ~Y^  ^Y7 ^5&@@@@@@@@@@@@\n",
          "@@@@@@J : ^@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#?.~GG!  .!?: ~?^ .??. .7Y~!G@@@@@@@@@@@@@@@\n",
          "@@@@@@!?&:.#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@G7.:5#7    ~^ :?!  ~?^  7GGP#@@@@@@@@@@@@@@@@@\n",
          "@@@@@&:?@: 5@B@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#Y^.!PGJ. .^!7!^7?: :~~.^JB@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@&@# ~@! ~&Y?G&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@BY7~75G5!.:!??7^.~?^  :~!Y#@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@&@G  5#^ ^5^:^!J5B&@@@@@@@@@@@@@@@@@@@@@@@&GY7!?5PG5J777?7~.  ^J?!?5G#&@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@P   ?#?:  ^7?!^^^!7J5G##B##BBGGGP5Y?7!^:.   .~::7Y5~.    .!G&##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@B:   ^J55Y~ .^~77?JJ?77^ ... ... .:^~~~!~^:^^!J5J~.  .^?P#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@@&! .:   .!^.     :^~~~^~~!7?JJ77!~^. ^7?JJJJ7~.  ^?P#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@@@@J~?JJ?!~7??77777!^     .::..         :^!7?J55PB@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@@@@@&GY?77??J??7!~~^^^^^^^^     .^!?YPB#&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@@@@@@@@@&BPYJJ??JJJJJJJJJ???Y5GB&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@@@@@@@@@@@@@@@@@&&&&&&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
          )
    print("\nTrolled.")
    menu()


def deep_state():
    while True:
        print("KILL JOHN LENNON !\n")
        time.sleep(1)


menu()
