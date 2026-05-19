"""Escenarios predefinidos para comparar algoritmos de planificacion."""

from typing import Dict, List, TypedDict


class Scenario(TypedDict):
    """Datos necesarios para ejecutar un escenario de simulacion."""

    disk_size: int
    head: int
    requests: List[int]
    direction: str
    description: str


def get_predefined_scenarios() -> Dict[str, Scenario]:
    """Retorna escenarios representativos para comparacion academica."""
    return {
        "Caso clasico": {
            "disk_size": 200,
            "head": 53,
            "requests": [98, 183, 37, 122, 14, 124, 65, 67],
            "direction": "right",
            "description": "Escenario de referencia para validar resultados.",
        },
        "Solicitudes agrupadas cerca del cabezal": {
            "disk_size": 200,
            "head": 100,
            "requests": [95, 98, 102, 105, 110, 90, 88, 115],
            "direction": "right",
            "description": "Muestra el comportamiento cuando hay alta localidad espacial.",
        },
        "Solicitudes dispersas": {
            "disk_size": 200,
            "head": 50,
            "requests": [5, 180, 20, 175, 60, 150, 10, 190],
            "direction": "right",
            "description": "Evidencia el costo de mover el cabezal entre cilindros alejados.",
        },
        "Cabezal cerca del extremo izquierdo": {
            "disk_size": 200,
            "head": 10,
            "requests": [15, 35, 80, 120, 160, 190, 5, 45],
            "direction": "right",
            "description": "Permite analizar el efecto de iniciar cerca de un borde del disco.",
        },
        "Cabezal cerca del extremo derecho": {
            "disk_size": 200,
            "head": 185,
            "requests": [180, 160, 140, 100, 60, 30, 10, 195],
            "direction": "left",
            "description": "Permite analizar el inicio cerca del extremo superior del disco.",
        },
        "Solicitudes cargadas hacia un solo lado": {
            "disk_size": 200,
            "head": 40,
            "requests": [80, 95, 110, 125, 140, 155, 170, 185],
            "direction": "right",
            "description": "Muestra si el algoritmo aprovecha solicitudes en una misma direccion.",
        },
    }
