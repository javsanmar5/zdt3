import math


def zdt3(x: list) -> list:
    return (_f1(x), _f2(x))

def _f1(x: list) -> float:
    return x[0]

def _f2(x: list) -> float:
    g_val = _g(x)
    f1_val = _f1(x)
    return g_val * (1 - math.sqrt(f1_val / g_val) - (f1_val / g_val) * math.sin(10 * math.pi * f1_val))

def _g(x: list) -> float:
    return 1 + 9 * sum(x[1:]) / (len(x) - 1)
