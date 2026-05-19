"""Pruebas unitarias para los algoritmos de planificacion de disco."""

import pytest

from algorithms import c_scan, fcfs, scan, sstf, validate_disk_input


REQUESTS = [98, 183, 37, 122, 14, 124, 65, 67]
HEAD = 53
DISK_SIZE = 200
DIRECTION = "right"


def test_fcfs_calculates_sequence_and_metrics() -> None:
    """FCFS debe respetar el orden original de llegada."""
    result = fcfs(REQUESTS, HEAD)

    assert result["sequence"] == [53, 98, 183, 37, 122, 14, 124, 65, 67]
    assert result["total_distance"] == 640
    assert result["average_access_time"] == 80


def test_sstf_calculates_sequence_and_metrics() -> None:
    """SSTF debe elegir en cada paso la solicitud mas cercana."""
    result = sstf(REQUESTS, HEAD)

    assert result["sequence"] == [53, 65, 67, 37, 14, 98, 122, 124, 183]
    assert result["total_distance"] == 236
    assert result["average_access_time"] == 29.5


def test_scan_calculates_sequence_and_metrics() -> None:
    """SCAN debe avanzar hasta el extremo y luego cambiar de direccion."""
    result = scan(REQUESTS, HEAD, DISK_SIZE, DIRECTION)

    assert result["sequence"] == [53, 65, 67, 98, 122, 124, 183, 199, 37, 14]
    assert result["total_distance"] == 331
    assert result["average_access_time"] == 41.375


def test_c_scan_calculates_sequence_and_metrics() -> None:
    """C-SCAN debe contar el salto al extremo opuesto como movimiento."""
    result = c_scan(REQUESTS, HEAD, DISK_SIZE, DIRECTION)

    assert result["sequence"] == [53, 65, 67, 98, 122, 124, 183, 199, 0, 14, 37]
    assert result["total_distance"] == 382
    assert result["average_access_time"] == 47.75


def test_validation_rejects_empty_requests() -> None:
    """La simulacion requiere al menos una solicitud."""
    with pytest.raises(ValueError, match="no puede estar vacia"):
        validate_disk_input([], HEAD, DISK_SIZE, DIRECTION)


def test_validation_rejects_request_out_of_range() -> None:
    """No se deben aceptar solicitudes fuera del rango del disco."""
    with pytest.raises(ValueError, match="excede"):
        validate_disk_input([10, 200], HEAD, DISK_SIZE, DIRECTION)


def test_validation_rejects_invalid_direction() -> None:
    """La direccion solo puede ser left o right."""
    with pytest.raises(ValueError, match="left"):
        validate_disk_input(REQUESTS, HEAD, DISK_SIZE, "up")
