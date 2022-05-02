import math
from sympy import Eq, symbols, solve, Symbol


def menu():
    print("--------------------------------")
    print("| ang | power | base | pulse |")
    print("--------------------------------\n")
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


def ang_power(inp):
    angular = inp
    volt = float(angular / (60 * math.pi))
    pulse = float(float(2000/9) * volt)
    power = int(100 * float(pulse / 2000))
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

    pulse = float(2000 * float(power/100))
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

    pulse = float(2000 * float(power * float(max_n/100)))
    print("Spin set to ", power, ".")

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


def max_net(base, ang):
    if base == "right":
        wr = ang
        wl = 0
        wm = pulse_angular(2000)

        wn = Symbol("wn", positive=True)

        eq = Eq(wr**2 + wl**2 + wm**2 - wr*wl - wl*wm - wr*wm - wn**2, 0)

        sol = solve(eq, wn, dict=True)
        max_n = sol[0][wn]

        out = ang_power(max_n)
        return out

    elif base == "left":
        wr = 0
        wl = ang
        wm = pulse_angular(2000)

        wn = Symbol("wn", positive=True)

        eq = Eq(wr**2 + wl**2 + wm**2 - wr*wl - wl*wm - wr*wm - wn**2, 0)

        sol = solve(eq, wn, dict=True)
        max_n = sol[0][wn]

        out = ang_power(max_n)
        return out

    elif base == "mid":
        wr = 0
        wl = pulse_angular(2000)
        wm = ang

        wn = Symbol("wn", positive=True)

        eq = Eq(wr**2 + wl**2 + wm**2 - wr*wl - wl*wm - wr*wm - wn**2, 0)

        sol = solve(eq, wn, dict=True)
        max_n = sol[0][wn]

        out = ang_power(max_n)
        return out

    elif base == "left+right":
        wr = ang
        wl = wr
        wm = pulse_angular(2000)

        wn = Symbol("wn", positive=True)

        eq = Eq(wr**2 + wl**2 + wm**2 - wr*wl - wl*wm - wr*wm - wn**2, 0)

        sol = solve(eq, wn, dict=True)
        max_n = sol[0][wn]

        out = ang_power(max_n)
        return out

    elif base == "left+mid":
        wr = pulse_angular(2000)
        wl = ang
        wm = wl

        wn = Symbol("wn", positive=True)

        eq = Eq(wr**2 + wl**2 + wm**2 - wr*wl - wl*wm - wr*wm - wn**2, 0)

        sol = solve(eq, wn, dict=True)
        max_n = sol[0][wn]

        out = ang_power(max_n)
        return out

    elif base == "right+mid":
        wr = ang
        wl = pulse_angular(2000)
        wm = wr

        wn = Symbol("wn", positive=True)

        eq = Eq(wr**2 + wl**2 + wm**2 - wr*wl - wl*wm - wr*wm - wn**2, 0)

        sol = solve(eq, wn, dict=True)
        max_n = sol[0][wn]

        out = ang_power(max_n)
        return out


def calc_pulse():
    theta, base = choose_base_wheel()
    if theta == math.pi/2 or 3*math.pi/2:
        k = float(math.tan(theta+0.01))
    else:
        k = float(math.tan(theta))

    if base == "left":
        wl = pulse_angular(power_set())
        wn = spin_set(max_net(base, wl))

        wr, wm = symbols('wr wm', positive=True)

        eq1 = Eq(2*k*wm - k*wr - math.sqrt(3)*wr - k*wl + math.sqrt(3)*wl, 0)
        eq2 = Eq(wr**2 + wl**2 + wm**2 - wr*wl - wl*wm - wr*wm - wn**2, 0)

        sol = solve([eq1, eq2], [wr, wm], dict=True)

        left = wl
        right = sol[0][wr]
        middle = sol[0][wm]

        print("left = ", left)
        print("right = ", right)
        print("middle = ", middle)

        menu()
        return left, right, middle

    elif base == "right":
        wr = pulse_angular(power_set())
        wn = spin_set(max_net(base, wr))

        wl, wm = symbols('wl wm', positive=True)

        eq1 = Eq(2 * k * wm - k * wr - math.sqrt(3) * wr - k * wl + math.sqrt(3) * wl, 0)
        eq2 = Eq(wr ** 2 + wl ** 2 + wm ** 2 - wr * wl - wl * wm - wr * wm - wn ** 2, 0)

        sol = solve([eq1, eq2], dict=True)

        right = wr
        left = sol[0][wl]
        middle = sol[0][wm]

        print("left = ", left)
        print("right = ", right)
        print("middle = ", middle)

        menu()
        return left, right, middle

    elif base == "mid":
        wm = pulse_angular(power_set())
        wn = spin_set(max_net(base, wm))

        wr, wl = symbols('wr wl', positive=True)

        eq1 = Eq(2 * k * wm - k * wr - math.sqrt(3) * wr - k * wl + math.sqrt(3) * wl, 0)
        eq2 = Eq(wr ** 2 + wl ** 2 + wm ** 2 - wr * wl - wl * wm - wr * wm - wn ** 2, 0)

        sol = solve([eq1, eq2], dict=True)

        middle = wm
        right = sol[0][wr]
        left = sol[0][wl]

        print("left = ", left)
        print("right = ", right)
        print("middle = ", middle)

        menu()
        return left, right, middle

    elif base == "left+right":
        wr = wl = pulse_angular(power_set())
        wn = spin_set(max_net(base, wr))

        wm = Symbol('wm', positive=True)

        eq1 = Eq(2 * k * wm - k * wr - math.sqrt(3) * wr - k * wl + math.sqrt(3) * wl, 0)
        eq2 = Eq(wr ** 2 + wl ** 2 + wm ** 2 - wr * wl - wl * wm - wr * wm - wn ** 2, 0)

        sol = solve([eq1, eq2], dict=True)

        right = left = wl
        middle = sol[0][wm]

        print("left = ", left)
        print("right = ", right)
        print("middle = ", middle)

        menu()
        return left, right, middle

    elif base == "left+mid":
        wl = wm = pulse_angular(power_set())
        wn = spin_set(max_net(base, wl))

        wr = Symbol('wr', positive=True)

        eq1 = Eq(2 * k * wm - k * wr - math.sqrt(3) * wr - k * wl + math.sqrt(3) * wl, 0)
        eq2 = Eq(wr ** 2 + wl ** 2 + wm ** 2 - wr * wl - wl * wm - wr * wm - wn ** 2, 0)

        sol = solve([eq1, eq2], dict=True)

        middle = left = wl
        right = sol[0][wr]

        print("left = ", left)
        print("right = ", right)
        print("middle = ", middle)

        menu()
        return left, right, middle

    elif base == "right+mid":
        wr = wm = pulse_angular(power_set())
        wn = spin_set(max_net(base, wr))

        wl = Symbol('wl', positive=True)

        eq1 = Eq(2 * k * wm - k * wr - math.sqrt(3) * wr - k * wl + math.sqrt(3) * wl, 0)
        eq2 = Eq(wr ** 2 + wl ** 2 + wm ** 2 - wr * wl - wl * wm - wr * wm - wn ** 2, 0)

        sol = solve([eq1, eq2], dict=True)

        right = middle = wr
        left = sol[0][wl]

        print("left = ", left)
        print("right = ", right)
        print("middle = ", middle)

        menu()
        return left, right, middle


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


menu()
