"""Funciones de visualizacion para el movimiento del cabezal."""

import os

os.environ.setdefault(
    "MPLCONFIGDIR",
    os.path.join(os.path.dirname(__file__), ".matplotlib_cache"),
)

import matplotlib.pyplot as plt


def plot_movement(result):
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


def plot_comparison(results):
    """Muestra los cuatro algoritmos en subgraficas para compararlos."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()

    for axis, result in zip(axes, results):
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
