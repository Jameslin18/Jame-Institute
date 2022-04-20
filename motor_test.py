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
    print("----------------------------------------")
    print("| set | start | man | cs | send | stop |")
    print("----------------------------------------")

    inp = raw_input()
    if inp == "set":
        esc_settings()
    elif inp == "start":
        esc_startup()
    elif inp == "man":
        manual_drive()
    elif inp == "cs":
        cont_servo()
    elif inp == "send":
        send()
    elif inp == "stop":
        stop()
    elif inp == "troll":
        troll()
    else:
        print("cringe.")
        menu()


def raw_input():
    inp = input("\nInput: ")
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
    print("\nYou have selected manual option, enter number to set throttle.")
    print("Enter 'menu' to return.")

    while True:
        try:
            while True:
                str_inp = raw_input()
                throttle = int(str_inp)

                if throttle >= max_value:
                    print("Maximum throttle is ", max_value - 1, ".")
                    pi.set_PWM_frequency(motor_1, motor_freq)
                    pi.set_PWM_dutycycle(motor_1, motor_duty_cycle)
                    pi.set_servo_pulsewidth(motor_1, max_value)

                elif 0 < throttle < 1100:
                    print("Minimum throttle is 1100.")
                    pi.set_PWM_frequency(motor_1, motor_freq)
                    pi.set_PWM_dutycycle(motor_1, motor_duty_cycle)
                    pi.set_servo_pulsewidth(motor_1, 1100)

                elif throttle == 0:
                    pi.set_servo_pulsewidth(motor_1, min_value)

                else:
                    pi.set_PWM_frequency(motor_1, motor_freq)
                    pi.set_PWM_dutycycle(motor_1, motor_duty_cycle)
                    pi.set_servo_pulsewidth(motor_1, throttle)
        except ValueError:
            if str_inp == "menu":
                menu()
                break
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


def stop():  # This will stop every action your Pi is performing for ESC of course.
    pi.set_servo_pulsewidth(motor_1, 0)
    pi.stop()


