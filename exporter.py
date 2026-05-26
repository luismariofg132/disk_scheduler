"""Exportacion de resultados del simulador."""

# IMPORTACIONES
import csv
import json
from pathlib import Path
from typing import Iterable

from algorithms import DiskResult


# EXPORTACIÓN A CSV
def export_to_csv(results: Iterable[DiskResult], file_path: str) -> Path:
    """Exporta los resultados a un archivo CSV y retorna la ruta generada."""
    path = Path(file_path)
    # Crea la carpeta si no existe
    path.parent.mkdir(parents=True, exist_ok=True)

    # Escribe el archivo CSV
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "algorithm",
                "sequence",
                "total_distance",
                "average_access_time",
            ],
        )
        writer.writeheader()
        for result in results:
            writer.writerow(
                {
                    "algorithm": result["algorithm"],
                    "sequence": " -> ".join(map(str, result["sequence"])),
                    "total_distance": result["total_distance"],
                    "average_access_time": f"{result['average_access_time']:.2f}",
                }
            )

    return path


# EXPORTACIÓN A JSON
def export_to_json(results: Iterable[DiskResult], file_path: str) -> Path:
    """Exporta los resultados a un archivo JSON y retorna la ruta generada."""
    path = Path(file_path)
    # Crea la carpeta si no existe
    path.parent.mkdir(parents=True, exist_ok=True)

    # Escribe el archivo JSON
    with path.open("w", encoding="utf-8") as json_file:
        json.dump(list(results), json_file, indent=4, ensure_ascii=False)

    return path
