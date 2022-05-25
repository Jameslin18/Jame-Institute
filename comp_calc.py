import math
from sympy import Eq, symbols, solve, Symbol
from calc import power_set, raw_input, calc_pulse_eq


def horiz_spin_set():
    print("Choose spin: [top] [bottom]")
    direction = raw_input()
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

    pulse = float(2000 * float(power / 100))

    print(direction.capitalize(), "spin set to ", pulse, ".")

    return pulse, direction


def side_spin_set():
    print("Choose spin: [left] [right]")
    direction = raw_input()
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

    pulse = float(2000 * float(power / 100))

    print(direction.capitalize(), "spin set to ", pulse, ".")

    return pulse, direction


def choose_wheel(theta):
    while True:
        if 0 < float(theta) < 2 * math.pi / 3:
            base = "left"
            print("Base wheel(s) = ", base)
            return base
        elif 4 * math.pi / 3 < float(theta) < 2 * math.pi:
            base = "right"
            print("Base wheel(s) = ", base)
            return base
        elif 2 * math.pi / 3 < float(theta) < 4 * math.pi / 3:
            base = "mid"
            print("Base wheel(s) = ", base)
            return base
        elif float(theta) == 0 and 2 * math.pi:
            base = "left+right"
            print("Base wheel(s) = ", base)
            return base
        elif float(theta) == 2 * math.pi / 3:
            base = "left+mid"
            print("Base wheel(s) = ", base)
            return base
        elif float(theta) == 4 * math.pi / 3:
            base = "right+mid"
            print("Base wheel(s) = ", base)
            return base


def dir_inp(value, direction):
    if direction == "bottom" or "left":
        out = -1 * value
        return out
    else:
        return value


def main_calc(min_value, w_net, k, base):
    if base == "left":
        wl = min_value
        if wl == 2000:
            right = middle = wl
            print("No Spin.")
        else:
            wn = w_net

            wr, wm = symbols('wr wm', real=True)

            eq1, eq2 = calc_pulse_eq(k, wr, wl, wm, wn)

            sol = solve([eq1, eq2], [wr, wm], dict=True)

            try:
                right = sol[1][wr]
                middle = sol[1][wm]
            except IndexError:
                right = sol[0][wr]
                middle = sol[0][wm]

        left = wl

        print("right = ", right)
        print("left = ", left)
        print("middle = ", middle)

        # menu()
        return right, left, middle

    elif base == "right":
        wr = min_value
        if wr == 2000:
            left = middle = wr
            print("No Spin.")
        else:
            wn = w_net

            wl, wm = symbols('wl wm', real=True)

            eq1, eq2 = calc_pulse_eq(k ,wr, wl, wm, wn)

            sol = solve([eq1, eq2], dict=True)

            try:
                left = sol[1][wl]
                middle = sol[1][wm]
            except IndexError:
                left = sol[0][wl]
                middle = sol[0][wm]

        right = wr

        print("right = ", right)
        print("left = ", left)
        print("middle = ", middle)

        # menu()
        return right, left, middle

    elif base == "mid":
        wm = min_value
        if wm == 2000:
            left = right = wm
            print("No Spin.")
        else:
            wn = w_net

            wr, wl = symbols('wr wl', real=True)

            eq1, eq2 = calc_pulse_eq(k ,wr, wl, wm, wn)

            sol = solve([eq1, eq2], dict=True)

            try:
                right = sol[1][wr]
                left = sol[1][wl]
            except IndexError:
                right = sol[0][wr]
                left = sol[0][wl]

        middle = wm

        print("right = ", right)
        print("left = ", left)
        print("middle = ", middle)

        # menu()
        return right, left, middle

    elif base == "left+right":
        wr = wl = min_value
        if wr == 2000:
            middle = wr
            print("No Spin.")
        else:
            wn = w_net

            wm = Symbol('wm', real=True)

            eq1, eq2 = calc_pulse_eq(k ,wr, wl, wm, wn)

            sol = solve([eq1, eq2], dict=True)

            try:
                middle = sol[1][wm]
            except IndexError:
                middle = sol[0][wm]

        right = left = wl

        print("right = ", right)
        print("left = ", left)
        print("middle = ", middle)

        # menu()
        return right, left, middle

    elif base == "left+mid":
        wl = wm = min_value
        if wl == 2000:
            right = wl
            print("No Spin.")
        else:
            wn = w_net

            wr = Symbol('wr', real=True)

            eq1, eq2 = calc_pulse_eq(k ,wr, wl, wm, wn)

            sol = solve([eq1, eq2], dict=True)

            try:
                right = sol[1][wr]
            except IndexError:
                right = sol[0][wr]

        middle = left = wl

        print("right = ", right)
        print("left = ", left)
        print("middle = ", middle)

        # menu()
        return right, left, middle

    elif base == "right+mid":
        wr = wm = min_value
        if wr == 2000:
            left = wr
            print("No Spin.")
        else:
            wn = w_net

            wl = Symbol('wl', real=True)

            eq1, eq2 = calc_pulse_eq(k, wr, wl, wm, wn)

            sol = solve([eq1, eq2], dict=True)

            try:
                left = sol[1][wl]
            except IndexError:
                left = sol[0][wl]

        right = middle = wr

        print("right = ", right)
        print("left = ", left)
        print("middle = ", middle)

        # menu()
        return right, left, middle


def print_deg(x, y):
    deg = float(math.degrees(math.atan2(y, x)))
    if deg < 0:
        print("\nAngle of spin = ", 360 + deg, "degrees")
    else:
        print("\nAngle of spin = ", deg, "degrees")


def comp_calc_pulse():
    min_val = power_set()
    h_val, h_dir = horiz_spin_set()
    s_val, s_dir = side_spin_set()

    if h_val == s_val == 0:
        right = left = mid = min_val
        out = right, left, mid
        print("No spin.")
        return out

    else:
        x_net = dir_inp(s_val, s_dir)
        y_net = dir_inp(h_val, h_dir)

        w_net = float(math.hypot(x_net, y_net))
        k = float(y_net/x_net)

        raw_theta = float((math.atan2(y_net, x_net)))
        if raw_theta < 0:
            theta = 2*math.pi + raw_theta
        else:
            theta = raw_theta

        base = choose_wheel(theta)

        right, left, mid = main_calc(min_val, w_net, k, base)
        out = right, left, mid

        print_deg(x_net, y_net)

        return out

comp_calc_pulse()