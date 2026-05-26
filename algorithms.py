"""Algoritmos de planificacion de E/S en disco.

El simulador se enfoca en el seek time: la distancia que recorre el cabezal
entre cilindros. Cada algoritmo retorna la secuencia completa de movimiento,
incluyendo la posicion inicial del cabezal.
"""

# IMPORTACIONES
from typing import Iterable, List, Optional, TypedDict

# ESTRUCTURA DE RESULTADOS
class DiskResult(TypedDict):
    """Resultado estandar que retorna cada algoritmo."""

    algorithm: str
    sequence: List[int]
    total_distance: int
    average_access_time: float

# FUNCIONES AUXILIARES
def _normalize_requests(requests: Iterable[int]) -> List[int]:
    """Convierte las solicitudes a lista para validarlas y reutilizarlas."""
    return list(requests)


def _validate_common(
    requests: Iterable[int],
    head: int,
    disk_size: Optional[int] = None,
    direction: Optional[str] = None,
) -> List[int]:
    """Valida entradas compartidas por los algoritmos."""
    normalized_requests = _normalize_requests(requests)

    # Verifica que existan solicitudes
    if not normalized_requests:
        raise ValueError("La lista de solicitudes no puede estar vacia.")

    # Verifica que el cabezal sea válido
    if head < 0:
        raise ValueError("La posicion inicial del cabezal no puede ser negativa.")

    # Validaciones relacionadas con el disco
    if disk_size is not None:
        if disk_size <= 0:
            raise ValueError("El tamano del disco debe ser mayor que cero.")
        if head >= disk_size:
            raise ValueError("La posicion inicial del cabezal esta fuera del rango del disco.")

    # Verifica solicitudes válidas
    for request in normalized_requests:
        if request < 0:
            raise ValueError("No se aceptan cilindros negativos.")
        if disk_size is not None and request >= disk_size:
            raise ValueError("Una solicitud excede el tamano del disco.")

    if direction is not None and direction not in ("left", "right"):
        raise ValueError('La direccion debe ser "left" o "right".')

    return normalized_requests


def validate_disk_input(
    requests: Iterable[int],
    head: int,
    disk_size: int,
    direction: Optional[str] = None,
) -> None:
    """Valida un caso completo de simulacion antes de ejecutar algoritmos."""
    _validate_common(requests, head, disk_size, direction)


def _total_distance(sequence: List[int]) -> int:
    """Suma la distancia absoluta entre movimientos consecutivos."""
    return sum(abs(sequence[i] - sequence[i - 1]) for i in range(1, len(sequence)))


def _build_result(algorithm: str, sequence: List[int], request_count: int) -> DiskResult:
    """Construye el diccionario de resultado con metricas calculadas."""
    total = _total_distance(sequence)
    average = total / request_count if request_count else 0
    return {
        "algorithm": algorithm,
        "sequence": sequence,
        "total_distance": total,
        "average_access_time": average,
    }


# ALGORITMO FCFS
def fcfs(requests: Iterable[int], head: int) -> DiskResult:
    """First-Come, First-Served: atiende las solicitudes en orden de llegada."""
    validated_requests = _validate_common(requests, head)
    sequence = [head] + validated_requests
    return _build_result("FCFS", sequence, len(validated_requests))


# ALGORITMO SSTF
def sstf(requests: Iterable[int], head: int) -> DiskResult:
    """Shortest Seek Time First: siempre elige la solicitud mas cercana."""
    pending = _validate_common(requests, head)
    current = head
    sequence = [head]

    # Encuentra la solicitud más cercana
    while pending:
        nearest = min(pending, key=lambda request: abs(request - current))
        sequence.append(nearest)
        pending.remove(nearest)
        current = nearest

    return _build_result("SSTF", sequence, len(sequence) - 1)


# ALGORITMO SCAN
def scan(requests: Iterable[int], head: int, disk_size: int, direction: str) -> DiskResult:
    """SCAN: mueve el cabezal como un ascensor hasta el extremo y luego regresa."""
    validated_requests = _validate_common(requests, head, disk_size, direction)
    max_cylinder = disk_size - 1
    
    # Solicitudes menores al cabezal
    left = sorted(request for request in validated_requests if request < head)
    
    # Solicitudes mayores o iguales
    right = sorted(request for request in validated_requests if request >= head)
    sequence = [head]

     # Movimiento hacia la derecha
    if direction == "right":
        sequence.extend(right)
        if sequence[-1] != max_cylinder:
            sequence.append(max_cylinder)
        sequence.extend(reversed(left))
    
    # Movimiento hacia la izquierda
    else:
        sequence.extend(reversed(left))
        if sequence[-1] != 0:
            sequence.append(0)
        sequence.extend(right)

    return _build_result("SCAN", sequence, len(validated_requests))


# ALGORITMO C-SCAN
def c_scan(requests: Iterable[int], head: int, disk_size: int, direction: str) -> DiskResult:
    """C-SCAN: avanza en una sola direccion y salta al extremo opuesto."""
    validated_requests = _validate_common(requests, head, disk_size, direction)
    max_cylinder = disk_size - 1
    left = sorted(request for request in validated_requests if request < head)
    right = sorted(request for request in validated_requests if request >= head)
    sequence = [head]

    # Movimiento hacia la derecha
    if direction == "right":
        sequence.extend(right)
        if sequence[-1] != max_cylinder:
            sequence.append(max_cylinder)
        if left:
            sequence.append(0)
            sequence.extend(left)
    
    # Movimiento hacia la izquierda
    else:
        sequence.extend(reversed(left))
        if sequence[-1] != 0:
            sequence.append(0)
        if right:
            sequence.append(max_cylinder)
            sequence.extend(reversed(right))

    return _build_result("C-SCAN", sequence, len(validated_requests))
