"""Interfaz web con Streamlit para el simulador de planificacion de disco.

La aplicación permite:
- Ejecutar simulaciones individuales.
- Comparar escenarios predefinidos.
- Visualizar gráficas.
- Descargar resultados en CSV y JSON.
"""

# IMPORTACIONES
import csv
import io
import json
from collections import Counter
from typing import Any, List

import matplotlib.pyplot as plt
import streamlit as st

# Algoritmos y validaciones
from algorithms import DiskResult, c_scan, fcfs, scan, sstf, validate_disk_input

# Conversión de solicitudes
from main import parse_requests

# Escenarios predefinidos
from scenarios import Scenario, get_predefined_scenarios

# Funciones de visualización
from visualization import (
    plot_algorithm_wins,
    plot_average_time_bars,
    plot_comparison,
    plot_movement,
    plot_scenario_average_time_comparison,
    plot_scenario_distance_comparison,
    plot_total_distance_bars,
)

# Tipo auxiliar para resultados de escenarios
ScenarioResult = dict[str, Any]

# SIMULACIÓN
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

# CONVERSIÓN DE RESULTADOS
def results_to_rows(results: List[DiskResult]) -> List[dict[str, object]]:
    """Convierte los resultados individuales a filas de tabla."""
    return [
        {
            "Algoritmo": result["algorithm"],
            "Secuencia de atencion": " -> ".join(map(str, result["sequence"])),
            "Distancia total": result["total_distance"],
            "Tiempo promedio de acceso": round(result["average_access_time"], 2),
        }
        for result in results
    ]


def rows_to_csv(rows: List[dict[str, object]]) -> bytes:
    """Convierte filas tabulares a CSV en memoria."""
    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
    return csv_buffer.getvalue().encode("utf-8")


def results_to_csv(results: List[DiskResult]) -> bytes:
    """Convierte resultados individuales a CSV en memoria."""
    return rows_to_csv(results_to_rows(results))


def results_to_json(results: List[DiskResult]) -> str:
    """Convierte resultados individuales a JSON en memoria."""
    return json.dumps(results, indent=4, ensure_ascii=False)


# VISUALIZACIONES
def select_individual_figure(option: str, results: List[DiskResult]):
    """Selecciona y crea la figura de simulacion individual."""
    result_by_name = {result["algorithm"]: result for result in results}

    if option in result_by_name:
        return plot_movement(result_by_name[option])
    if option == "Comparacion general":
        return plot_comparison(results)
    if option == "Barras: distancia total":
        return plot_total_distance_bars(results)
    return plot_average_time_bars(results)


# ESCENARIOS
def run_scenario_comparison(selected_scenarios: List[str]) -> tuple[List[ScenarioResult], List[dict[str, object]]]:
    """Ejecuta todos los algoritmos para los escenarios seleccionados."""
    scenarios = get_predefined_scenarios()
    scenario_results: List[ScenarioResult] = []
    winners: List[dict[str, object]] = []

    for scenario_name in selected_scenarios:
        scenario = scenarios[scenario_name]
        results = run_simulation(
            scenario["requests"],
            scenario["head"],
            scenario["disk_size"],
            scenario["direction"],
        )
        best = get_best_algorithm(results)
        
        # Guarda ganador del escenario
        winners.append(
            {
                "Escenario": scenario_name,
                "Mejor algoritmo": best["algorithm"],
                "Distancia total": best["total_distance"],
                "Tiempo promedio": round(best["average_access_time"], 2),
            }
        )

        
        # Guarda resultados completos
        for result in results:
            scenario_results.append(
                {
                    "scenario": scenario_name,
                    "algorithm": result["algorithm"],
                    "total_distance": result["total_distance"],
                    "average_access_time": result["average_access_time"],
                    "sequence": result["sequence"],
                }
            )

    return scenario_results, winners


def scenario_results_to_rows(scenario_results: List[ScenarioResult]) -> List[dict[str, object]]:
    """Convierte resultados de escenarios a filas para la tabla completa."""
    return [
        {
            "Escenario": result["scenario"],
            "Algoritmo": result["algorithm"],
            "Distancia total": result["total_distance"],
            "Tiempo promedio": round(float(result["average_access_time"]), 2),
            "Secuencia": " -> ".join(map(str, result["sequence"])),
        }
        for result in scenario_results
    ]


