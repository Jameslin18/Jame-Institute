import math
import time
from sympy import Eq, symbols, solve, Symbol


def menu():
    print("-------------------------------------")
    print("| ang | power | base | pulse |")
    print("-------------------------------------\n")
    while True:
        inp = raw_input()
        if inp == "ang":
            angle_calc()
            break
        elif inp == "power":
            power_set()
            break
        elif inp == "base":
            choose_base_wheel()
            break
        elif inp == "pulse":
            calc_pulse()
            break
        elif inp == "troll":
            troll()
            break
        elif inp == "psychosis":
            deep_state()
        else:
            print("cringe.")


def raw_input():
    inp = input("Input: ")
    return inp


def angle_inp():
    print("Give angle of rotation.")
    deg = int(raw_input())
    theta = float(deg * math.pi/180)
    return theta


def pulse_power(inp):
    pulse = inp
    power = float(100 * float(pulse / 2000))
    return power


def ang_pulse(inp):
    angular = inp
    volt = float(angular / (60 * math.pi))
    pulse = float(float(2000 / 9) * volt)
    return pulse


def power_set():
    print("Give power value from 0 - 100.")
    while True:
        try:
            power = int(raw_input())
            if power > 100:
                power = 100
                print("Max value is 100.")
                break
            elif power < 0:
                power = 0
                print("Min value is 0.")
                break
            else:
                break
        except ValueError:
            print("cringe.")

    pulse = float(1200 + 800 * float(power/100))
    print("Power set to ", power, ".")

    return pulse


def spin_set(max_n):
    print("Give spin value from 0 - 100.")
    while True:
        try:
            power = int(raw_input())
            if power > 100:
                power = 100
                print("Max value is 100.")
                break
            elif power < 0:
                power = 0
                print("Min value is 0.")
                break
            else:
                break
        except ValueError:
            print("cringe.")

    pulse = float(2000 * float(float(max_n/100) * float(power/100)))
    print("Spin set to ", pulse, ".")

    return pulse


def choose_base_wheel():
    theta = angle_inp()
    while True:
        if 0 < float(theta) < 2 * math.pi / 3:
            base = "left"
            print("Base wheel(s) = ", base)
            return theta, base
        elif 4 * math.pi / 3 < float(theta) < 2 * math.pi:
            base = "right"
            print("Base wheel(s) = ", base)
            return theta, base
        elif 2 * math.pi / 3 < float(theta) < 4 * math.pi / 3:
            base = "mid"
            print("Base wheel(s) = ", base)
            return theta, base
        elif float(theta) == 0 and 2 * math.pi:
            base = "left+right"
            print("Base wheel(s) = ", base)
            return theta, base
        elif float(theta) == 2 * math.pi / 3:
            base = "left+mid"
            print("Base wheel(s) = ", base)
            return theta, base
        elif float(theta) == 4 * math.pi / 3:
            base = "right+mid"
            print("Base wheel(s) = ", base)
            return theta, base
        elif float(theta) > 2 * math.pi:
            print("Cannot go over 360 degrees.")
            break


def max_net(base, ang):
    if base == "right":
        wr = ang
        wl = 2000
        wm = 2000

        wn = Symbol("wn", positive=True)

        eq1 = Eq(wr**2 + wl**2 + wm**2 - wr*wl - wl*wm - wr*wm - wn**2, 0)

        sol = solve(eq1, wn, dict=True)
        max_n = sol[0][wn]

        out = pulse_power(max_n)
        return out

    elif base == "left":
        wr = 2000
        wl = ang
        wm = 2000

        wn = Symbol("wn", nonnegative=True)

        eq1 = Eq(wr**2 + wl**2 + wm**2 - wr*wl - wl*wm - wr*wm - wn**2, 0)

        sol = solve(eq1, wn, dict=True)
        max_n = sol[0][wn]

        print(ang)
        print(max_n)
        out = pulse_power(max_n)
        print(out)
        return out

    elif base == "mid":
        wr = 2000
        wl = 2000
        wm = ang

        wn = Symbol("wn", positive=True)

        eq1 = Eq(wr ** 2 + wl ** 2 + wm ** 2 - wr * wl - wl * wm - wr * wm - wn ** 2, 0)

        sol = solve(eq1, wn, dict=True)
        max_n = sol[0][wn]

        out = pulse_power(max_n)
        return out

    elif base == "left+right":
        wr = ang
        wl = wr
        wm = 2000

        wn = Symbol("wn", positive=True)

        eq1 = Eq(wr ** 2 + wl ** 2 + wm ** 2 - wr * wl - wl * wm - wr * wm - wn ** 2, 0)

        sol = solve(eq1, wn, dict=True)
        max_n = sol[0][wn]

        out = pulse_power(max_n)
        return out

    elif base == "left+mid":
        wr = 2000
        wl = ang
        wm = wl

        wn = Symbol("wn", positive=True)

        eq1 = Eq(wr ** 2 + wl ** 2 + wm ** 2 - wr * wl - wl * wm - wr * wm - wn ** 2, 0)

        sol = solve(eq1, wn, dict=True)
        max_n = sol[0][wn]

        out = pulse_power(max_n)
        return out

    elif base == "right+mid":
        wr = ang
        wl = 2000
        wm = wr

        wn = Symbol("wn", positive=True)

        eq1 = Eq(wr ** 2 + wl ** 2 + wm ** 2 - wr * wl - wl * wm - wr * wm - wn ** 2, 0)

        sol = solve(eq1, wn, dict=True)
        max_n = sol[0][wn]

        out = pulse_power(max_n)
        return out


