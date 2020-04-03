import random as rand
import operator
from sage.all import *
import matplotlib.pyplot as plt
from collections import namedtuple
import xlwt


Br_rob_step = namedtuple('Br_rob_step', 'x_strat y_strat x y v_upper v_lower eps')

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


def br_rob(C, eps_threshold=0.1, return_intermediate=False):
    m, n = C.dimensions()
    x = C.column(0)
    y = C.row(0)
    x_strategy = vector([1] + [0] * (m - 1))
    y_strategy = vector([1] + [0] * (n - 1))
    v_upper_min, next_a = max_with_index(x)
    v_lower_max, next_b = min_with_index(y)
    eps = v_upper_min - v_lower_max
    k = 1
    if return_intermediate:
        intermediate = [Br_rob_step(0, 0, x, y, v_upper_min, v_lower_max, eps)]
    while eps > eps_threshold:
        k += 1
        x_strategy[next_a] += 1
        y_strategy[next_b] += 1
        next_a_print, next_b_print = next_a, next_b
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
        if return_intermediate:
            intermediate.append(Br_rob_step(next_a_print, next_b_print, x, y, v_upper, v_lower, eps))
    if return_intermediate:
        return x_strategy / k, y_strategy / k, v_upper_min, v_lower_max, k, intermediate
    else:
        return x_strategy / k, y_strategy / k, v_upper_min, v_lower_max, k


def printable_vector(v):
    # return v
    return '(' + ', '.join('{:.3f}'.format(float(x)) for x in v) + ')'


def draw_eps(intermediate):
    fig, ax = plt.subplots()
    ax.plot(list(range(1, len(intermediate) + 1)), list(step.eps for step in intermediate))
    ax.set(xlabel='iterations', ylabel=r'$\varepsilon$')
    fig.savefig('eps.png')


def draw_price(intermediate):
    fig, ax = plt.subplots()
    ax.plot(list(range(1, len(intermediate) + 1)), list(step.v_upper for step in intermediate), label='upper bound')
    ax.plot(list(range(1, len(intermediate) + 1)), list(step.v_lower for step in intermediate), label='lower bound')
    ax.legend()
    ax.set(xlabel='iterations', ylabel=r'game price')
    fig.savefig('price.png')


def print_step(ws, i, step, i_value):
    for j, x in enumerate((i_value, step.x_strat, step.y_strat, *step.x, *step.y,
     step.v_upper, step.v_lower, step.eps)):
        ws.write(i, j, x)        



def print_steps(intermediate):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Brown Robinson')
    print_step(ws, 0, Br_rob_step('x strat', 'y strat',
     ('x_{}'.format(i + 1) for i in range(len(b.x))),
     ('y_{}'.format(i + 1) for i in range(len(b.y))), 'v^/k', 'v_/k', 'eps'), 'k')
    for i, step in enumerate(intermediate):
        print_step(ws, i+1, step, i+1)
    wb.save('br_rob.xls')



def exact_solution(C):
    u = vector([1, 1, 1])
    C_inv = C.inverse()
    v = 1 / (u * (C_inv * u))
    x = v * (u * C_inv)
    y = v * (C_inv * u)
    return x, y, v


def main():
    C = Matrix([[17, 4, 9], [0, 16, 9], [12, 2, 19]])
    eps = 0.1
    print(C)

    x, y, v = exact_solution(C)
    x_, y_, v_upper, v_lower, iterations, intermediate = br_rob(C, eps, return_intermediate=True)
    draw_eps(intermediate)
    draw_price(intermediate)
    print_steps(intermediate)
    print('Analytic results:\nx={}, y={}, v={}\n'.format(printable_vector(x),
     printable_vector(y), printable_vector(v)))
    print('Numerical results:\nx={}, y={}, {}<=v<={}, eps={}, iterations={}\n'
        .format(printable_vector(x_), printable_vector(y_), printable_vector(v_lower),
         printable_vector(v_upper), printable_vector(v_upper - v_lower), iterations))


if __name__ == '__main__':
    main()