def scenario_results_to_json(scenario_results: List[ScenarioResult]) -> str:
    """Convierte resultados de escenarios a JSON en memoria."""
    return json.dumps(scenario_results, indent=4, ensure_ascii=False)

# ANÁLISIS AUTOMÁTICO
def build_scenario_analysis(winners: List[dict[str, object]]) -> str:
    """Genera una explicacion automatica sobre el algoritmo que mas gana."""
    if not winners:
        return "No hay escenarios seleccionados para analizar."

    counts = Counter(str(winner["Mejor algoritmo"]) for winner in winners)
    top_algorithm, top_count = counts.most_common(1)[0]
    total = len(winners)
    explanations = {
        "FCFS": (
            "FCFS gano mas veces porque en estos escenarios el orden de llegada "
            "coincidio con recorridos relativamente cortos. Aun asi, suele ser "
            "sensible al orden de las solicitudes."
        ),
        "SSTF": (
            "SSTF gano mas veces porque selecciona siempre la solicitud mas cercana "
            "al cabezal actual, reduciendo el movimiento inmediato. En sistemas "
            "reales puede presentar inanicion para solicitudes lejanas."
        ),
        "SCAN": (
            "SCAN gano mas veces porque el movimiento tipo ascensor aprovecho la "
            "direccion inicial y evito saltos desordenados. Es util cuando se busca "
            "un recorrido mas predecible."
        ),
        "C-SCAN": (
            "C-SCAN gano mas veces porque el recorrido circular favorecio una "
            "atencion uniforme en la direccion seleccionada. Su salto al extremo "
            "opuesto puede aumentar la distancia en otros casos."
        ),
    }
    return (
        f"En los {total} escenarios evaluados, {top_algorithm} fue el algoritmo "
        f"que mas veces obtuvo la menor distancia total ({top_count} veces). "
        f"{explanations[top_algorithm]}"
    )


def scenario_visual_explanation(option: str) -> str:
    """Retorna una explicacion didactica para la visualizacion elegida."""
    explanations = {
        "Distancia total por escenario": (
            "Esta grafica permite observar que algoritmo reduce mas el movimiento "
            "fisico del cabezal en cada distribucion de solicitudes. Una menor "
            "distancia total representa menor seek time acumulado."
        ),
        "Tiempo promedio por escenario": (
            "Esta grafica muestra la distancia promedio recorrida por solicitud. "
            "Es util para comparar el rendimiento relativo cuando cambia la "
            "ubicacion del cabezal o la dispersion de las solicitudes."
        ),
        "Ganadores por escenario": (
            "Esta visualizacion resume cuantas veces cada algoritmo obtuvo la "
            "menor distancia total. Sirve para mostrar que un algoritmo puede "
            "funcionar mejor en ciertos casos, pero no necesariamente en todos."
        ),
    }
    return explanations[option]


# MODO INDIVIDUAL
def render_individual_mode(
    run_button: bool,
    disk_size: int,
    head: int,
    raw_requests: str,
    direction: str,
) -> None:
    """Renderiza resultados del modo de simulacion individual."""
    if not run_button and "individual_results" not in st.session_state:
        st.info("Ingresa los datos y presiona Ejecutar simulacion.")
        return

    # Ejecuta simulación
    if run_button:
        try:
            requests = parse_requests(raw_requests)
            st.session_state["individual_results"] = run_simulation(
                requests,
                int(head),
                int(disk_size),
                direction,
            )
        except ValueError as error:
            st.error(f"Datos invalidos: {error}")
            return

    results = st.session_state["individual_results"]
    best = get_best_algorithm(results)

    # Tabla de resultados
    st.subheader("Tabla comparativa")
    st.dataframe(results_to_rows(results), use_container_width=True, hide_index=True)
    
    # Mejor algoritmo
    st.success(
        f"Algoritmo mas eficiente: {best['algorithm']} "
        f"con {best['total_distance']} cilindros recorridos."
    )

    # Descargas
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

      # Visualización
    st.subheader("Visualizacion")
    plot_option = st.selectbox(
        "Selecciona una grafica",
        options=[
            "FCFS",
            "SSTF",
            "SCAN",
            "C-SCAN",
            "Comparacion general",
            "Barras: distancia total",
            "Barras: tiempo promedio",
        ],
    )
    fig = select_individual_figure(plot_option, results)
    st.pyplot(fig)
    plt.close(fig)


