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

def pulse_angular():
    pulse = int(raw_input())
    volt = float(float(9 / 2000) * pulse)
    wh_angular = float(volt * 60 * math.pi)
    ball_angular = wh_angular * float(101.6 / 40)
    return ball_angular


def angle_calc():
    while True:
        class BallAngular(object):
            def __init__(self):
                while True:
                    try:
                        print("Give left wheel pulsewidth.")
                        self.left = pulse_angular()

                        print("Give right wheel pulsewidth.")
                        self.right = pulse_angular()

                        print("Give mid wheel pulsewidth.")
                        self.mid = pulse_angular()

                        break
                    except ValueError:
                        print("cringe.")

        ball = BallAngular()

        class LeftAngular:
            i = ball.left * math.sin(math.pi / 6)  # left.i * sqrt3/2
            j = ball.left * math.cos(math.pi / 6)  # left.j * 1/2

        l_vector = LeftAngular()

        class RightAngular:
            i = ball.right * math.sin(11 * math.pi / 6)  # right.i * sqrt3/2
            j = ball.right * math.cos(11 * math.pi / 6)  # right.i * -1/2

        r_vector = RightAngular()

        class MidAngular:
            i = ball.mid * math.cos(math.pi)  # mid.i * -1
            j = ball.mid * math.sin(0)  # mid.i * 0

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
            print("\n------------------")
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
            print("ball left = ", ball.left)
            print("ball right = ", ball.right)
            print("ball mid = ", ball.mid)
            print("------------------")
            print("\n")

        except ZeroDivisionError:
            print("no spin\n")

        print("[stop] or any input.")
        inp = raw_input()

        if inp == "stop":
            break


angle_calc()

# deg = int(raw_input())

# theta = float(deg * float(math.pi / 180))
