import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

POINTS_DIR = BASE_DIR / "points"
POINTS_DIR.mkdir(exist_ok=True)

FIGURES_DIR = BASE_DIR / "figures"
FIGURES_DIR.mkdir(exist_ok=True)


# =============================================================================
# WYZNACZNIKI
# =============================================================================


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


# =============================================================================
# GENEROWANIE ZBIORÓW
# =============================================================================


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


# =============================================================================
# KLASYFIKACJA
# =============================================================================

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


# =============================================================================
# BENCHMARK
# =============================================================================


def run_time_benchmark(sizes=[1000, 10_000, 50_000, 100_000], seed=42):
    """
    Porównuje czasy klasyfikacji dla różnych rozmiarów próbek (N)
    oraz różnych metod wyznaczników (zalecenie nr 6 z instrukcji).
    """
    print("\n" + "=" * 70)
    print("URUCHAMIANIE TESTÓW WYDAJNOŚCI CZASOWEJ (Benchmark)")
    print("=" * 70)

    # Generujemy zbiór o maksymalnym rozmiarze
    max_n = max(sizes)
    full_points = generate_setA(N=max_n, save=False, seed=seed)

    records = []

    for n in sizes:
        print(f"Testowanie dla N = {n:,} punktów...")
        pts_subset = full_points[:n]

        for method_name, det_func in METHODS.items():
            start_time = time.perf_counter()
            _ = classify_dataset(
                pts_subset,
                A_POINT,
                B_POINT,
                det_func,
                eps=1e-12,
                dtype=np.float64,
            )
            elapsed_time = time.perf_counter() - start_time

            records.append({
                "N": n,
                "Metoda": method_name,
                "Czas_sekundy": elapsed_time,
                "Czas_ms": elapsed_time * 1000.0,
            })

    df_benchmark = pd.DataFrame(records)
    df_benchmark.to_csv(BASE_DIR / "benchmark_results.csv", index=False)
    print("\n[INFO] Wyniki benchmarku zapisano w 'benchmark_results.csv'.")
    return df_benchmark


# =============================================================================
# WIZUALIZACJA
# =============================================================================

# Globalne ustawienia stylu dla krystalicznej czytelności
plt.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 15,
    "axes.labelsize": 13,
    "xtick.labelsize": 11.5,
    "ytick.labelsize": 11.5,
    "legend.fontsize": 12,
    "figure.titlesize": 16,
    "lines.linewidth": 2.2,
    "grid.alpha": 0.45,
    "grid.linestyle": "--",
})

# Standardowa paleta kolorów
COLOR_RAW = "#2ca02c"       # Czysta, naukowa zieleń (jak w raw_dataset.png)
COLOR_LEFT = "#1f77b4"      # Niebieski
COLOR_RIGHT = "#ff7f0e"     # Pomarańczowy
COLOR_COLLINEAR = "#2ca02c" # Zielony (współliniowy)
COLOR_LINE = "#d62728"      # Czerwona prosta


def draw_all_datasets(points_A, points_B, points_C, points_D):
    """Rysuje siatkę 2x2 prezentującą surowe zbiory danych (przed klasyfikacją)."""
    # Brak suptitle wewnątrz grafiki - maksymalne wykorzystanie powierzchni
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 10.5))

    # Zbiór A
    axes[0, 0].scatter(
        points_A[:, 0], points_A[:, 1], s=2.5, alpha=0.35, color=COLOR_RAW
    )
    axes[0, 0].set_title("Zbiór A", fontsize=15, fontweight="bold", pad=8)
    axes[0, 0].set_xlabel("X")
    axes[0, 0].set_ylabel("Y")
    axes[0, 0].grid(True)

    # Zbiór B
    axes[0, 1].scatter(
        points_B[:, 0], points_B[:, 1], s=2.5, alpha=0.35, color=COLOR_RAW
    )
    axes[0, 1].set_title("Zbiór B", fontsize=15, fontweight="bold", pad=8)
    axes[0, 1].set_xlabel("X")
    axes[0, 1].set_ylabel("Y")
    axes[0, 1].grid(True)

    # Zbiór C (wymagany aspekt 1:1)
    axes[1, 0].scatter(
        points_C[:, 0], points_C[:, 1], s=22, alpha=0.8, color=COLOR_RAW
    )
    axes[1, 0].set_title("Zbiór C", fontsize=15, fontweight="bold", pad=8)
    axes[1, 0].set_xlabel("X")
    axes[1, 0].set_ylabel("Y")
    axes[1, 0].set_aspect("equal", adjustable="box")
    axes[1, 0].grid(True)

    # Zbiór D
    axes[1, 1].scatter(
        points_D[:, 0], points_D[:, 1], s=20, alpha=0.8, color=COLOR_RAW
    )
    axes[1, 1].set_title("Zbiór D", fontsize=15, fontweight="bold", pad=8)
    axes[1, 1].set_xlabel("X")
    axes[1, 1].set_ylabel("Y")
    axes[1, 1].grid(True)

    plt.tight_layout()
    save_path = FIGURES_DIR / "raw_datasets.png"
    plt.savefig(save_path, dpi=400)
    plt.close()
    print(f"[WYKRES] Zapisano w wysokiej rozdzielczości 400 DPI: {save_path}")


