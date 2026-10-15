import numpy as np


def det_3x3_custom(a, b, c, dtype=np.float64):
    """
    Własny wyznacznik 3x3 z narzuconą precyzją (float32 lub float64).
    """
    xa, ya = dtype(a[0]), dtype(a[1])
    xb, yb = dtype(b[0]), dtype(b[1])
    xc, yc = dtype(c[0]), dtype(c[1])

    return (xa * yb + ya * xc + xb * yc) - (yb * xc + xa * yc + ya * xb)


def det_2x2_custom(a, b, c, dtype=np.float64):
    """
    Własny wyznacznik 2x2 z narzuconą precyzją (float32 lub float64).
    """
    xa, ya = dtype(a[0]), dtype(a[1])
    xb, yb = dtype(b[0]), dtype(b[1])
    xc, yc = dtype(c[0]), dtype(c[1])

    return (xa - xc) * (yb - yc) - (ya - yc) * (xb - xc)


def det_3x3_numpy(a, b, c, dtype=np.float64):
    """
    Wyznacznik 3x3 z biblioteki NumPy w zadanej precyzji.
    """
    matrix = np.array(
        [[a[0], a[1], 1.0], [b[0], b[1], 1.0], [c[0], c[1], 1.0]], dtype=dtype
    )
    return np.linalg.det(matrix)


def det_2x2_numpy(a, b, c, dtype=np.float64):
    """
    Wyznacznik 2x2 z biblioteki NumPy w zadanej precyzji.
    """
    matrix = np.array(
        [[a[0] - c[0], a[1] - c[1]], [b[0] - c[0], b[1] - c[1]]], dtype=dtype
    )
    return np.linalg.det(matrix)


def classify_orientation(det_val, eps=0.0):
    if det_val > eps:
        return 1  # Lewo
    elif det_val < -eps:
        return -1  # Prawo
    else:
        return 0  # Na prostej
