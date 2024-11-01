import math


def cf6(xreal):
    n = len(xreal)
    obj = [0.0, 0.0]
    sum1 = sum2 = 0.0
    
    for j in range(2, n + 1):
        if j % 2 == 1:
            yj = xreal[j-1] - 0.8 * xreal[0] * math.cos(6.0 * math.pi * xreal[0] + j * math.pi / n)
            sum1 += yj * yj
        else:
            yj = xreal[j-1] - 0.8 * xreal[0] * math.sin(6.0 * math.pi * xreal[0] + j * math.pi / n)
            sum2 += yj * yj

    obj[0] = xreal[0] + sum1
    obj[1] = (1.0 - xreal[0]) ** 2 + sum2
    
    return obj
