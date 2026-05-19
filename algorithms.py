"""Algoritmos de planificacion de E/S en disco.

El simulador se enfoca en el seek time: la distancia que recorre el cabezal
entre cilindros. Cada algoritmo retorna la secuencia completa de movimiento,
incluyendo la posicion inicial del cabezal.
"""


def _validate_common(requests, head, disk_size=None, direction=None):
    """Valida entradas compartidas por los algoritmos."""
    if head < 0:
        raise ValueError("La posicion inicial del cabezal no puede ser negativa.")

    if disk_size is not None:
        if disk_size <= 0:
            raise ValueError("El tamano del disco debe ser mayor que cero.")
        if head >= disk_size:
            raise ValueError("La posicion inicial del cabezal esta fuera del rango del disco.")

    for request in requests:
        if request < 0:
            raise ValueError("No se aceptan cilindros negativos.")
        if disk_size is not None and request >= disk_size:
            raise ValueError("Una solicitud excede el tamano del disco.")

    if direction is not None and direction not in ("left", "right"):
        raise ValueError('La direccion debe ser "left" o "right".')


def validate_disk_input(requests, head, disk_size, direction=None):
    """Valida un caso completo de simulacion antes de ejecutar algoritmos."""
    _validate_common(requests, head, disk_size, direction)


def _total_distance(sequence):
    """Suma la distancia absoluta entre movimientos consecutivos."""
    return sum(abs(sequence[i] - sequence[i - 1]) for i in range(1, len(sequence)))


def _build_result(algorithm, sequence, request_count):
    total = _total_distance(sequence)
    average = total / request_count if request_count else 0
    return {
        "algorithm": algorithm,
        "sequence": sequence,
        "total_distance": total,
        "average_access_time": average,
    }


def fcfs(requests, head):
    """First-Come, First-Served: atiende las solicitudes en orden de llegada."""
    _validate_common(requests, head)
    sequence = [head] + list(requests)
    return _build_result("FCFS", sequence, len(requests))


def sstf(requests, head):
    """Shortest Seek Time First: siempre elige la solicitud mas cercana."""
    _validate_common(requests, head)
    pending = list(requests)
    current = head
    sequence = [head]

    while pending:
        nearest = min(pending, key=lambda request: abs(request - current))
        sequence.append(nearest)
        pending.remove(nearest)
        current = nearest

    return _build_result("SSTF", sequence, len(requests))


def scan(requests, head, disk_size, direction):
    """SCAN: mueve el cabezal como un ascensor hasta el extremo y luego regresa."""
    _validate_common(requests, head, disk_size, direction)
    if not requests:
        return _build_result("SCAN", [head], 0)

    max_cylinder = disk_size - 1
    left = sorted(request for request in requests if request < head)
    right = sorted(request for request in requests if request >= head)
    sequence = [head]

    if direction == "right":
        sequence.extend(right)
        if sequence[-1] != max_cylinder:
            sequence.append(max_cylinder)
        sequence.extend(reversed(left))
    else:
        sequence.extend(reversed(left))
        if sequence[-1] != 0:
            sequence.append(0)
        sequence.extend(right)

    return _build_result("SCAN", sequence, len(requests))


def c_scan(requests, head, disk_size, direction):
    """C-SCAN: avanza en una sola direccion y salta al extremo opuesto."""
    _validate_common(requests, head, disk_size, direction)
    if not requests:
        return _build_result("C-SCAN", [head], 0)

    max_cylinder = disk_size - 1
    left = sorted(request for request in requests if request < head)
    right = sorted(request for request in requests if request >= head)
    sequence = [head]

    if direction == "right":
        sequence.extend(right)
        if sequence[-1] != max_cylinder:
            sequence.append(max_cylinder)
        if left:
            sequence.append(0)
            sequence.extend(left)
    else:
        sequence.extend(reversed(left))
        if sequence[-1] != 0:
            sequence.append(0)
        if right:
            sequence.append(max_cylinder)
            sequence.extend(reversed(right))

    return _build_result("C-SCAN", sequence, len(requests))
