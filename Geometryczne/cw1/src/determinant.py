import numpy as np


def det_3x3_custom(a, b, c, dtype=np.float64):
    """
    Oblicza wyznacznik 3x3 z reguły Sarrusa ze współrzędnych jednorodnych:
    | a_x  a_y  1 |
    | b_x  b_y  1 |
    | c_x  c_y  1 |
    w zadanej precyzji sprzętowej (np.float64 lub np.float32).
    """
    xa, ya = dtype(a[0]), dtype(a[1])
    xb, yb = dtype(b[0]), dtype(b[1])
    xc, yc = dtype(c[0]), dtype(c[1])

    return (xa * yb + ya * xc + xb * yc) - (yb * xc + xa * yc + ya * xb)


def det_2x2_custom(a, b, c, dtype=np.float64):
    """
    Oblicza wyznacznik 2x2 z wektorów przesuniętych względem punktu c:
    | a_x - c_x   a_y - c_y |
    | b_x - c_x   b_y - c_y |
    w zadanej precyzji sprzętowej (np.float64 lub np.float32).
    """
    xa, ya = dtype(a[0]), dtype(a[1])
    xb, yb = dtype(b[0]), dtype(b[1])
    xc, yc = dtype(c[0]), dtype(c[1])

    return (xa - xc) * (yb - yc) - (ya - yc) * (xb - xc)


def det_3x3_numpy(a, b, c, dtype=np.float64):
    """
    Oblicza wyznacznik 3x3 z użyciem funkcji bibliotecznej np.linalg.det.
    """
    matrix = np.array(
        [[a[0], a[1], 1.0], [b[0], b[1], 1.0], [c[0], c[1], 1.0]], dtype=dtype
    )
    return np.linalg.det(matrix)


def det_2x2_numpy(a, b, c, dtype=np.float64):
    """
    Oblicza wyznacznik 2x2 z użyciem funkcji bibliotecznej np.linalg.det.
    """
    matrix = np.array(
        [[a[0] - c[0], a[1] - c[1]], [b[0] - c[0], b[1] - c[1]]], dtype=dtype
    )
    return np.linalg.det(matrix)


def classify_orientation(det_val, eps=0.0):
    """
    Klasyfikuje położenie punktu c względem zorientowanej prostej ab
    z uwzględnieniem przedziału tolerancji wokół zera [-eps, eps].

    Zwraca:
       1 : po lewej stronie prostej (det > eps)
      -1 : po prawej stronie prostej (det < -eps)
       0 : na prostej / współliniowy (|det| <= eps)
    """
    if det_val > eps:
        return 1
    elif det_val < -eps:
        return -1
    else:
        return 0
