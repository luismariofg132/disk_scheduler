"""Funciones de visualizacion para el movimiento del cabezal.
Este módulo genera gráficas para:
- Movimiento del cabezal.
- Comparación entre algoritmos.
- Distancia total recorrida.
- Tiempo promedio de acceso.
- Comparación de escenarios."""

# IMPORTACIONES
import os
from collections import Counter
from typing import Iterable, List, Mapping

os.environ.setdefault(
    "MPLCONFIGDIR",
    os.path.join(os.path.dirname(__file__), ".matplotlib_cache"),
)

# Configuración de caché de matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from algorithms import DiskResult


# Tipo auxiliar para métricas de escenarios
ScenarioMetric = Mapping[str, object]


# MOVIMIENTO INDIVIDUAL
def plot_movement(result: DiskResult) -> Figure:
    """Grafica la secuencia de movimiento de un algoritmo y retorna la figura."""
    sequence = result["sequence"]
    steps = list(range(len(sequence)))

    fig, axis = plt.subplots(figsize=(9, 5))
    axis.plot(steps, sequence, marker="o", linewidth=2)
    axis.set_title(f"Movimiento del cabezal - {result['algorithm']}")
    axis.set_xlabel("Paso / tiempo")
    axis.set_ylabel("Cilindro")
    axis.grid(True, linestyle="--", alpha=0.6)
    axis.set_xticks(steps)
    fig.tight_layout()
    return fig


# COMPARACIÓN GENERAL
def plot_comparison(results: Iterable[DiskResult]) -> Figure:
    """Muestra los cuatro algoritmos en subgraficas y retorna la figura."""
    result_list = list(results)
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()

    for axis, result in zip(axes, result_list):
        sequence = result["sequence"]
        steps = list(range(len(sequence)))
        axis.plot(steps, sequence, marker="o", linewidth=2)
        axis.set_title(result["algorithm"])
        axis.set_xlabel("Paso / tiempo")
        axis.set_ylabel("Cilindro")
        axis.grid(True, linestyle="--", alpha=0.6)
        axis.set_xticks(steps)

    fig.suptitle("Comparacion de algoritmos de planificacion de disco")
    fig.tight_layout()
    return fig

# DISTANCIA TOTAL
def plot_total_distance_bars(results: Iterable[DiskResult]) -> Figure:
    """Grafica barras de distancia total y retorna la figura."""
    result_list = list(results)
    algorithms = _algorithm_names(result_list)
    distances = [result["total_distance"] for result in result_list]

    fig, axis = plt.subplots(figsize=(9, 5))
    axis.bar(algorithms, distances, color=["#4C78A8", "#F58518", "#54A24B", "#B279A2"])
    axis.set_title("Comparacion de distancia total")
    axis.set_xlabel("Algoritmo")
    axis.set_ylabel("Distancia total recorrida")
    axis.grid(axis="y", linestyle="--", alpha=0.6)
    fig.tight_layout()
    return fig

# TIEMPO PROMEDIO
def plot_average_time_bars(results: Iterable[DiskResult]) -> Figure:
    """Grafica barras de tiempo promedio de acceso y retorna la figura."""
    result_list = list(results)
    algorithms = _algorithm_names(result_list)
    averages = [result["average_access_time"] for result in result_list]

    fig, axis = plt.subplots(figsize=(9, 5))
    axis.bar(algorithms, averages, color=["#4C78A8", "#F58518", "#54A24B", "#B279A2"])
    axis.set_title("Comparacion de tiempo promedio de acceso")
    axis.set_xlabel("Algoritmo")
    axis.set_ylabel("Tiempo promedio de acceso")
    axis.grid(axis="y", linestyle="--", alpha=0.6)
    fig.tight_layout()
    return fig


# ESCENARIOS
def plot_scenario_distance_comparison(scenario_results: Iterable[ScenarioMetric]) -> Figure:
    """Grafica distancia total por escenario con barras agrupadas por algoritmo."""
    return _plot_grouped_scenario_bars(
        scenario_results,
        metric_key="total_distance",
        title="Distancia total por escenario",
        ylabel="Distancia total recorrida",
    )


def plot_scenario_average_time_comparison(scenario_results: Iterable[ScenarioMetric]) -> Figure:
    """Grafica tiempo promedio por escenario con barras agrupadas por algoritmo."""
    return _plot_grouped_scenario_bars(
        scenario_results,
        metric_key="average_access_time",
        title="Tiempo promedio por escenario",
        ylabel="Tiempo promedio de acceso",
    )


# GANADORES
def plot_algorithm_wins(winners: Iterable[Mapping[str, object]]) -> Figure:
    """Grafica cuantas veces gano cada algoritmo en los escenarios evaluados."""
    winner_list = list(winners)
    win_counts = Counter(str(winner["Mejor algoritmo"]) for winner in winner_list)
    algorithms = ["FCFS", "SSTF", "SCAN", "C-SCAN"]
    counts = [win_counts.get(algorithm, 0) for algorithm in algorithms]

    fig, axis = plt.subplots(figsize=(8, 5))
    axis.bar(algorithms, counts, color=["#4C78A8", "#F58518", "#54A24B", "#B279A2"])
    axis.set_title("Ganadores por escenario")
    axis.set_xlabel("Algoritmo")
    axis.set_ylabel("Cantidad de escenarios ganados")
    axis.set_ylim(0, max(counts + [1]))
    axis.grid(axis="y", linestyle="--", alpha=0.6)
    fig.tight_layout()
    return fig


# FUNCIONES AUXILIARES
def _algorithm_names(results: List[DiskResult]) -> List[str]:
    """Extrae los nombres de algoritmos para las graficas comparativas."""
    return [result["algorithm"] for result in results]


def _plot_grouped_scenario_bars(
    scenario_results: Iterable[ScenarioMetric],
    metric_key: str,
    title: str,
    ylabel: str,
) -> Figure:
    """Construye una grafica de barras agrupadas para metricas por escenario."""
    result_list = list(scenario_results)
    scenarios = list(dict.fromkeys(str(result["scenario"]) for result in result_list))
    algorithms = ["FCFS", "SSTF", "SCAN", "C-SCAN"]
    x_positions = list(range(len(scenarios)))
    width = 0.18
    offsets = [-1.5 * width, -0.5 * width, 0.5 * width, 1.5 * width]
    colors = ["#4C78A8", "#F58518", "#54A24B", "#B279A2"]

    fig, axis = plt.subplots(figsize=(12, 6))

    # Crea barras para cada algoritmo
    for algorithm, offset, color in zip(algorithms, offsets, colors):
        values = [
            _metric_for(result_list, scenario, algorithm, metric_key)
            for scenario in scenarios
        ]
        axis.bar(
            [position + offset for position in x_positions],
            values,
            width=width,
            label=algorithm,
            color=color,
        )

    axis.set_title(title)
    axis.set_xlabel("Escenario")
    axis.set_ylabel(ylabel)
    axis.set_xticks(x_positions)
    axis.set_xticklabels(scenarios, rotation=25, ha="right")
    axis.legend()
    axis.grid(axis="y", linestyle="--", alpha=0.6)
    fig.tight_layout()
    return fig


def _metric_for(
    scenario_results: List[ScenarioMetric],
    scenario: str,
    algorithm: str,
    metric_key: str,
) -> float:
    """Busca una metrica para un par escenario-algoritmo."""
    for result in scenario_results:
        if result["scenario"] == scenario and result["algorithm"] == algorithm:
            return float(result[metric_key])
    return 0.0
