# Simulador de planificacion de E/S en disco

Aplicacion en Python para comparar algoritmos de planificacion de E/S en disco. El simulador modela el movimiento del cabezal entre cilindros y usa esa distancia como una aproximacion del **seek time** acumulado.

## Problema

En un disco magnetico, el acceso a datos no depende solo de la transferencia de informacion. Tambien existe una penalizacion fisica por mover el brazo/cabezal hasta el cilindro solicitado. Si el controlador atiende las solicitudes en un orden poco eficiente, el cabezal puede recorrer una distancia innecesariamente alta.

La planificacion de E/S intenta decidir el orden de atencion de las solicitudes para reducir el movimiento, mejorar el tiempo promedio de acceso o mantener un comportamiento justo y predecible.

## Algoritmos implementados

### FCFS

**First-Come, First-Served** atiende las solicitudes en el mismo orden en que llegan. Es el algoritmo mas simple y facil de entender, pero puede producir mucho movimiento si las solicitudes estan dispersas.

### SSTF

**Shortest Seek Time First** elige en cada paso la solicitud mas cercana a la posicion actual del cabezal. Suele reducir la distancia total, aunque puede dejar esperando solicitudes lejanas si siguen apareciendo solicitudes cercanas.

### SCAN

**SCAN** simula un ascensor. El cabezal avanza en una direccion, atiende solicitudes en el camino hasta llegar al extremo del disco y luego cambia de direccion para atender las restantes.

### C-SCAN

**Circular SCAN** avanza en una sola direccion. Al llegar al extremo, salta al extremo opuesto y continua atendiendo solicitudes en la misma direccion. En este proyecto, el salto se cuenta como movimiento del cabezal.

## Estructura

```text
disk_scheduler/
├── main.py
├── algorithms.py
├── visualization.py
├── exporter.py
├── tests/
│   └── test_algorithms.py
├── README.md
└── requirements.txt
```

## Instalacion

Desde la carpeta del proyecto:

```bash
pip install -r requirements.txt
```

## Ejecucion interactiva

```bash
python main.py
```

El programa pedira:

- Tamano del disco.
- Posicion inicial del cabezal.
- Lista de solicitudes.
- Direccion inicial para SCAN y C-SCAN.

La lista de solicitudes puede escribirse asi:

```text
[98, 183, 37, 122, 14, 124, 65, 67]
```

Tambien se acepta:

```text
98, 183, 37, 122, 14, 124, 65, 67
```

## Ejecucion con caso de prueba

```bash
python main.py --example
```

Para ejecutar sin abrir graficas:

```bash
python main.py --example --no-plots
```

Para evitar la pregunta de exportacion:

```bash
python main.py --example --no-export-prompt
```

Para exportar sin pregunta interactiva:

```bash
python main.py --example --no-plots --export both
```

## Ejecución con interfaz gráfica

```bash
streamlit run app.py
```

Si Windows no reconoce el comando `streamlit`, usa:

```bash
python -m streamlit run app.py
```

La interfaz web permite ingresar el tamaño del disco, la posición inicial del
cabezal, la lista de solicitudes y la dirección inicial para SCAN/C-SCAN.
Después de presionar **Ejecutar simulación**, muestra la tabla comparativa,
indica automáticamente el algoritmo más eficiente y permite elegir una sola
gráfica a la vez:

- FCFS
- SSTF
- SCAN
- C-SCAN
- Comparación general
- Barras: distancia total
- Barras: tiempo promedio

También incluye botones para descargar los resultados en CSV y JSON.

## Ejemplo de entrada

```text
Tamano del disco: 200
Posicion inicial del cabezal: 53
Solicitudes: [98, 183, 37, 122, 14, 124, 65, 67]
Direccion: right
```

## Ejemplo de salida

```text
+-------------+-------------------------------------------------+-------------------+-------------------+
| Algoritmo   | Secuencia de atencion                           | Distancia total   | Tiempo promedio   |
+-------------+-------------------------------------------------+-------------------+-------------------+
| FCFS        | [53, 98, 183, 37, 122, 14, 124, 65, 67]         | 640               | 80.00             |
| SSTF        | [53, 65, 67, 37, 14, 98, 122, 124, 183]         | 236               | 29.50             |
| SCAN        | [53, 65, 67, 98, 122, 124, 183, 199, 37, 14]    | 331               | 41.38             |
| C-SCAN      | [53, 65, 67, 98, 122, 124, 183, 199, 0, 14, 37] | 382               | 47.75             |
+-------------+-------------------------------------------------+-------------------+-------------------+

Para este caso, el algoritmo mas eficiente fue SSTF porque recorrio la menor distancia total: 236 cilindros.
```

## Interpretacion de resultados

- **Secuencia de atencion:** recorrido completo del cabezal, iniciando en la posicion inicial.
- **Distancia total:** suma de movimientos entre cilindros consecutivos. Representa el seek time acumulado.
- **Tiempo promedio de acceso:** distancia total dividida entre el numero de solicitudes originales.
- **Algoritmo mas eficiente:** el que tiene menor distancia total para el caso evaluado.

## Graficas

El proyecto genera:

- Una grafica individual por algoritmo con el movimiento del cabezal.
- Una comparacion de los movimientos en subgraficas.
- Una grafica de barras para distancia total.
- Una grafica de barras para tiempo promedio de acceso.

## Exportacion

Al finalizar, el programa pregunta si deseas exportar resultados:

```text
Deseas exportar resultados? (none/csv/json/both):
```

Los archivos se guardan en:

```text
exports/results.csv
exports/results.json
```

## Validaciones

El simulador valida que:

- No existan cilindros negativos.
- La posicion inicial del cabezal este dentro del rango del disco.
- Las solicitudes esten dentro del rango `0` a `disk_size - 1`.
- La direccion sea `left` o `right`.
- La lista de solicitudes no este vacia.

## Pruebas

Para ejecutar las pruebas unitarias:

```bash
pytest
```

Las pruebas cubren FCFS, SSTF, SCAN, C-SCAN y validaciones principales.

## Ventajas y desventajas

| Algoritmo | Ventajas | Desventajas |
|---|---|---|
| FCFS | Muy simple, respeta el orden de llegada, facil de implementar. | Puede generar recorridos largos y tiempos promedio altos. |
| SSTF | Suele reducir la distancia total recorrida. | Puede causar espera prolongada para solicitudes lejanas. |
| SCAN | Movimiento ordenado y predecible, reduce saltos extremos frecuentes. | Puede atender mas tarde solicitudes que quedan justo detras del cabezal. |
| C-SCAN | Ofrece un tratamiento mas uniforme en una sola direccion. | El salto al extremo opuesto aumenta la distancia total contabilizada. |