def troll():
    print("\n",
          "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&######BBBBGGGGGGGGBBBBBBB##&@@&&&&&&@@@@@@@@@@@@@@@@@@\n",
          "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&B5Y55YYJJ?7~^^^::^7?????7?777!!!~~^   .^!!~^~7J?!~:^~?G&@@@@@@@@@@@@@@\n",
          "@@@@@@@@@@@@@@@@@@@&BPY?!~^~!!77?JYYJJYYYJJJJJJJ???????????77!~^:.   ..:~77~:.^!7:   ^J#@@@@@@@@@@@@\n",
          "@@@@@@@@@@@@@@@&GJ~^   .~7JPB#BG5JJ?7!~^:...             . :::^~!777?YJ?!^:~7?~. .     .J&@@@@@@@@@@\n",
          "@@@@@@@@@@@@@G?: :?J~?YYJPGY!^.         :!7!!7^.^~~^. ~!!7??~7YYYJJ7???JJJY?~:~?7        ^G@@@@@@@@@\n",
          "@@@@@@@@@@&5^  ~YGP5J~.^Y7~JG#BG5?^     :~^^::7!~: ^!!^~?7!5&@@@@@@@@#5~~~.^:~: ^.     !!:.Y@@&@@@@@\n",
          "@@@@@@@&@#^  ^5J7J?.   .~Y&@@@@@@@@Y   ^7!!~Y7^77J?:  ^7.7&@@@@@@@@@@@@&7:~:..^:       !YPP5#@@&@@@@\n",
          "@@@@@@@&@B  7G7J??5P:^5#@@@@@@@@@@@@P. ~7!  ^BY.J?7?.   Y@@@@@@@@@@@@@@@@J ....:.    ::.  .~?G@@&@@@\n",
          "@@@@@@@@@J ^G: :7?Y#&@@@@@@@@@@@@@@@@G^Y775PBY:!5~YG^  ?@@@@@@@@@@@@@@@@@@?  .::.... ::^^^^.  7@@&@@\n",
          "@@@@@@@@B7J5J..J?:^~7P&@@@@@@@@@@@@@#Y^~?@G7. .G5P!!7.:&@@@@@@@@@@@@@@@@@@@7~!?PPJJY!^^^^^::   !&@@@\n",
          "@@@@@@&Y!GGJY5GP77?!!~75B&&#&&@@@&B?. .!#&.   .!P5~7: ^#@@@@@@@@@@@@@@@@@@BGG&G?J:.JJJJJJPG5Y7: :5&@\n",
          "&@@&J~~.BP^YGJ~!^7J7~^^::^^~~7???~.   .~@P      :. ..   !G&@@@@@@@@@@@@@&5:  ^?~   :^!?YP&#YJYBP^ ~#\n",
          "@@Y. 7:P#.^@@@#Y!:^!7!~:.!77!!!!!JPB#G5#@7        ^Y55YJ!~!?5G#&&&&#BGBP~.      :YB&@@@@@&BJPJ.?#5.:\n",
          "@P  ?7:@J  B@@@@@&GJ!~!!^.     !GG5?JYG#5.          .:^5@5YPY^ .::..~7~  .~~. .J&@@@@@@@#^5~ GY.:G#:\n",
          "@P :G .#B. J@@@@@@@@@#PY?7!~~^!B?. ?@P!:     YGP5J7~.  !@~ .JBY~    .  :~~. ^?#@@@@@@@@B:^G. .#?~ 5#\n",
          "@P ^G  ^BB^^@@@@@@@@@@@@@&B5J7!^   ?@7   .. .?JJ5GB&#: ~@!   .~!..:^!?J?77YB@@@@@@@@@@P. P!   JP~~ Y\n",
          "@G :G^:  J&?B@@@@@@@@@@@@@@@@@&&#G55&@#BBBGGP5J7   :!..:?.    ~J5B&@&&&@@@@@@@@@@@@@&?  JY    ^#:?  \n",
          "@@!.G^5 ..^~B@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&#&&@&5YY5PGG5Y5PPGB&@@@@@@@@@@@@@@@@@@@@5:  ?5     .#^7: \n",
          "&@@J~ Y!:B. B@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#!   ?5  ..  ^#.!^ \n",
          "@&@@7 ^P GY G@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@5. . ^7  !!.  P? ?: \n",
          "@@&@@J G^!# Y@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#!  7^   ~J~  ^57 .?  \n",
          "@@@&@@!Y7:&^7@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@5.  Y!  ~J!.  ~?:  7~:7\n",
          "@@@@&@GY?.&~~@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#7   JJ  .~.        .^.J@\n",
          "@@@@&@&P? #7^@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@5^.  JY   ^.   :!     ~G@@\n",
          "@@@@@@@B? BY^@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&577?:.YJ   ~?    :5    !@@@@\n",
          "@@@@@@@#! PP~@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@BJ7JY~ ^P7   :Y.    Y!   ^&@&@@\n",
          "@@@@&@@&: J#G@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&P7!5Y~  ?5^    Y^   .57   !&@&@@@\n",
          "@@@@&@@P  !@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&J:~P5^  ~57     J!   ~5~  :Y@@&@@@@\n",
          "@@@@&@&^  !@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#J:~PP~  ^YJ:.~  .J~   ?Y. :J#@@@@@@@@\n",
          "@@@@&@P   ~@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#?.~PG!  :JJ: ~!. ~Y^  ^Y7 ^5&@@@@@@@@@@\n",
          "@@@@@@J : ^@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#?.~GG!  .!?: ~?^ .??. .7Y~!G@@@@@@@@@@@@@\n",
          "@@@@@@!?&:.#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@G7.:5#7    ~^ :?!  ~?^  7GGP#@@@@@@@@@@@@@@@\n",
          "@@@@@&:?@: 5@B@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#Y^.!PGJ. .^!7!^7?: :~~.^JB@@@@@@@@@@@@@@@@@@@@\n",
          "@@@&@# ~@! ~&Y?G&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@BY7~75G5!.:!??7^.~?^  :~!Y#@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@&@G  5#^ ^5^:^!J5B&@@@@@@@@@@@@@@@@@@@@@@@&GY7!?5PG5J777?7~.  ^J?!?5G#&@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@P   ?#?:  ^7?!^^^!7J5G##B##BBGGGP5Y?7!^:.   .~::7Y5~.    .!G&##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@B:   ^J55Y~ .^~77?JJ?77^ ... ... .:^~~~!~^:^^!J5J~.  .^?P#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@@&! .:   .!^.     :^~~~^~~!7?JJ77!~^. ^7?JJJJ7~.  ^?P#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@@@@J~?JJ?!~7??77777!^     .::..         :^!7?J55PB@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@@@@@&GY?77??J??7!~~^^^^^^^^     .^!?YPB#&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@@@@@@@@@&BPYJJ??JJJJJJJJJ???Y5GB&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@@@@@@@@@@@@@@@@@&&&&&&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",
          "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
          )
    print("\nTrolled.")
    menu()


menu()