# MODO ESCENARIOS
def render_scenario_mode(selected_scenarios: List[str], compare_button: bool) -> None:
    """Renderiza resultados del modo de comparacion de escenarios."""
    scenarios = get_predefined_scenarios()
    st.subheader("Escenarios predefinidos")
    
    # Muestra información de escenarios
    for scenario_name in selected_scenarios:
        scenario = scenarios[scenario_name]
        st.markdown(
            f"**{scenario_name}:** {scenario['description']} "
            f"`head={scenario['head']}`, `direction={scenario['direction']}`, "
            f"`requests={scenario['requests']}`"
        )

    if not compare_button and "scenario_results" not in st.session_state:
        st.info("Selecciona los escenarios y presiona Comparar escenarios.")
        return

     # Ejecuta comparación
    if compare_button:
        if not selected_scenarios:
            st.error("Selecciona al menos un escenario para comparar.")
            return
        scenario_results, winners = run_scenario_comparison(selected_scenarios)
        st.session_state["scenario_results"] = scenario_results
        st.session_state["scenario_winners"] = winners

    scenario_results = st.session_state["scenario_results"]
    winners = st.session_state["scenario_winners"]
    complete_rows = scenario_results_to_rows(scenario_results)

    # Tabla completa
    st.subheader("Tabla completa de resultados")
    st.dataframe(complete_rows, use_container_width=True, hide_index=True)

     # Ganadores
    st.subheader("Mejor algoritmo por escenario")
    st.dataframe(winners, use_container_width=True, hide_index=True)

    st.info(build_scenario_analysis(winners))

    col_csv, col_json = st.columns(2)
    with col_csv:
        st.download_button(
            "Descargar comparacion en CSV",
            data=rows_to_csv(complete_rows),
            file_name="scenario_comparison_results.csv",
            mime="text/csv",
        )
    with col_json:
        st.download_button(
            "Descargar comparacion en JSON",
            data=scenario_results_to_json(scenario_results),
            file_name="scenario_comparison_results.json",
            mime="application/json",
        )

    # Visualizaciones
    st.subheader("Visualizacion de escenarios")
    plot_option = st.selectbox(
        "Selecciona una visualizacion",
        options=[
            "Distancia total por escenario",
            "Tiempo promedio por escenario",
            "Ganadores por escenario",
        ],
    )

    if plot_option == "Distancia total por escenario":
        fig = plot_scenario_distance_comparison(scenario_results)
    elif plot_option == "Tiempo promedio por escenario":
        fig = plot_scenario_average_time_comparison(scenario_results)
    else:
        fig = plot_algorithm_wins(winners)

    st.pyplot(fig)
    plt.close(fig)
    st.caption(scenario_visual_explanation(plot_option))


# FUNCIÓN PRINCIPAL
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

     # SIDEBAR
    with st.sidebar:
        mode = st.selectbox(
            "Modo de simulacion",
            options=["Simulacion individual", "Comparacion de escenarios"],
            key="simulation_mode",
        )

         # Reinicia resultados al cambiar modo
        if st.session_state.get("active_mode") != mode:
            st.session_state["active_mode"] = mode
            st.session_state.pop("individual_results", None)
            st.session_state.pop("scenario_results", None)
            st.session_state.pop("scenario_winners", None)
            st.rerun()

         # MODO INDIVIDUAL
        if mode == "Simulacion individual":
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
            run_button = st.button("Ejecutar simulacion", type="primary")
            for _ in range(6):
                st.empty()
        
        # MODO ESCENARIOS
        else:
            scenarios = get_predefined_scenarios()
            st.header("Escenarios")
            selected_scenarios = st.multiselect(
                "Selecciona escenarios para comparar",
                options=list(scenarios.keys()),
                default=list(scenarios.keys()),
            )
            compare_button = st.button("Comparar escenarios", type="primary")
            for _ in range(6):
                st.empty()

    # CONTENIDO PRINCIPAL
    if mode == "Simulacion individual":
        render_individual_mode(
            run_button,
            int(disk_size),
            int(head),
            raw_requests,
            direction,
        )
    else:
        render_scenario_mode(selected_scenarios, compare_button)


# Ejecuta la aplicación
if __name__ == "__main__":
    main()
