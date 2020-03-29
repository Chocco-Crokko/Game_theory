#!/usr/bin/env sage

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


def main():
    if len(sys.argv) < 2:
        print('Usage: <program_name> <N>')
        return
    N = int(sys.argv[1])
    a = -3
    b = 3/2
    c = 18/5
    d = -18/50
    e = -72/25
    # a = -5
    # b = 10/3
    # c = 10
    # d = -2
    # e = -8
    for k in range(0, N):
        n = k + 2
        n_matrix = n + 1
        m = Matrix(n_matrix, n_matrix, lambda i, j: h(i/n, j/n, a, b, c, d, e))
        print_matrix(m)
        s = get_settle(m)
        if s is None:
            print('No settle point, finding solution with Brown-Robinson\'s method:')
            print(br_rob(m))
        else:
            print('Settle point:')
            print('x = {}, y = {}, H = {}'.format(
                *(rational_to_str(v) for v in (s[0]/n, s[1]/n, h(s[0]/n, s[1]/n, a, b, c, d, e)))))
        print('')


if __name__ == '__main__':
    main()