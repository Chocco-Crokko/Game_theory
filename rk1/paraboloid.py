import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import pi, sqrt
import random


def coordinates(phi, t, a):
    return t * np.cos(phi), t * np.sin(phi), a * t ** 2


def random_point(t_max, a):
    phi = 2 * pi * random.random()
    t = random.uniform(0, t_max)
    return np.array(coordinates(phi, t, a))


def dist(a, b):
    return np.linalg.norm(a - b)


def add_point_if_not_insersect(points, new_point, r):
    for point in points:
        if dist(point, new_point) < 2 * r:
            return
    points.append(new_point)


def prepare_game(t_max, a, s, r):
    points = []
    while len(points) < s:
        rp = random_point(t_max, a)
        add_point_if_not_insersect(points, rp, r)
    return points


def game_price_by_simulations(points, t_max, a, r, simulations):
    wins = 0
    for i in range(simulations):
        rp = random_point(t_max, a)
        for point in points:
            if dist(point, rp) < r:
                wins += 1
                break
    return wins / simulations


def draw_points(ax, points, r):
    for point in points:
        ax.scatter(*point, color='r')


def draw_paraboloid(ax, t_max, a):
    phi = np.linspace(0, 2 * pi)
    t = np.linspace(0, t_max)
    phi_mesh, t_mesh = np.meshgrid(phi, t)
    ax.plot_wireframe(*coordinates(phi_mesh, t_mesh, a), color='b')


def main():
    if len(sys.argv) < 6:
        print('Usage: <program_name> <h_max> <a> <number_of_points> <sphere_radius> <number_of_simulations>')
        return
    h_max = float(sys.argv[1])
    a = float(sys.argv[2])
    s = int(sys.argv[3])
    r = float(sys.argv[4])
    simulations = int(sys.argv[5])

    t_max = sqrt(h_max) / a
    points = prepare_game(t_max, a, s, r)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    draw_points(ax, points, r)
    draw_paraboloid(ax, t_max, a)

    v = game_price_by_simulations(points, t_max, a, r, simulations)
    print(f'v = {v}')
    
    plt.show()


if __name__ == '__main__':
    main()
