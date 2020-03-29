import random as rand
import operator
from sage.all import *


def _max_min_with_index(v, func, rand_choice=True):
    m = v[0]
    indexes = [0]
    for i in range(1, len(v)):
        if func(v[i], m):
            m = v[i]
            indexes = [i]
        elif v[i] == m:
            indexes.append(i)
    if rand_choice:
        return m, rand.choice(indexes)
    else:
        return m, indexes


def max_with_index(v, rand_choice=True):
    return _max_min_with_index(v, operator.gt, rand_choice)


def min_with_index(v, rand_choice=True):
    return _max_min_with_index(v, operator.lt, rand_choice)


def print_br_rob_step(x_strategy, y_strategy, x, y, v_upper, v_lower, k):
    print(x_strategy, y_strategy, x, y, v_upper, v_lower, k)


def br_rob(C, eps_threshold=0.1, print_intermediate=False):
    m, n = C.dimensions()
    x = C.column(0)
    y = C.row(0)
    x_strategy = vector([1] + [0] * (m - 1))
    y_strategy = vector([1] + [0] * (n - 1))
    v_upper_min, next_a = max_with_index(x)
    v_lower_max, next_b = min_with_index(y)
    eps = v_upper_min - v_lower_max
    k = 1
    if print_intermediate:
        print_br_rob_step(x_strategy, y_strategy, x, y, v_upper_min, v_lower_max, k)
    while eps > eps_threshold:
        k += 1
        x_strategy[next_a] += 1
        y_strategy[next_b] += 1
        x += C.column(next_b)
        y += C.row(next_a)
        v_upper, next_a = max_with_index(x)
        v_lower, next_b = min_with_index(y)
        v_upper /= k
        v_lower /= k
        if v_upper < v_upper_min:
            v_upper_min = v_upper
        if v_lower > v_lower_max:
            v_lower_max = v_lower
        eps = v_upper_min - v_lower_max
        if print_intermediate:
            print_br_rob_step(x_strategy, y_strategy, x, y, v_upper, v_lower, k)
    return x_strategy / k, y_strategy / k, v_upper_min, v_lower_max, k


def printable_vector(v):
    # return v
    return '(' + ', '.join('{:.3f}'.format(float(x)) for x in v) + ')'


if __name__ == '__main__':
    C = Matrix([[17, 4, 9], [0, 16, 9], [12, 2, 19]])
    # C = Matrix([[2, 1, 3], [3, 0, 1], [1, 2, 1]])
    u = vector([1, 1, 1])
    eps = 0.1
    # eps = 1/12
    print(C)

    C_inv = C.inverse()
    v = 1 / (u * (C_inv * u))
    x = v * (u * C_inv)
    y = v * (C_inv * u)
    x_, y_, v_upper, v_lower, iterations = br_rob(C, eps)
    print('Analytic results:\nx={}, y={}, v={}\n'.format(printable_vector(x),
     printable_vector(y), printable_vector(v)))
    print('Numerical results:\nx={}, y={}, {}<=v<={}, eps={}, iterations={}\n'
        .format(printable_vector(x_), printable_vector(y_), printable_vector(v_lower),
         printable_vector(v_upper), printable_vector(v_upper - v_lower), iterations))
