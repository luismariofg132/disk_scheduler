"""Interfaz web con Streamlit para el simulador de planificacion de disco."""

import io
import json
import csv
from typing import List

import streamlit as st

from algorithms import DiskResult, c_scan, fcfs, scan, sstf, validate_disk_input
from main import parse_requests
from visualization import (
    plot_average_time_bars,
    plot_comparison,
    plot_movement,
    plot_total_distance_bars,
)


def run_simulation(
    requests: List[int],
    head: int,
    disk_size: int,
    direction: str,
) -> List[DiskResult]:
    """Ejecuta los cuatro algoritmos de planificacion de disco."""
    validate_disk_input(requests, head, disk_size, direction)
    return [
        fcfs(requests, head),
        sstf(requests, head),
        scan(requests, head, disk_size, direction),
        c_scan(requests, head, disk_size, direction),
    ]


def get_best_algorithm(results: List[DiskResult]) -> DiskResult:
    """Retorna el resultado con menor distancia total recorrida."""
    return min(results, key=lambda result: result["total_distance"])


def results_to_rows(results: List[DiskResult]) -> List[dict[str, object]]:
    """Convierte los resultados a filas amigables para tablas y CSV."""
    return [
        {
            "Algoritmo": result["algorithm"],
            "Secuencia de atencion": " -> ".join(map(str, result["sequence"])),
            "Distancia total": result["total_distance"],
            "Tiempo promedio de acceso": round(result["average_access_time"], 2),
        }
        for result in results
    ]


def results_to_csv(results: List[DiskResult]) -> bytes:
    """Convierte los resultados a CSV en memoria."""
    csv_buffer = io.StringIO()
    rows = results_to_rows(results)
    writer = csv.DictWriter(csv_buffer, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
    return csv_buffer.getvalue().encode("utf-8")


def results_to_json(results: List[DiskResult]) -> str:
    """Convierte los resultados a JSON en memoria."""
    return json.dumps(results, indent=4, ensure_ascii=False)


def select_figure(option: str, results: List[DiskResult]):
    """Selecciona y crea la figura solicitada por el usuario."""
    result_by_name = {result["algorithm"]: result for result in results}

    if option in result_by_name:
        return plot_movement(result_by_name[option])
    if option == "Comparación general":
        return plot_comparison(results)
    if option == "Barras: distancia total":
        return plot_total_distance_bars(results)
    return plot_average_time_bars(results)


def main() -> None:
    """Construye y ejecuta la aplicacion Streamlit."""
    st.set_page_config(
        page_title="Simulador de planificacion de E/S",
        layout="wide",
    )

    st.title("Simulador de planificacion de E/S en disco")
    st.write(
        "Compara FCFS, SSTF, SCAN y C-SCAN usando la distancia recorrida "
        "por el cabezal como aproximacion del seek time."
    )

    with st.sidebar:
        st.header("Datos de entrada")
        disk_size = st.number_input(
            "Tamano del disco",
            min_value=1,
            value=200,
            step=1,
            help="Ejemplo: 200 representa cilindros de 0 a 199.",
        )
        head = st.number_input(
            "Posicion inicial del cabezal",
            min_value=0,
            value=53,
            step=1,
        )
        raw_requests = st.text_area(
            "Lista de solicitudes",
            value="[98, 183, 37, 122, 14, 124, 65, 67]",
            help="Puedes escribir [98, 183, 37] o 98, 183, 37.",
        )
        direction = st.selectbox(
            "Direccion inicial para SCAN/C-SCAN",
            options=["right", "left"],
        )
        run_button = st.button("Ejecutar simulación", type="primary")

    if not run_button and "results" not in st.session_state:
        st.info("Ingresa los datos y presiona Ejecutar simulación.")
        return

    if run_button:
        try:
            requests = parse_requests(raw_requests)
            results = run_simulation(requests, int(head), int(disk_size), direction)
            st.session_state["results"] = results
        except ValueError as error:
            st.error(f"Datos invalidos: {error}")
            return

    results = st.session_state["results"]
    best = get_best_algorithm(results)

    st.subheader("Tabla comparativa")
    st.dataframe(results_to_rows(results), use_container_width=True, hide_index=True)

    st.success(
        f"Algoritmo mas eficiente: {best['algorithm']} "
        f"con {best['total_distance']} cilindros recorridos."
    )

    col_csv, col_json = st.columns(2)
    with col_csv:
        st.download_button(
            "Descargar resultados en CSV",
            data=results_to_csv(results),
            file_name="disk_scheduler_results.csv",
            mime="text/csv",
        )
    with col_json:
        st.download_button(
            "Descargar resultados en JSON",
            data=results_to_json(results),
            file_name="disk_scheduler_results.json",
            mime="application/json",
        )

    st.subheader("Visualizacion")
    plot_option = st.selectbox(
        "Selecciona una grafica",
        options=[
            "FCFS",
            "SSTF",
            "SCAN",
            "C-SCAN",
            "Comparación general",
            "Barras: distancia total",
            "Barras: tiempo promedio",
        ],
    )
    fig = select_figure(plot_option, results)
    st.pyplot(fig)


if __name__ == "__main__":
    main()
