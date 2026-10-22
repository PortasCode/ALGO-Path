import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from src.classifier import A_POINT, B_POINT, classify_dataset
from src.determinant import det_2x2_custom, det_3x3_custom

FIGURES_DIR = Path(__file__).resolve().parent.parent / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

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
