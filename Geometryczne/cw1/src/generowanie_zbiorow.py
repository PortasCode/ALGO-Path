import numpy as np
from pathlib import Path

POINTS_DIR = Path(__file__).resolve().parent.parent / "points"
POINTS_DIR.mkdir(exist_ok=True)


def generate_setA(N=100_000, save=True, seed=16):
    """
    Zbiór A: N punktów o współrzędnych losowanych niezależnie z rozkładu
    jednostajnego na przedziale [-1000, 1000].
    """
    np.random.seed(seed)
    points = np.random.uniform(-1000.0, 1000.0, size=(N, 2))
    if save:
        np.savetxt(POINTS_DIR / "setA_points.csv", points, delimiter=",")
    return points


def generate_setB(N=100_000, save=True, seed=16):
    """
    Zbiór B: N punktów o współrzędnych losowanych niezależnie z rozkładu
    jednostajnego na przedziale [-10^14, 10^14].
    """
    np.random.seed(seed)
    points = np.random.uniform(-1e14, 1e14, size=(N, 2))
    if save:
        np.savetxt(POINTS_DIR / "setB_points.csv", points, delimiter=",")
    return points


def generate_setC(N=1000, r=100.0, save=True, seed=16):
    """
    Zbiór C: N punktów leżących na okręgu o środku S=(0,0) i promieniu R=100.
    Kąt theta losowany z rozkładu jednostajnego na [0, 2*pi).
    """
    np.random.seed(seed)
    theta = np.random.uniform(0, 2 * np.pi, size=N)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    points = np.column_stack((x, y))
    if save:
        np.savetxt(POINTS_DIR / "setC_points.csv", points, delimiter=",")
    return points


def generate_setD(N=1000, save=True, seed=16):
    """
    Zbiór D: N punktów leżących na prostej wyznaczonej przez a=(-1, 0) i b=(1, 0.1).
    Równanie kierunkowe: y = 0.05 * x + 0.05, gdzie x in [-1000, 1000].
    """
    np.random.seed(seed)
    x = np.random.uniform(-1000.0, 1000.0, size=N)
    y = 0.05 * x + 0.05
    points = np.column_stack((x, y))
    if save:
        np.savetxt(POINTS_DIR / "setD_points.csv", points, delimiter=",")
    return points


def generate_setD_parametric(N=1000, save=True, seed=16):
    """
    Zbiór D (wariant parametryczny): Punkty generowane wektorowo ze wzoru P(t) = a + t * (b - a).
    Dla a=[-1, 0] i b=[1, 0.1] wektor kierunkowy to [2, 0.1].
    Parametr t losowany z [-500, 500] odpowiada zakresowi x in [-1001, 999].
    """
    np.random.seed(seed)
    t = np.random.uniform(-500.0, 500.0, size=N)
    x = -1.0 + 2.0 * t
    y = 0.0 + 0.1 * t
    points = np.column_stack((x, y))
    if save:
        np.savetxt(POINTS_DIR / "setD_param_points.csv", points, delimiter=",")
    return points

