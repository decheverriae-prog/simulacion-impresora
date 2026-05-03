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

## Publicar en GitHub (subir el repositorio)

Este proyecto tiene su propio Git en la carpeta `simulacion_impresora` (commit inicial en la rama `main`).

1. En GitHub crea un repositorio **nuevo y vacío** (sin README), por ejemplo `simulacion_impresora`, **público**.
2. En PowerShell:

```powershell
cd "c:\Users\CHEUS\OneDrive\Desktop\editor de texto\simulacion_impresora"

git remote add origin https://github.com/TU_USUARIO/simulacion_impresora.git
git push -u origin main
```

Sustituye `TU_USUARIO` y el nombre del repo por los tuyos. Si GitHub pide iniciar sesión, usa tu usuario y un **Personal Access Token** como contraseña (o SSH si ya tienes clave configurada).

Con SSH:

```powershell
git remote add origin git@github.com:TU_USUARIO/simulacion_impresora.git
git push -u origin main
```

## Licencia educativa

Uso libre para fines académicos.
