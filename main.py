"""
Entrada principal: lanzar la interfaz gráfica de la simulación de impresora.
Ejecutar desde esta carpeta: python main.py
"""

from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.printer_gui import launch_app

if __name__ == "__main__":
    launch_app()