def calc_pulse():
    theta, base = choose_base_wheel()
    if theta == math.pi/2 or 3*math.pi/2:
        k = float(math.tan(theta+0.01))
    else:
        k = float(math.tan(theta))

    if base == "left":
        wl = power_set()
        wn = spin_set(max_net(base, wl))

        wr, wm = symbols('wr wm', real=True)

        eq1 = Eq(2*k*wm - k*wr - math.sqrt(3)*wr - k*wl + math.sqrt(3)*wl, 0)
        eq2 = Eq(wr**2 + wl**2 + wm**2 - wr*wl - wl*wm - wr*wm - wn**2, 0)

        sol = solve([eq1, eq2], [wr, wm], dict=True)

        left = wl
        try:
            right = sol[1][wr]
            middle = sol[1][wm]
        except IndexError:
            right = sol[0][wr]
            middle = sol[0][wm]

        print("right = ", right)
        print("left = ", left)
        print("middle = ", middle)

        # menu()
        return right, left, middle

    elif base == "right":
        wr = power_set()
        wn = spin_set(max_net(base, wr))

        wl, wm = symbols('wl wm', real=True)

        eq1 = Eq(2 * k * wm - k * wr - math.sqrt(3) * wr - k * wl + math.sqrt(3) * wl, 0)
        eq2 = Eq(wr ** 2 + wl ** 2 + wm ** 2 - wr * wl - wl * wm - wr * wm - wn ** 2, 0)

        sol = solve([eq1, eq2], dict=True)

        right = wr
        try:
            left = sol[1][wl]
            middle = sol[1][wm]
        except IndexError:
            left = sol[0][wl]
            middle = sol[0][wm]

        print("right = ", right)
        print("left = ", left)
        print("middle = ", middle)

        # menu()
        return right, left, middle

    elif base == "mid":
        wm = power_set()
        wn = spin_set(max_net(base, wm))

        wr, wl = symbols('wr wl', real=True)

        eq1 = Eq(2 * k * wm - k * wr - math.sqrt(3) * wr - k * wl + math.sqrt(3) * wl, 0)
        eq2 = Eq(wr ** 2 + wl ** 2 + wm ** 2 - wr * wl - wl * wm - wr * wm - wn ** 2, 0)

        sol = solve([eq1, eq2], dict=True)

        middle = wm
        try:
            right = sol[1][wr]
            left = sol[1][wl]
        except IndexError:
            right = sol[0][wr]
            left = sol[0][wl]

        print("right = ", right)
        print("left = ", left)
        print("middle = ", middle)

        # menu()
        return right, left, middle

    elif base == "left+right":
        wr = wl = power_set()
        wn = max_net(base, wr)

        wm = Symbol('wm', real=True)

        eq1 = Eq(2 * k * wm - k * wr - math.sqrt(3) * wr - k * wl + math.sqrt(3) * wl, 0)
        eq2 = Eq(wr ** 2 + wl ** 2 + wm ** 2 - wr * wl - wl * wm - wr * wm - wn ** 2, 0)

        sol = solve([eq1, eq2], dict=True)

        right = left = wl
        try:
            middle = sol[1][wm]
        except IndexError:
            middle = sol[0][wm]

        print("right = ", right)
        print("left = ", left)
        print("middle = ", middle)

        # menu()
        return right, left, middle

    elif base == "left+mid":
        wl = wm = power_set()
        wn = max_net(base, wl)

        wr = Symbol('wr', real=True)

        eq1 = Eq(2 * k * wm - k * wr - math.sqrt(3) * wr - k * wl + math.sqrt(3) * wl, 0)
        eq2 = Eq(wr ** 2 + wl ** 2 + wm ** 2 - wr * wl - wl * wm - wr * wm - wn ** 2, 0)

        sol = solve([eq1, eq2], dict=True)

        middle = left = wl
        try:
            right = sol[1][wr]
        except IndexError:
            right = sol[0][wr]

        print("right = ", right)
        print("left = ", left)
        print("middle = ", middle)

        # menu()
        return right, left, middle

    elif base == "right+mid":
        wr = wm = power_set()
        wn = max_net(base, wr)

        wl = Symbol('wl', real=True)

        eq1 = Eq(2 * k * wm - k * wr - math.sqrt(3) * wr - k * wl + math.sqrt(3) * wl, 0)
        eq2 = Eq(wr ** 2 + wl ** 2 + wm ** 2 - wr * wl - wl * wm - wr * wm - wn ** 2, 0)

        sol = solve([eq1, eq2], dict=True)

        right = middle = wr
        try:
            left = sol[1][wl]
        except IndexError:
            left = sol[0][wl]

        print("right = ", right)
        print("left = ", left)
        print("middle = ", middle)

        # menu()
        return right, left, middle


