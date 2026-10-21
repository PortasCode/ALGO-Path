import time
import numpy as np
import pandas as pd
from src.classifier import A_POINT, B_POINT, classify_dataset, METHODS
from src.generowanie_zbiorow import generate_setA


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
    df_benchmark.to_csv("benchmark_results.csv", index=False)
    print("\n[INFO] Wyniki benchmarku zapisano w 'benchmark_results.csv'.")
    return df_benchmark
