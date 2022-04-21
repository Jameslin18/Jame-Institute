import math


def raw_input():
    inp = input("Input: ")
    return inp


def angle_inp():
    print("Give angle of rotation.")
    deg = int(raw_input())
    theta = float(deg * math.pi/180)
    return theta


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

    print("Power set to ", power)

    return power


# def choose_base_wheel():
    # class WheelThrottle(object):
        # def __init__(self):
            # if 0 < theta


# power_set()


def get_pulse():
    v = float(w / 60 / math.pi)
    p = int(v / float(2000 / 9))
    return p


def angle_calc():
    while True:
        class WheelAngular(object):
            def __init__(self):
                while True:
                    try:
                        print("Give left wheel pulsewidth.")
                        pulse_l = int(raw_input())
                        volt_l = float(float(9 / 2000) * pulse_l)
                        wh_angular_l = float(volt_l * 60 * math.pi)
                        self.left = wh_angular_l * float(101.6/40)

                        print("Give right wheel pulsewidth.")
                        pulse_r = int(raw_input())
                        volt_r = float(float(9 / 2000) * pulse_r)
                        wh_angular_r = float(volt_r * 60 * math.pi)
                        self.right = wh_angular_r * float(101.6 / 40)

                        print("Give mid wheel pulsewidth.")
                        pulse_m = int(raw_input())
                        volt_m = float(float(9 / 2000) * pulse_m)
                        wh_angular_m = float(volt_m * 60 * math.pi)
                        self.mid = wh_angular_m * float(101.6 / 40)

                        break
                    except ValueError:
                        print("cringe.")

        wheel = WheelAngular()

        class LeftAngular:
            i = wheel.left * math.cos(5 * math.pi / 6)  # left.i * sqrt3/2
            j = wheel.left * math.sin(5 * math.pi / 6)  # left.j * 1/2

        l_vector = LeftAngular()

        class RightAngular:
            i = wheel.right * math.cos(7 * math.pi / 6)  # right.i * sqrt3/2
            j = wheel.right * math.sin(7 * math.pi / 6)  # right.i * -1/2

        r_vector = RightAngular()

        class MidAngular:
            i = wheel.mid * math.cos(0)  # mid.i * 1
            j = wheel.mid * math.sin(0)  # mid.i * 0

        m_vector = MidAngular()

        class NetAngular:
            i = int(l_vector.i + r_vector.i + m_vector.i)  # (left.i * sqrt3/2) + (right.i * sqrt3/2) - mid.i
            j = int(l_vector.j + r_vector.j + m_vector.j)  # (left.j * 1/2) - (right.i * 1/2) + 0

        n_vector = NetAngular()

        try:
            theta = math.atan2(n_vector.j, n_vector.i)
            deg = int((theta * float(180 / math.pi)))
            if deg < 0:
                print("\nAngle = ", 360 + deg, "degrees")
            else:
                print("\nAngle = ", deg, "degrees")
            print("i = ", n_vector.i)
            print("j = ", n_vector.j)
            print(m_vector.i, l_vector.i, r_vector.i)
            print("\n")

        except ZeroDivisionError:
            print("no spin\n")

        print("\n[stop] or any input.")
        inp = raw_input()

        if inp == "stop":
            break


angle_calc()

# deg = int(raw_input())

# theta = float(deg * float(math.pi / 180))
