# config.py
"""
Argumentos y constantes utilizadas a lo largo del programa
"""

import argparse
from os.path import join, dirname, abspath

# Parser de argumentos por consola
ap = argparse.ArgumentParser()

# Argumento para especificar la calidad del video
ap.add_argument("-q", "--quality",
                required=False,
                help="Parametro de calidad de la camara. Low: 0, High: 1. Valor default: 0",
                choices=["0", "1"],
                default="0")

# Se asume que la camara esta en orientacion norte por defecto
ap.add_argument("-o", "--orientation",
                required=False,
                help="Parametro de orientación de la camara. Valor default: n (norte)",
                choices=["n", "o", "s", "e"],
                default="n",
                type=str.lower)

# Argumento para mostrar la camara
ap.add_argument("-s", "--show",
                required=False,
                help="Mostrar camara. Valor default: False",
                action="store_true")

# Argumento para mostrar el modo debug del programa info de la pantalla
ap.add_argument("-d", "--debug",
                required=False,
                help="Modo debug. Mostrar información de la pantalla (controles y variables). Valor default: False",
                action="store_true")

args = vars(ap.parse_args())


# Umbral para considerar foto borrosa
THRESHOLD: float = 299.12

# Colores
COLOR_BLACK: tuple      = (0, 0, 0)
COLOR_BACKGROUND: tuple = (32, 32, 32)
COLOR_CONFIRM: tuple    = (139, 0, 0)   # Rojo
COLOR_REJECT: tuple     = (0, 128, 0)   # Verde

FPS: int      = 60
BAR_SIZE: int = 250

# Rutas de las imagenes
BASE_DIR = dirname(abspath(__file__)).replace("utils", "")
CAMERA_NOT_FOUND_PATH: str = join(f"{BASE_DIR}", "assets", "camera_not_found.jpg")
CAMERA_FOUND_PATH: str     = join(f"{BASE_DIR}", "assets", "camera_found.jpg")