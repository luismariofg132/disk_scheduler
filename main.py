"""Interfaz principal del simulador de planificacion de E/S en disco."""

import argparse
import ast
import os
from typing import List

os.environ.setdefault(
    "MPLCONFIGDIR",
    os.path.join(os.path.dirname(__file__), ".matplotlib_cache"),
)

import matplotlib.pyplot as plt
from tabulate import tabulate

from algorithms import DiskResult, c_scan, fcfs, scan, sstf, validate_disk_input
from exporter import export_to_csv, export_to_json
from visualization import (
    plot_average_time_bars,
    plot_comparison,
    plot_movement,
    plot_total_distance_bars,
)


def parse_requests(raw_value: str) -> List[int]:
    """Convierte una entrada tipo '[1, 2, 3]' o '1,2,3' en lista de enteros."""
    value = raw_value.strip()
    if not value:
        raise ValueError("La lista de solicitudes no puede estar vacia.")

    if value.startswith("["):
        parsed = ast.literal_eval(value)
        if not isinstance(parsed, list):
            raise ValueError("La entrada debe ser una lista de cilindros.")
        requests = parsed
    else:
        requests = [item.strip() for item in value.split(",")]

    try:
        return [int(request) for request in requests]
    except (TypeError, ValueError) as exc:
        raise ValueError("Todas las solicitudes deben ser numeros enteros.") from exc


def read_int(prompt: str) -> int:
    """Lee un entero desde consola y repite hasta recibir un valor valido."""
    while True:
        raw_value = input(prompt).strip()
        try:
            return int(raw_value)
        except ValueError:
            print("Entrada invalida. Ingresa un numero entero.")


def read_direction() -> str:
    """Lee y valida la direccion inicial para SCAN y C-SCAN."""
    while True:
        direction = input("Direccion inicial para SCAN/C-SCAN (left/right): ").strip().lower()
        if direction in ("left", "right"):
            return direction
        print('Direccion invalida. Debe ser "left" o "right".')


def read_requests() -> List[int]:
    """Lee la lista de solicitudes desde consola."""
    while True:
        raw_requests = input("Lista de solicitudes, ejemplo [98, 183, 37]: ")
        try:
            return parse_requests(raw_requests)
        except ValueError as error:
            print(f"Entrada invalida. {error}")


def read_interactive_input() -> tuple[int, int, List[int], str]:
    """Solicita al usuario todos los datos necesarios para la simulacion."""
    while True:
        disk_size = read_int("Tamano del disco, ejemplo 200: ")
        head = read_int("Posicion inicial del cabezal: ")
        requests = read_requests()
        direction = read_direction()

        try:
            validate_disk_input(requests, head, disk_size, direction)
            return disk_size, head, requests, direction
        except ValueError as error:
            print(f"Datos invalidos: {error}")
            print("Vuelve a ingresar el caso de simulacion.\n")


def example_input() -> tuple[int, int, List[int], str]:
    """Retorna los datos de prueba clasicos del problema."""
    return 200, 53, [98, 183, 37, 122, 14, 124, 65, 67], "right"


def run_algorithms(
    requests: List[int],
    head: int,
    disk_size: int,
    direction: str,
) -> List[DiskResult]:
    """Ejecuta todos los algoritmos y retorna sus resultados."""
    validate_disk_input(requests, head, disk_size, direction)
    return [
        fcfs(requests, head),
        sstf(requests, head),
        scan(requests, head, disk_size, direction),
        c_scan(requests, head, disk_size, direction),
    ]


def get_best_algorithm(results: List[DiskResult]) -> DiskResult:
    """Determina el algoritmo mas eficiente por menor distancia total."""
    return min(results, key=lambda result: result["total_distance"])


def print_results_table(results: List[DiskResult]) -> None:
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
                "Secuencia de atencion",
                "Distancia total",
                "Tiempo promedio",
            ],
            tablefmt="grid",
        )
    )


def explain_best_algorithm(results: List[DiskResult]) -> None:
    """Imprime una explicacion breve del algoritmo mas eficiente."""
    best = get_best_algorithm(results)
    print()
    print(
        "Para este caso, el algoritmo mas eficiente fue "
        f"{best['algorithm']} porque recorrio la menor distancia total: "
        f"{best['total_distance']} cilindros."
    )
    print(
        "Menor distancia implica menor seek time acumulado, ya que el cabezal "
        "realiza menos movimiento fisico para atender las solicitudes."
    )


def export_results(results: List[DiskResult], export_choice: str) -> None:
    """Exporta resultados segun la opcion seleccionada."""
    output_dir = os.path.join(os.path.dirname(__file__), "exports")

    if export_choice in ("csv", "both"):
        csv_path = export_to_csv(results, os.path.join(output_dir, "results.csv"))
        print(f"Resultados CSV exportados en: {csv_path}")

    if export_choice in ("json", "both"):
        json_path = export_to_json(results, os.path.join(output_dir, "results.json"))
        print(f"Resultados JSON exportados en: {json_path}")

    if export_choice not in ("none", "csv", "json", "both", ""):
        print("Opcion de exportacion no reconocida. No se exportaron resultados.")


def ask_export_results(results: List[DiskResult]) -> None:
    """Pregunta si se desean exportar los resultados a CSV o JSON."""
    export_choice = input("Deseas exportar resultados? (none/csv/json/both): ").strip().lower()
    export_results(results, export_choice)


def show_plots(results: List[DiskResult]) -> None:
    """Genera las graficas individuales y comparativas."""
    for result in results:
        plot_movement(result)
    plot_comparison(results)
    plot_total_distance_bars(results)
    plot_average_time_bars(results)
    plt.show()


def build_parser() -> argparse.ArgumentParser:
    """Crea el parser de argumentos de linea de comandos."""
    parser = argparse.ArgumentParser(description="Simulador de planificacion de E/S en disco")
    parser.add_argument(
        "--example",
        action="store_true",
        help="Ejecuta directamente el caso de prueba sugerido.",
    )
    parser.add_argument(
        "--no-plots",
        action="store_true",
        help="Ejecuta la simulacion sin abrir graficas.",
    )
    parser.add_argument(
        "--no-export-prompt",
        action="store_true",
        help="No pregunta por exportacion al finalizar.",
    )
    parser.add_argument(
        "--export",
        choices=["none", "csv", "json", "both"],
        help="Exporta resultados sin preguntar.",
    )
    return parser


def main() -> None:
    """Punto de entrada del programa."""
    args = build_parser().parse_args()

    print("Simulador de planificacion de E/S en disco")
    if args.example:
        disk_size, head, requests, direction = example_input()
    else:
        disk_size, head, requests, direction = read_interactive_input()

    results = run_algorithms(requests, head, disk_size, direction)

    print()
    print(f"Tamano del disco: cilindros 0 a {disk_size - 1}")
    print(f"Posicion inicial del cabezal: {head}")
    print(f"Solicitudes: {requests}")
    print(f"Direccion inicial para SCAN/C-SCAN: {direction}")
    print()

    print_results_table(results)
    explain_best_algorithm(results)
    print()

    if args.export:
        export_results(results, args.export)
    elif not args.no_export_prompt:
        ask_export_results(results)

    if not args.no_plots:
        show_plots(results)


if __name__ == "__main__":
    main()
