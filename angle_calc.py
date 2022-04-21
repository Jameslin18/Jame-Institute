import math


def raw_input():
    inp = input("Input: ")
    return inp


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
                        # volt_l = float(float(9 / 2000) * pulse_l)
                        # self.left = float(volt_l * 60 * math.pi)
                        self.left = pulse_l

                        print("Give right wheel pulsewidth.")
                        pulse_r = int(raw_input())
                        # volt_r = float(float(9 / 2000) * pulse_r)
                        # self.right = float(volt_r * 60 * math.pi)
                        self.right = pulse_r

                        print("Give mid wheel pulsewidth.")
                        pulse_m = int(raw_input())
                        # volt_m = float(float(9 / 2000) * pulse_m)
                        # self.mid = float(volt_m * 60 * math.pi)
                        self.mid = pulse_m

                        break
                    except ValueError:
                        print("cringe.")

        wheel = WheelAngular()

        class LeftAngular:
            i = wheel.left * math.cos(math.pi / 6)
            j = wheel.left * math.sin(math.pi / 6)

        l_vector = LeftAngular()

        class RightAngular:
            i = wheel.right * math.cos(11 * math.pi / 6)
            j = wheel.right * math.sin(11 * math.pi / 6)

        r_vector = RightAngular()

        class MidAngular:
            i = wheel.mid * math.cos(0)
            j = wheel.mid * math.sin(0)

        m_vector = MidAngular()

        class NetAngular:
            i = l_vector.i + r_vector.i + m_vector.j
            j = l_vector.j + r_vector.j

        n_vector = NetAngular()

        try:
            theta = math.atan(n_vector.j / n_vector.i)
            deg = int((theta * float(180 / math.pi)))
            print("\nAngle = ", deg, "degrees")
            print("tan() = ", float(n_vector.j / n_vector.i), "\n")

        except ZeroDivisionError:
            print("no spin\n")

        print("[stop] or any input.\n")
        inp = raw_input()

        if inp == "stop":
            break


angle_calc()

# deg = int(raw_input())

# theta = float(deg * float(math.pi / 180))