def pulse_angular(inp):
    pulse = int(inp)
    volt = float(float(9 / 2000) * pulse)
    wh_angular = float(volt * 60 * math.pi)
    # ball_angular = wh_angular * float(101.6 / 40)
    return wh_angular


def angle_calc():
    while True:
        class WheelAngular(object):
            def __init__(self):
                while True:
                    try:
                        print("Give left wheel pulsewidth.")
                        self.left = pulse_angular(raw_input())

                        print("Give right wheel pulsewidth.")
                        self.right = pulse_angular(raw_input())

                        print("Give mid wheel pulsewidth.")
                        self.mid = pulse_angular(raw_input())

                        break
                    except ValueError:
                        print("cringe.")

        wheel = WheelAngular()

        class LeftAngular:
            i = wheel.left * math.cos(4 * math.pi / 3)  # left.i * -1/2
            j = wheel.left * math.sin(4 * math.pi / 3)  # left.j * -sqrt3/2

        l_vector = LeftAngular()

        class RightAngular:
            i = wheel.right * math.cos(2 * math.pi / 3)  # right.i * -1/2
            j = wheel.right * math.sin(2 * math.pi / 3)  # right.i * sqrt3/2

        r_vector = RightAngular()

        class MidAngular:
            i = wheel.mid * math.cos(0)  # mid.i * 1
            j = wheel.mid * math.sin(0)  # mid.i * 0

        m_vector = MidAngular()

        class NetAngular:
            i = int(l_vector.i + r_vector.i + m_vector.i)  # mid.i -1/2(left.i) - 1/2(right.i)
            j = int(l_vector.j + r_vector.j + m_vector.j)  # sqrt3/2(right.j) - sqrt3/2(left.i)

        n_vector = NetAngular()

        if n_vector.i == n_vector.j == 0:
            print("\nNo spin.")
        else:
            theta = math.atan2(n_vector.j, n_vector.i)
            deg = int((theta * float(180 / math.pi)))
            if deg < 0:
                print("\nAngle = ", 360 + deg, "degrees")
            else:
                print("\nAngle = ", deg, "degrees")

        print("\nData:")
        print("------------------")
        print("i net = ", n_vector.i)
        print("j net = ", n_vector.j)
        print("------------------")
        print("i left = ", l_vector.i)
        print("i right = ", r_vector.i)
        print("i mid = ", m_vector.i)
        print("------------------")
        print("j left = ", l_vector.j)
        print("j right = ", r_vector.j)
        print("j mid = ", m_vector.j)
        print("------------------")
        print("wheel left = ", wheel.left)
        print("wheel right = ", wheel.right)
        print("wheel mid = ", wheel.mid)
        print("------------------")
        print("\n")

        print("[stop] [menu] Enter")
        inp = raw_input()
        if inp == "stop":
            break
        elif inp == "menu":
            menu()
            break
        elif inp == '':
            angle_calc()


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
