import matplotlib.pyplot as plt
from pathlib import Path

FIGURES_DIR = Path(__file__).resolve().parent.parent / "figures"


def draw_all_datasets(points_A, points_B, points_C, points_D):
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(
        "Wizualizacja wygenerowanych zbiorów punktów", fontsize=16, fontweight="bold"
    )

    # Wykres points_A
    axes[0, 0].scatter(
        points_A[:, 0], points_A[:, 1], s=1.5, alpha=0.25, color="#2ca02c"
    )
    axes[0, 0].set_title(r"Zbiór A: $10^5$ punktów w $[-1000, 1000]^2$")
    axes[0, 0].set_xlabel("X")
    axes[0, 0].set_ylabel("Y")
    axes[0, 0].grid(True, linestyle="--", alpha=0.5)

    # Wykres points_B
    axes[0, 1].scatter(
        points_B[:, 0], points_B[:, 1], s=1.5, alpha=0.25, color="#2ca02c"
    )
    axes[0, 1].set_title(r"Zbiór B: $10^5$ punktów w $[-1e14, 1e14]^2$")
    axes[0, 1].set_xlabel("X")
    axes[0, 1].set_ylabel("Y")
    axes[0, 1].grid(True, linestyle="--", alpha=0.5)

    # Wykres points_C
    axes[1, 0].scatter(
        points_C[:, 0], points_C[:, 1], s=10, alpha=0.60, color="#2ca02c"
    )
    axes[1, 0].set_title(r"Zbiór C: 1000 punktów na okręgu S=(0,0), R=100")
    axes[1, 0].set_xlabel("X")
    axes[1, 0].set_ylabel("Y")
    axes[1, 0].grid(True, linestyle="--", alpha=0.5)

    # Wykres points_D
    axes[1, 1].scatter(
        points_D[:, 0], points_D[:, 1], s=10, alpha=0.50, color="#2ca02c"
    )
    axes[1, 1].set_title(r"Zbiór D: 1000 punktów na prostej $y = 0.05x + 0.05$")
    axes[1, 1].set_xlabel("X")
    axes[1, 1].set_ylabel("Y")
    axes[1, 1].grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    save_path = FIGURES_DIR / "raw_dataset.png"
    plt.savefig(save_path, dpi=300)
    plt.show()
