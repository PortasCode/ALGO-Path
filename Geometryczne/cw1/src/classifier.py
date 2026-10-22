import numpy as np
from src.determinant import (
    det_3x3_custom,
    det_2x2_custom,
    det_3x3_numpy,
    det_2x2_numpy,
    classify_orientation,
)

A_POINT = [-1.0, 0.0]
B_POINT = [1.0, 0.1]

EPSILONS = [0.0, 1e-14, 1e-12, 1e-10, 1e-8, 1e-6]
DTYPES = [np.float64, np.float32]

METHODS = {
    "custom_3x3": det_3x3_custom,
    "custom_2x2": det_2x2_custom,
    "numpy_3x3": det_3x3_numpy,
    "numpy_2x2": det_2x2_numpy,
}


def classify_dataset(points, a, b, det_func, eps=0.0, dtype=np.float64):
    """
    Dla każdego punktu w tablicy 'points' oblicza wyznacznik za pomocą 'det_func'
    i klasyfikuje jego orientację za pomocą 'classify_orientation'.

    Parametry:
      points   : tablica punktów Nx2
      a, b     : punkty definiujące prostą
      det_func : funkcja licząca wyznacznik (np. det_2x2_custom)
      eps      : tolerancja dla zera
      dtype    : np.float64 lub np.float32

    Zwraca:
      tablicę (lub listę) etykiet o długości N, np. [1, -1, 0, 1, ...]
    """
    results = []
    for point in points:
        det = det_func(a, b, point, dtype)
        orient = classify_orientation(det, eps)
        results.append(orient)
    return np.array(results)


def count_categories(labels):
    """
    Zlicza liczbę punktów w poszczególnych kategoriach orientacji.

    Parametry:
      labels : tablica etykiet (1 = lewo, -1 = prawo, 0 = na prostej)

    Zwraca:
      słownik z podziałem: {"left": int, "right": int, "on": int}
    """
    return {
        "left": int(np.sum(labels == 1)),
        "right": int(np.sum(labels == -1)),
        "on": int(np.sum(labels == 0)),
    }


def find_differences(labels_1, labels_2):
    """
    Porównuje dwie tablice etykiet uzyskane dwiema różnymi metodami
    dla tego samego zbioru punktów.

    Zwraca:
      liczba_roznic : całkowita liczba punktów o różnych etykietach
      indeksy_roznic: lista/tablica indeksów punktów, gdzie metody się różnią
    """

    diff_indices = np.where(labels_1 != labels_2)[0]
    diff_count = len(diff_indices)

    return diff_count, diff_indices


def run_experiments(datasets_dict):
    """
    Przeprowadza pełną analizę dla wszystkich zbiorów, precyzji, metod i epsilonów.

    Parametry:
      datasets_dict : słownik ze zbiorami, np. {"A": pts_a, "B": pts_b, "C": pts_c, "D": pts_d}

    Zwraca:
      listę słowników z wynikami gotową do zamiany w pandas.DataFrame
    """
    all_results = []

    # Słownik do przechowywania indeksów spornych punktów (np. do wykresów różnic)
    disputed_points = {}

    for set_name, points in datasets_dict.items():
        print(f"--- Analiza zbioru {set_name} ---")
        for dtype in DTYPES:
            for eps in EPSILONS:
                current_labels = {}

                # 1. Wylicz klasyfikację dla każdej z 4 metod
                for method_name, det_func in METHODS.items():
                    labels = classify_dataset(
                        points, A_POINT, B_POINT, det_func, eps=eps, dtype=dtype
                    )
                    current_labels[method_name] = labels

                    stats = count_categories(labels)

                    record = {
                        "dataset": set_name,
                        "dtype": "float64" if dtype == np.float64 else "float32",
                        "epsilon": eps,
                        "method": method_name,
                        "left": stats["left"],
                        "right": stats["right"],
                        "collinear": stats["on"],
                    }

                    all_results.append(record)

                diff_count, diff_indices = find_differences(
                    current_labels["custom_3x3"], current_labels["custom_2x2"]
                )

                if diff_count > 0:
                    dtype_str = "float64" if dtype == np.float64 else "float32"
                    disputed_points[(set_name, dtype_str, eps)] = diff_indices
                    disputed_points[(set_name, dtype, eps)] = diff_indices
                    print(
                        f"[{set_name} | {dtype_str} | eps={eps}] Różnice 3x3 vs 2x2: {diff_count} punktów!"
                    )

    return all_results, disputed_points
