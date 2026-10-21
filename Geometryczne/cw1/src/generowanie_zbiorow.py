import numpy as np
from pathlib import Path

POINTS_DIR = Path(__file__).resolve().parent.parent / "points"


# Generowanie zbioru A
def generate_setA(N=100_000, save=True, seed=16):
    np.random.seed(seed)
    points = np.random.uniform(-1000.0, 1000.0, size=(N, 2))
    if save:
        np.savetxt(POINTS_DIR / "setA_points.csv", points, delimiter=",")
    return points


# Generowanie zbioru B
def generate_setB(N=100_000, save=True, seed=16):
    np.random.seed(seed)
    points = np.random.uniform(-1e14, 1e14, size=(N, 2))
    if save:
        np.savetxt(POINTS_DIR / "setB_points.csv", points, delimiter=",")
    return points


# Generowanie zbioru C
def generate_setC(N=1000, r=100.0, save=True, seed=16):
    np.random.seed(seed)
    theta = np.random.uniform(0, 2 * np.pi, size=N)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    points = np.column_stack((x, y))
    if save:
        np.savetxt(POINTS_DIR / "setC_points.csv", points, delimiter=",")
    return points


# Generowanie zbioru D (równanie kierunkowe: y = 0.05x + 0.05)
def generate_setD(N=1000, save=True, seed=16):
    np.random.seed(seed)
    x = np.random.uniform(-1000.0, 1000.0, size=N)
    y = 0.05 * x + 0.05
    points = np.column_stack((x, y))
    if save:
        np.savetxt(POINTS_DIR / "setD_points.csv", points, delimiter=",")
    return points


# Generowanie zbioru D za pomocą równania parametrycznego wektora: P(t) = a + t * (b - a)
def generate_setD_parametric(N=1000, save=True, seed=16):
    np.random.seed(seed)
    # Dla a = [-1.0, 0.0] i b = [1.0, 0.1]:
    # b - a = [2.0, 0.1]
    # Losujemy t z przedziału [-500, 500], aby x = -1 + 2t leżało w [-1001, 999]
    t = np.random.uniform(-500.0, 500.0, size=N)
    x = -1.0 + 2.0 * t
    y = 0.0 + 0.1 * t
    points = np.column_stack((x, y))
    if save:
        np.savetxt(POINTS_DIR / "setD_param_points.csv", points, delimiter=",")
    return points

