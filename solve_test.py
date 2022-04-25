from sympy import Eq, symbols, solve
import math


theta = math.pi / 6
k = float(math.tan(theta))
w1 = 600
wn = 3000

w2, w3 = symbols('w2 w3', real=True)

eq1 = Eq(2 * k * w3 + (math.sqrt(3) - k) * w1 - (math.sqrt(3) + k) * w2, 0)
eq2 = Eq((w1 + w2) ** 2 + w3 * w3 - w1 * w3 - w2 * w3 - wn ** 2, 0)

print(solve([eq1, eq2]))
