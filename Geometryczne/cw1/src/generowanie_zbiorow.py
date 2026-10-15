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


# Generowanie zbioru D
def generate_setD(N=1000, save=True, seed=16):
    np.random.seed(seed)
    x = np.random.uniform(-1000.0, 1000.0, size=N)
    y = 0.05 * x + 0.05
    points = np.column_stack((x, y))
    if save:
        np.savetxt(POINTS_DIR / "setD_points.csv", points, delimiter=",")
    return points
