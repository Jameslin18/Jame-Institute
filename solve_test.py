from sympy import symbols
import sympy as sy
import math

theta = math.pi / 6

tan = float(math.tan(theta))

ang_v = 600

ang_n = 3000

w1, wN, k, w2, w3 = sy.symbols('w1 wN k w2 w3')

# f1 = Eq(2 * k * w3 + (math.sqrt(3) - k) * w1 - (math.sqrt(3) + k) * w2, 0)
# f2 = Eq((w1 + w2) ** 2 + w3(w3 - w1 - w2) - wN ** 2, 0)

sol = sy.nsolve((2 * k * w3 + (math.sqrt(3) - k) * w1 - (math.sqrt(3) + k) * w2),
                ((w1 + w2) ** 2 + w3(w3 - w1 - w2) - wN ** 2),
                (w2, w3), (0, 0))

sy.nsolve.subs(w1, 600)
sy.nsolve.subs(wN, 3000)
sy.nsolve.subs(k, math.tan(math.pi/6))

print(sol)
