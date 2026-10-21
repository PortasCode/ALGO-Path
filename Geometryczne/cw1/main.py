import numpy as np
import pandas as pd
from src.classifier import A_POINT, B_POINT, run_experiments
from src.determinant import det_2x2_custom, det_3x3_custom
from src.benchmark import run_time_benchmark
from src import generowanie_zbiorow as gen
from src import visualizer as vis


def analyze_set_b_disputed(points_b, disputed_indices):
    """
    Bada punkty ze Zbioru B, co do których metody 3x3 i 2x2 się nie zgodziły (Uwaga szczegółowa 3).
    """
    print("\n" + "=" * 70)
    print("SZCZEGÓŁOWA ANALIZA SPORNYCH PUNKTÓW ZE ZBIORU B (Uwaga szczegółowa 3)")
    print("=" * 70)

    # Przeskalowany wektor prostej (mnożymy współrzędne przez 10^14)
    scale = 1e14
    a_scaled = [A_POINT[0] * scale, A_POINT[1] * scale]
    b_scaled = [B_POINT[0] * scale, B_POINT[1] * scale]

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
        "A": gen.generate_setA(),
        "B": gen.generate_setB(),
        "C": gen.generate_setC(),
        "D_kier": gen.generate_setD(),
        "D_param": gen.generate_setD_parametric(),
    }

    # 2. Eksperyment klasyfikacyjny
    print("\n[KROK 2] Klasyfikacja punktów (4 metody x różne epsilony x 2 precyzje)...")
    results, disputed = run_experiments(datasets)
    df = pd.DataFrame(results)
    df.to_csv("classifier_results.csv", index=False)
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
    print("\n[KROK 3] Generowanie wykresów do sprawozdania (jakość 300 DPI w folderze figures/)...")
    vis.draw_all_datasets(datasets["A"], datasets["B"], datasets["C"], datasets["D_kier"])
    vis.plot_all_classified_datasets(datasets, eps=1e-10)
    vis.plot_differences_set_d(datasets["D_kier"])
    if len(disputed_indices_b) > 0:
        vis.plot_set_b_anomalies(datasets["B"], disputed_indices_b)

    # 5. Pomiary czasowe (zalecenie nr 6 z instrukcji)
    print("\n[KROK 4] Przeprowadzanie benchmarku wydajności czasowej...")
    benchmark_df = run_time_benchmark(sizes=[1000, 10_000, 50_000, 100_000])
    vis.plot_benchmark_chart(benchmark_df)

    print("\n" + "=" * 70)
    print("PROCES ZAKOŃCZONY SUKCESEM!")
    print("Wszystkie dane liczbowe (classifier_results.csv, benchmark_results.csv)")
    print("oraz wszystkie 5 wykresów (w folderze figures/) są gotowe do wklejenia do sprawozdania.")
    print("=" * 70)


if __name__ == "__main__":
    main()
