"""Simulador de planificacion de E/S en disco."""

import os

os.environ.setdefault(
    "MPLCONFIGDIR",
    os.path.join(os.path.dirname(__file__), ".matplotlib_cache"),
)

from tabulate import tabulate
import matplotlib.pyplot as plt

from algorithms import c_scan, fcfs, scan, sstf, validate_disk_input
from visualization import plot_comparison, plot_movement


def print_results_table(results):
    """Imprime una tabla comparativa con las metricas principales."""
    table = [
        [
            result["algorithm"],
            result["sequence"],
            result["total_distance"],
            f"{result['average_access_time']:.2f}",
        ]
        for result in results
    ]

    print(
        tabulate(
            table,
            headers=[
                "Algoritmo",
                "Secuencia",
                "Distancia total",
                "Tiempo promedio",
            ],
            tablefmt="grid",
        )
    )


def explain_best_algorithm(results):
    """Indica el algoritmo mas eficiente segun la distancia total recorrida."""
    best = min(results, key=lambda result: result["total_distance"])
    print()
    print(
        "Para este caso de prueba, el algoritmo mas eficiente fue "
        f"{best['algorithm']} porque recorrio la menor distancia total: "
        f"{best['total_distance']} cilindros."
    )
    print(
        "Menor distancia implica menor seek time acumulado, ya que el cabezal "
        "realiza menos movimiento fisico para atender las solicitudes."
    )


def main():
    # Datos de prueba sugeridos para la exposicion academica.
    disk_size = 200
    head = 53
    requests = [98, 183, 37, 122, 14, 124, 65, 67]
    direction = "right"

    validate_disk_input(requests, head, disk_size, direction)

    results = [
        fcfs(requests, head),
        sstf(requests, head),
        scan(requests, head, disk_size, direction),
        c_scan(requests, head, disk_size, direction),
    ]

    print("Simulador de planificacion de E/S en disco")
    print(f"Tamano del disco: cilindros 0 a {disk_size - 1}")
    print(f"Posicion inicial del cabezal: {head}")
    print(f"Solicitudes: {requests}")
    print(f"Direccion inicial para SCAN/C-SCAN: {direction}")
    print()

    print_results_table(results)
    explain_best_algorithm(results)

    for result in results:
        plot_movement(result)
    plot_comparison(results)
    plt.show()


if __name__ == "__main__":
    main()
