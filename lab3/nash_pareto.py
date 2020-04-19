import sys
import numpy as np
from sage.all import *
from random import randint
import itertools as it


def random_matrix(n, lower, upper):
    return Matrix(n, n, lambda i, j: randint(lower, upper))


def random_game(players, n, lower=-99, upper=99):
    assert(players == 2)
    return tuple(random_matrix(n, lower, upper) for k in range(players))


def get_player_value_with_new_strategy(game, p, strat, x_p):
    x = game[p]
    for i in range(len(strat)):
        if i == p:
            x = x[x_p]
        else:
            x = x[strat[i]]
    return x


def get_player_value(game, p, strat):
    x = game[p]
    for i in range(len(strat)):
        x = x[strat[i]]
    return x


def get_game_value(game, strat):
    players = len(game)
    return tuple(get_player_value(game, p, strat) for p in range(players))


def is_nash_optimal(game, players, n, strat):
    h = get_game_value(game, strat)
    for p in range(players):
        for x_p in range(n):
            if x_p == strat[p]:
                continue
            if get_player_value_with_new_strategy(game, p, strat, x_p) > h[p]:
                return False
    return True


def nash_optimal(game):
    players, dimensions = len(game), game[0].dimensions()
    assert(dimensions[0] == dimensions[1])
    n = dimensions[0]
    res = []
    for strat in it.product(range(n), repeat=players):
        if is_nash_optimal(game, players, n, strat):
            res.append(strat)
    return res


def is_pareto_dominated_by(game, players, n, h, strat_p):
    strictly_more = False
    for p in range(players):
        h_p = get_player_value(game, p, strat_p)
        if h[p] < h_p:
            strictly_more = True
        elif h[p] > h_p:
            return False
    return strictly_more


def is_pareto_optimal(game, players, n, strat):
    h = get_game_value(game, strat)
    for strat_p in it.product(range(n), repeat=players):
        if is_pareto_dominated_by(game, players, n, h, strat_p):
            return False
    return True


def pareto_optimal(game):
    players, dimensions = len(game), game[0].dimensions()
    assert(dimensions[0] == dimensions[1])
    n = dimensions[0]
    res = []
    for strat in it.product(range(n), repeat=players):
        if is_pareto_optimal(game, players, n, strat):
            res.append(strat)
    return res


def print_game(game, form_func):
    players, dimensions = len(game), game[0].dimensions()
    assert(dimensions[0] == dimensions[1])
    n = dimensions[0]
    for i in range(n):
        print('[{}]'.format(' '.join('({})'.format(
            ','.join(form_func(game[p][i][j]) for p in range(players))) for j in range(n))))


def print_optimals(game, form_func=lambda x: '{:3}'.format(x)):
    print_game(game, form_func)
    nash_opt = nash_optimal(game)
    pareto_opt = pareto_optimal(game)
    both_opt = list(set(nash_opt) & set(pareto_opt))
    nash_opt, pareto_opt, both_opt = (list(get_game_value(game, strat) for strat in opt)
     for opt in (nash_opt, pareto_opt, both_opt))
    print('Nash optimal strategies:')
    print(nash_opt)
    print('Pareto optimal strategies:')
    print(pareto_opt)
    print('Optimal in both ways strategies:')
    print(both_opt)
    print('')


def check_algorithms():
    dispute = (Matrix([[4, 0], [0, 1]]), Matrix([[1, 0], [0, 4]]))
    print('Family dispute game')
    print_optimals(dispute)

    first_eps, second_eps = 0.5, 0.1
    crossroad = (Matrix([[1, 1 - first_eps], [2, 0]]), Matrix([[1, 2], [1 - second_eps, 0]]))
    print('Crossroad game')
    print_optimals(crossroad, lambda x: '{:.1f}'.format(float(x)))

    print('Prisoner\'s dilemma game')
    prisoners = (Matrix([[-5, 0], [-10, -1]]), Matrix([[-5, -10], [0, -1]]))
    print_optimals(prisoners)


# is a >= b
def is_strictly_dominate(a, b):
    strictly_more = False
    for i in range(len(a)):
        if a[i] < b[i]:
            return False
        elif a[i] > b[i]:
            strictly_more = True
    return strictly_more


def find_dominant_for_2(game):
    players, n = 2, 2
    game[0]
    for p, func in ((0, game[0].row), (1, game[1].column)):
        for i in range(n):
            if is_strictly_dominate(func(i), func(1 - i)):
                return p, func(i)
    return -1, None


def mixed_strategy(game):
    players, dimensions = len(game), game[0].dimensions()
    assert(players == 2 and dimensions == (2, 2))
    n = dimensions[0]
    p, strat = find_dominant_for_2(game)
    if strat is not None:
        x, y = strat
        return x, y, game[0][x][y], game[1][x][y]
    strats = nash_optimal(game)
    if len(strats) == 0 or len(strats) == 2:
        for i in range(2):
            assert(game[i].det() != 0)
        u = vector([1, 1])
        v1 = 1 / (u * game[0].inverse() * u)
        v2 = 1 / (u * game[1].inverse() * u)
        x = v2 * u * game[1].inverse()
        y = v1 * game[0].inverse() * u
        return x, y, v1, v2


def printable_vector(v):
    return '({})'.format(', '.join('{:.3f}'.format(float(x)) for x in v))


def main():
    check_algorithms()
    rand_game = random_game(2, 10)
    print('Random {}x{} game'.format(10, 10))
    print_optimals(rand_game)

    game = (Matrix([[6, 8], [2, 9]]), Matrix([[7, 4], [1, 3]]))
    print('Bimatrix 2x2 game')
    print_game(game, lambda x: '{:1}'.format(x))
    print('Nash optimal strategies:')
    print(list(get_game_value(game, strat) for strat in nash_optimal(game)))
    x, y, v1, v2 = mixed_strategy(game)
    print('Mixed strategy:\nx={}, y={}, v1={}, v2={}\n'
        .format(*(printable_vector(val) for val in (x, y, v1, v2))))


if __name__ == '__main__':
    main()