def plot_all_classified_datasets(datasets, eps=1e-10):
    """
    Rysuje siatkę 2x2 z punktami pokolorowanymi wg klasyfikacji.
    Legenda umieszczona centralnie na samej górze figury, NIE zasłania żadnego wykresu!
    """
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 11.0))

    mapping = [
        ("A", axes[0, 0], "Zbiór A", 1.8, 0.35),
        ("B", axes[0, 1], "Zbiór B", 1.8, 0.35),
        ("C", axes[1, 0], "Zbiór C", 24, 0.8),
        ("D_kier", axes[1, 1], "Zbiór D", 24, 0.85),
    ]

    for key, ax, title, size, alpha in mapping:
        pts = datasets[key]
        labels = classify_dataset(pts, A_POINT, B_POINT, det_2x2_custom, eps=eps)

        left_mask = labels == 1
        right_mask = labels == -1
        on_mask = labels == 0

        # Rysowanie punktów
        if np.any(left_mask):
            ax.scatter(pts[left_mask, 0], pts[left_mask, 1], s=size, alpha=alpha, color=COLOR_LEFT, label="Lewo")
        if np.any(right_mask):
            ax.scatter(pts[right_mask, 0], pts[right_mask, 1], s=size, alpha=alpha, color=COLOR_RIGHT, label="Prawo")
        if np.any(on_mask):
            ax.scatter(pts[on_mask, 0], pts[on_mask, 1], s=size * 2.8, alpha=1.0, color=COLOR_COLLINEAR, label="Na prostej")

        # Dorysowanie linii prostej
        x_min, x_max = ax.get_xlim()
        x_vals = np.array([x_min, x_max])
        y_vals = 0.05 * x_vals + 0.05
        ax.plot(x_vals, y_vals, color=COLOR_LINE, linestyle="--", linewidth=2.0, label="Prosta AB")

        ax.set_title(title, fontsize=15, fontweight="bold", pad=8)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.grid(True)
        if key == "C":
            ax.set_aspect("equal", adjustable="box")

    # Tworzymy elegancką, wspólną poziomą legendę na samej górze figury (nie zasłania żadnego punktu!)
    handles, labels_text = axes[0, 0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels_text,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.99),
        ncol=4,
        fontsize=12.5,
        markerscale=3.5,
        framealpha=0.95,
        edgecolor="#aaaaaa",
    )

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    save_path = FIGURES_DIR / "classified_datasets.png"
    plt.savefig(save_path, dpi=400)
    plt.close()
    print(f"[WYKRES] Zapisano klasyfikację zbiorów (400 DPI): {save_path}")


