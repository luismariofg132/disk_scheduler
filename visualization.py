"""Funciones de visualizacion para el movimiento del cabezal."""

import os
from typing import Iterable, List

os.environ.setdefault(
    "MPLCONFIGDIR",
    os.path.join(os.path.dirname(__file__), ".matplotlib_cache"),
)

import matplotlib.pyplot as plt

from algorithms import DiskResult


def plot_movement(result: DiskResult) -> None:
    """Grafica la secuencia de movimiento de un algoritmo."""
    sequence = result["sequence"]
    steps = list(range(len(sequence)))

    plt.figure(figsize=(9, 5))
    plt.plot(steps, sequence, marker="o", linewidth=2)
    plt.title(f"Movimiento del cabezal - {result['algorithm']}")
    plt.xlabel("Paso / tiempo")
    plt.ylabel("Cilindro")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.xticks(steps)
    plt.tight_layout()


def plot_comparison(results: Iterable[DiskResult]) -> None:
    """Muestra los cuatro algoritmos en subgraficas para compararlos."""
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


def plot_total_distance_bars(results: Iterable[DiskResult]) -> None:
    """Grafica una comparacion de barras de la distancia total recorrida."""
    result_list = list(results)
    algorithms = _algorithm_names(result_list)
    distances = [result["total_distance"] for result in result_list]

    plt.figure(figsize=(9, 5))
    plt.bar(algorithms, distances, color=["#4C78A8", "#F58518", "#54A24B", "#B279A2"])
    plt.title("Comparacion de distancia total")
    plt.xlabel("Algoritmo")
    plt.ylabel("Distancia total recorrida")
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()


def plot_average_time_bars(results: Iterable[DiskResult]) -> None:
    """Grafica una comparacion de barras del tiempo promedio de acceso."""
    result_list = list(results)
    algorithms = _algorithm_names(result_list)
    averages = [result["average_access_time"] for result in result_list]

    plt.figure(figsize=(9, 5))
    plt.bar(algorithms, averages, color=["#4C78A8", "#F58518", "#54A24B", "#B279A2"])
    plt.title("Comparacion de tiempo promedio de acceso")
    plt.xlabel("Algoritmo")
    plt.ylabel("Tiempo promedio de acceso")
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()


def _algorithm_names(results: List[DiskResult]) -> List[str]:
    """Extrae los nombres de algoritmos para las graficas comparativas."""
    return [result["algorithm"] for result in results]
