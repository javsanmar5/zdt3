import math

import numpy as np


def cf6(x):
    n = len(x)
    obj = [0.0, 0.0]
    sum1 = sum2 = 0.0
    
    for j in range(2, n + 1):
        if j % 2 == 1:
            yj = x[j-1] - 0.8 * x[0] * math.cos(6.0 * math.pi * x[0] + j * math.pi / n)
            sum1 += yj * yj
        else:
            yj = x[j-1] - 0.8 * x[0] * math.sin(6.0 * math.pi * x[0] + j * math.pi / n)
            sum2 += yj * yj

    obj[0] = x[0] + sum1
    obj[1] = (1.0 - x[0]) ** 2 + sum2
    
    return obj

    
def constraints_cf6(x):
    return _constraint1(x) + _constraint2(x)
    
def _constraint1(x):
    n = len(x)
    left_term = x[1] - 0.8 * x[0] * np.sin(6 * np.pi * x[0] + (2 * np.pi / n))
    term = 0.5 * (1 - x[0]) - (1 - x[0]) ** 2
    right_term = np.sign(term) * np.sqrt(abs(term))
    if left_term - right_term < 0:
        return left_term - right_term
    return 0

def _constraint2(x):
    n = len(x)
    left_term = x[3] - 0.8 * x[0] * np.sin(6 * np.pi * x[0] + (4 * np.pi / n))
    term = 0.25 * np.sqrt(1 - x[0]) - 0.5 * (1 - x[0])
    right_term = np.sign(term) * np.sqrt(abs(term))
    if left_term - right_term < 0:
        return left_term - right_term
    return 0
    
