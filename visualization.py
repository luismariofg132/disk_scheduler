"""Funciones de visualizacion para el movimiento del cabezal."""

import os
from typing import Iterable, List

os.environ.setdefault(
    "MPLCONFIGDIR",
    os.path.join(os.path.dirname(__file__), ".matplotlib_cache"),
)

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from algorithms import DiskResult


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


def _algorithm_names(results: List[DiskResult]) -> List[str]:
    """Extrae los nombres de algoritmos para las graficas comparativas."""
    return [result["algorithm"] for result in results]