def plot_set_b_anomalies(points_b, disputed_indices):
    """
    Wizualizuje punkty ze Zbioru B, które zostały fałszywie uznane za współliniowe.
    Wyraźnie oznacza i opisuje współrzędne punktów spornych w czytelnych ramkach.
    """
    fig, ax = plt.subplots(figsize=(11.5, 8.0))

    # Tło z próbką punktów
    sample_indices = np.random.choice(len(points_b), size=2000, replace=False)
    ax.scatter(
        points_b[sample_indices, 0],
        points_b[sample_indices, 1],
        s=3.0,
        color="#9ecae1",
        alpha=0.4,
        label="Próbka tła ze Zbioru B (2 000 pkt)",
        zorder=1,
    )

    # Rysujemy prostą AB
    x_span = np.array([-1e14, 1e14])
    ax.plot(x_span, 0.05 * x_span + 0.05, color=COLOR_LINE, linestyle="--", linewidth=1.5, label="Prosta AB", zorder=2)

    # Większe odstępy dla etykiet, aby były odsunięte od punktów i nie zasłaniały wykresu
    label_offsets = {
        0: (3.5e13, 3.0e13),
        1: (3.5e13, -4.5e13),
    }

    for i, idx in enumerate(disputed_indices):
        pt = points_b[idx]
        d3 = det_3x3_custom(A_POINT, B_POINT, pt, np.float64)
        d2 = det_2x2_custom(A_POINT, B_POINT, pt, np.float64)

        ax.scatter(
            pt[0],
            pt[1],
            s=280,
            color="#e31a1c",
            marker="*",
            edgecolor="black",
            linewidth=1.6,
            zorder=6,
            label="Punkt sporny (błędne det_2x2 = 0.0)" if i == 0 else None,
        )

        dx, dy = label_offsets.get(i, (2e13, 2e13))
        text_content = (
            f"PUNKT #{idx}\n"
            f"X = {pt[0]:.4e}, Y = {pt[1]:.4e}\n"
            f"det_2x2 = {d2:.1f} (Błędnie: ON)\n"
            f"det_3x3 = {d3:.2e} ({'LEWO' if d3 > 0 else 'PRAWO'})"
        )

        ax.annotate(
            text_content,
            xy=(pt[0], pt[1]),
            xytext=(pt[0] + dx, pt[1] + dy),
            arrowprops=dict(
                facecolor="black",
                edgecolor="black",
                shrink=0.1,
                width=2.0,
                headwidth=10,
                headlength=10,
            ),
            fontsize=12,
            fontweight="bold",
            fontfamily="monospace",
            bbox=dict(
                boxstyle="round,pad=0.8",
                facecolor="white",
                edgecolor="#b2182b",
                alpha=0.98,
                linewidth=2.0,
            ),
            zorder=7,
        )

    ax.set_xlabel("Współrzędna X (skala 10^14)", fontsize=13)
    ax.set_ylabel("Współrzędna Y (skala 10^14)", fontsize=13)
    ax.set_title("Fałszywie oznaczone punkty na prostej w Zbiorze B", fontsize=14, fontweight="bold", pad=12)
    ax.grid(True)
    ax.legend(loc="upper left", fontsize=11.5, framealpha=0.95)

    plt.tight_layout()
    save_path = FIGURES_DIR / "set_b_anomalies.png"
    plt.savefig(save_path, dpi=400)
    plt.close()
    print(f"[WYKRES] Zapisano w wysokiej rozdzielczości 400 DPI: {save_path}")


def plot_benchmark_chart(benchmark_df):
    """
    Rysuje wykres zależności czasu obliczeń od liczby punktów N (zalecenie nr 6).
    """
    fig, ax = plt.subplots(figsize=(10.5, 6.2))

    methods = benchmark_df["Metoda"].unique()
    colors = {
        "custom_2x2": "#2ca02c",  # Zielony
        "custom_3x3": "#1f77b4",  # Niebieski
        "numpy_2x2": "#d62728",   # Czerwony
        "numpy_3x3": "#ff7f0e",   # Pomarańczowy
    }

    for method in methods:
        sub = benchmark_df[benchmark_df["Metoda"] == method]
        ax.plot(
            sub["N"],
            sub["Czas_sekundy"],
            linewidth=2.8,
            color=colors.get(method, "black"),
            label=f"Metoda: {method}",
        )

    ax.set_xlabel("Liczba punktów (N)", fontsize=13)
    ax.set_ylabel("Czas wykonania [sekundy]", fontsize=13)
    ax.set_title("Porównanie efektywności czasowej wyznaczników", fontsize=14, fontweight="bold", pad=12)
    ax.grid(True)
    ax.legend(loc="upper left", fontsize=12, framealpha=0.95)

    plt.tight_layout()
    save_path = FIGURES_DIR / "benchmark_times.png"
    plt.savefig(save_path, dpi=400)
    plt.close()
    print(f"[WYKRES] Zapisano w wysokiej rozdzielczości 400 DPI: {save_path}")


# =============================================================================
# ANALIZA I PROGRAM GŁÓWNY
# =============================================================================


