import sys
import numpy as np
from sage.all import *
from brown_robinson import br_rob, max_with_index, min_with_index


def h(x, y, a, b, c, d, e):
    return a*x**2 + b*y**2 + c*x*y + d*x + e*y


def get_settle(m):
    minmax = None
    minmax_ij = None
    for i, row in enumerate(m.rows()):
        min_row, j = min_with_index(row, rand_choice=False)
        if minmax is None or min_row > minmax:
            minmax = min_row
            minmax_ij = list((i, j_) for j_ in j)
        elif min_row == minmax:
            minmax_ij.extend(list((i, j_) for j_ in j))
    maxmin = None
    maxmin_ij = None
    for j, column in enumerate(m.columns()):
        max_column, i = max_with_index(column, rand_choice=False)
        if maxmin is None or max_column < maxmin:
            maxmin = max_column
            maxmin_ij = list((i_, j) for i_ in i)
        elif max_column == minmax:
            maxmin_ij.extend(list((i_, j) for i_ in i))
    if len(minmax_ij) == 1 and len(maxmin_ij) == 1 and minmax_ij[0] == maxmin_ij[0]:
        return minmax_ij[0]
    else:
        return None


def print_matrix(m, digits=3):
    print(m.str(rep_mapping=lambda x : rational_to_str(x)))


def rational_to_str(r):
    return '{:.3f}'.format(float(r))


def exact_solution(a, b, c, d, e):
    a, b, c, d, e = (QQ(x) for x in (a, b, c, d, e))
    assert(a < 0 and b > 0)
    x = var('x')
    y = var('y')
    x_eq = -(c * y + d) / (2 * a)
    y_eq = -(c * x + e) / (2 * b)
    y_sol = solve((y == y_eq(x=x_eq)), y)[0].rhs()
    x_sol = x_eq(y=y_sol)
    assert((y_eq(x=x_sol) - y_sol).n() == 0)
    return x_sol, y_sol, h(x_sol, y_sol, a, b, c, d, e)


def find_closest(M, value):
    m, n = M.dimensions()
    diff = None
    for i in range(m):
        for j in range(n):
            d = abs(M[i][j] - value)
            if diff is None or d < diff:
                diff = d
                res = (i, j)
    i, j = res
    return i, j, M[i][j]


def numerical_solution(a, b, c, d, e, N):
    for k in range(2, N + 1):
        n = k
        n_matrix = n + 1
        m = Matrix(n_matrix, n_matrix, lambda i, j: h(i/n, j/n, a, b, c, d, e))
        print(f'N = {k}')
        print_matrix(m)
        s = get_settle(m)
        if s is None:
            print('There is no settle point, finding solution with Brown-Robinson\'s method:')
            x, y, v_upper, v_lower, iterations = br_rob(m, eps_threshold=0.01)
            i, j, v = find_closest(m, (v_upper + v_lower) / 2)
            print('x = {}, y = {}, H = {}'.format(
                *(rational_to_str(val) for val in (i/n, j/n, v))))
        else:
            print('Settle point:\nx = {}, y = {}, H = {}'.format(
                *(rational_to_str(v) for v in (s[0]/n, s[1]/n, h(s[0]/n, s[1]/n, a, b, c, d, e)))))
        print('')


def main():
    if len(sys.argv) < 2:
        print('Usage: <program_name> <N>')
        return
    N = int(sys.argv[1])
    # a = -3
    # b = 3/2
    # c = 18/5
    # d = -18/50
    # e = -72/25
    a = -5
    b = 10/3
    c = 10
    d = -2
    e = -8
    x, y, v = exact_solution(a, b, c, d, e)
    print('Analytical results:\nx={}, y={}, v={}\n'.format(
        *(rational_to_str(val) for val in (x, y, v))))
    print('Numerical results')
    numerical_solution(a, b, c, d, e, N)



if __name__ == '__main__':
    main()