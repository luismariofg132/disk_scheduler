# Simulador de planificacion de E/S en disco

Este proyecto simula algoritmos de planificacion de E/S para un controlador de disco. El objetivo es comparar como se mueve el cabezal al atender solicitudes de cilindros y medir el costo asociado al movimiento fisico del brazo del disco.

En discos magneticos, una parte importante de la latencia proviene del movimiento fisico del cabezal. Este simulador se enfoca en el **seek time**, representado como la distancia recorrida entre cilindros consecutivos.

## Problema que resuelve

Cuando varias solicitudes de lectura o escritura llegan al disco, el controlador debe decidir en que orden atenderlas. Un mal orden puede hacer que el cabezal recorra demasiada distancia, aumentando el tiempo de acceso. Los algoritmos de planificacion buscan reducir o controlar ese movimiento.

## Algoritmos implementados

- **FCFS (First-Come, First-Served):** atiende las solicitudes en el mismo orden en que llegan. Es simple y justo, pero puede generar mucho movimiento.
- **SSTF (Shortest Seek Time First):** en cada paso atiende la solicitud mas cercana a la posicion actual. Suele reducir la distancia total, aunque puede retrasar solicitudes lejanas.
- **SCAN:** funciona como un ascensor. El cabezal avanza en una direccion, atiende solicitudes hasta llegar al extremo del disco y luego cambia de direccion.
- **C-SCAN:** el cabezal avanza en una sola direccion. Al llegar al extremo, salta al extremo opuesto y continua. El salto se cuenta como movimiento.

## Estructura

```text
disk_scheduler/
├── main.py
├── algorithms.py
├── visualization.py
├── README.md
└── requirements.txt
```

## Instalacion

Desde la carpeta `disk_scheduler`, instala las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecucion

```bash
python main.py
```

El programa usa estos datos de prueba:

```python
disk_size = 200
head = 53
requests = [98, 183, 37, 122, 14, 124, 65, 67]
direction = "right"
```

## Ejemplo de salida

```text
Algoritmo | Secuencia                         | Distancia total | Tiempo promedio
FCFS      | [53, 98, 183, 37, 122, ...]       | ...             | ...
SSTF      | [53, 65, 67, 37, 14, ...]         | ...             | ...
SCAN      | [53, 65, 67, 98, 122, ...]        | ...             | ...
C-SCAN    | [53, 65, 67, 98, 122, ...]        | ...             | ...
```

Despues de la tabla, el programa indica cual algoritmo fue mas eficiente para el caso de prueba, usando como criterio la menor distancia total recorrida.

## Interpretacion de metricas

- **Secuencia:** muestra el recorrido completo del cabezal, empezando por la posicion inicial.
- **Distancia total:** suma de todos los movimientos entre cilindros consecutivos. Representa el seek time acumulado.
- **Tiempo promedio de acceso:** distancia total dividida entre el numero de solicitudes. Permite comparar el costo promedio por solicitud.

## Visualizacion

El proyecto usa `matplotlib` para graficar el movimiento del cabezal:

- Eje X: paso o tiempo.
- Eje Y: posicion del cilindro.
- Linea con marcadores: movimientos consecutivos del cabezal.
- Graficas individuales para cada algoritmo.
- Comparacion final en subgraficas.

## Validaciones

El simulador valida que:

- No existan cilindros negativos.
- Las solicitudes no superen el tamano del disco.
- La posicion inicial del cabezal este dentro del rango.
- La direccion sea `left` o `right`.
