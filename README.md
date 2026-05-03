# Simulación de cola de impresión

Proyecto en Python que simula una impresora con **una cola FIFO propia**, trabajos de impresión, métricas de espera y **interfaz gráfica** con Tkinter (la lógica está en paquete `src/`, independiente de la UI).

## Requisitos

- Python 3.10 o superior (probado en 3.14)
- Tkinter (incluido en la instalación habitual de Python en Windows)

## Ejecución

Desde esta carpeta (`simulacion_impresora`):

```powershell
py -3 main.py
```

En sistemas donde el comando sea `python`:

```bash
python main.py
```

## Pruebas

```powershell
py -3 -m pip install -r requirements.txt
py -3 -m pytest tests -v
```

## Estructura del código

| Módulo | Rol |
|--------|-----|
| `src/custom_queue.py` | Cola FIFO propia (`enqueue` / `dequeue`); la simulación no atiende trabajos sin usar esta estructura. |
| `src/print_task.py` | Modelo `PrintTask`: ID, páginas, instante de llegada. |
| `src/printer.py` | `Printer`: duración por trabajo, ocupación (`busy_until`), comprobar ocupado/libre. |
| `src/print_simulation.py` | `PrintSimulation`: llegadas en el tiempo, cola, un trabajo activo a la vez, esperas y métricas. |
| `src/printer_gui.py` | Entrada por tabla, validaciones de UI y muestra de resultados. |

## Métricas al finalizar

- Cantidad total de trabajos **válidos** procesados  
- Tiempo medio de espera en cola  
- Trabajo con **mayor** tiempo de espera  
- **Tamaño máximo** alcanzado por la cola  

Los trabajos con datos inválidos (ID vacío, páginas ≤ 0, llegada negativa) se informan como rechazados y no cuentan en el procesamiento.

## Contenido sugerido para el PDF de entrega

1. **Descripción breve**  
   - Cómo avanza la simulación por eventos en el tiempo: las llegadas se encolan; la impresora, si está libre, **desencola** el siguiente trabajo (FIFO); el tiempo de servicio es `páginas × segundos_por_página`; el tiempo de espera es el instante en que empieza el servicio menos la llegada.  
   - Uso de `Queue`: único buffer entre llegadas y la impresora; el tamaño máximo de cola es el máximo número de elementos encolados a la vez.  
   - Clases: `Queue`, `PrintTask`, `Printer`, `PrintSimulation` (+ datos de resultado y métricas).  
   - Métricas: las cuatro enumeradas arriba.  
   - Interfaz: **Tkinter** (`printer_gui`), escenario de ejemplo y valores mostrados.  

2. **Enlace al video en Google Drive** (≤ 3 min, código + ejecución, permiso de lectura).  

3. **Enlace al repositorio público GitHub** con este código, este README y la carpeta `tests/`.

## Licencia educativa

Uso libre para fines académicos.