def analyze_set_b_disputed(points_b, disputed_indices):
    """
    Bada punkty ze Zbioru B, co do których metody 3x3 i 2x2 się nie zgodziły (Uwaga szczegółowa 3).
    """
    print("\n" + "=" * 70)
    print("SZCZEGÓŁOWA ANALIZA SPORNYCH PUNKTÓW ZE ZBIORU B (Uwaga szczegółowa 3)")
    print("=" * 70)

    # Punkty prostej leżące na TEJ SAMEJ prostej y = 0.05x + 0.05, ale w skali 10^14
    scale = 1e14
    a_scaled = [-scale, 0.05 * (-scale) + 0.05]
    b_scaled = [scale, 0.05 * scale + 0.05]

    for idx in disputed_indices:
        pt = points_b[idx]
        print(f"\n[Punkt nr {idx}]")
        print(f"  Współrzędne punktu: X = {pt[0]:.6e}, Y = {pt[1]:.6e}")

        # Obliczenia ze standardowym wektorem
        d3 = det_3x3_custom(A_POINT, B_POINT, pt, dtype=np.float64)
        d2 = det_2x2_custom(A_POINT, B_POINT, pt, dtype=np.float64)
        print(f"  Standardowy wektor a=[-1, 0], b=[1, 0.1]:")
        print(f"    det_3x3 = {d3} -> klasyfikacja: {'NA PROSTEJ (0)' if d3 == 0 else ('LEWO (1)' if d3 > 0 else 'PRAWO (-1)')}")
        print(f"    det_2x2 = {d2} -> klasyfikacja: {'NA PROSTEJ (0)' if d2 == 0 else ('LEWO (1)' if d2 > 0 else 'PRAWO (-1)')}")

        # Obliczenia z przeskalowanym wektorem
        d3_sc = det_3x3_custom(a_scaled, b_scaled, pt, dtype=np.float64)
        d2_sc = det_2x2_custom(a_scaled, b_scaled, pt, dtype=np.float64)
        print(f"  Przeskalowany wektor (* 10^14):")
        print(f"    det_3x3 = {d3_sc:.6e} -> klasyfikacja: {'NA PROSTEJ (0)' if d3_sc == 0 else ('LEWO (1)' if d3_sc > 0 else 'PRAWO (-1)')}")
        print(f"    det_2x2 = {d2_sc:.6e} -> klasyfikacja: {'NA PROSTEJ (0)' if d2_sc == 0 else ('LEWO (1)' if d2_sc > 0 else 'PRAWO (-1)')}")


def main():
    print("=" * 70)
    print("KOMPLEKSOWY PROGRAM ANALIZY GEOMETRYCZNEJ (Ćwiczenie 1)")
    print("=" * 70)

    # 1. Generowanie zbiorów punktów
    print("\n[KROK 1] Generowanie zbiorów punktów...")
    datasets = {
        "A": generate_setA(),
        "B": generate_setB(),
        "C": generate_setC(),
        "D_kier": generate_setD(),
        "D_param": generate_setD_parametric(),
    }

    # 2. Eksperyment klasyfikacyjny
    print("\n[KROK 2] Klasyfikacja punktów (4 metody x różne epsilony x 2 precyzje)...")
    results, disputed = run_experiments(datasets)
    df = pd.DataFrame(results)
    df.to_csv(BASE_DIR / "classifier_results.csv", index=False)
    print("\n[INFO] Pełną tabelę wyników zapisano w: 'classifier_results.csv'")

    # 3. Analiza spornych punktów ze Zbioru B
    disputed_indices_b = []
    key_b = ("B", "float64", 0.0)
    if key_b in disputed:
        disputed_indices_b = disputed[key_b]
        analyze_set_b_disputed(datasets["B"], disputed_indices_b)
    elif ("B", np.float64, 0.0) in disputed:
        disputed_indices_b = disputed[("B", np.float64, 0.0)]
        analyze_set_b_disputed(datasets["B"], disputed_indices_b)

    # 4. Generowanie wszystkich wykresów do sprawozdania
    print("\n[KROK 3] Generowanie wykresów do sprawozdania (wysoka rozdzielczość 400 DPI w folderze figures/)...")
    draw_all_datasets(datasets["A"], datasets["B"], datasets["C"], datasets["D_kier"])
    plot_all_classified_datasets(datasets, eps=1e-10)
    if len(disputed_indices_b) > 0:
        plot_set_b_anomalies(datasets["B"], disputed_indices_b)

    # 5. Pomiary czasowe (zalecenie nr 6 z instrukcji)
    print("\n[KROK 4] Przeprowadzanie benchmarku wydajności czasowej...")
    benchmark_df = run_time_benchmark(sizes=[1000, 10_000, 50_000, 100_000])
    plot_benchmark_chart(benchmark_df)

    print("\n" + "=" * 70)
    print("PROCES ZAKOŃCZONY SUKCESEM!")
    print("Wszystkie dane liczbowe (classifier_results.csv, benchmark_results.csv)")
    print("oraz wszystkie 4 wykresy (w folderze figures/) są gotowe do wklejenia do sprawozdania.")
    print("=" * 70)


if __name__ == "__main__":
    main()
