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

# Argumento para elegir el bot asistente a utilizar
ap.add_argument("-a", "--assistant",
                required=True,
                help="Asistente. Elegir asistente de IA a utilizar",
                type=str.lower)

# Argumento para realizar demos
ap.add_argument("-t", "--demo",
                required=False,
                help="Modo demostración. El asistente no es ocupado. Se utiliza un output de demostración. Valor default: False",
                action="store_true")

args = vars(ap.parse_args())


# Colores
COLOR_BLACK: tuple = (0, 0, 0)
COLOR_WHITE: tuple = (255, 255, 255)
COLOR_BACKGROUND: tuple = (32, 32, 32)
COLOR_REJECT: tuple = (139, 0, 0)   # Rojo
COLOR_CONFIRM: tuple = (0, 128, 0)   # Verde

# Pantalla
FPS: int = 60
BAR_SIZE: int = 250

# Rutas de las imagenes
BASE_DIR = dirname(abspath(__file__)).replace("utils", "")
BACKGROUND: str = join(f"{BASE_DIR}", "assets", "background.jpg")
NOTFOUND_NOINTERNET: str = join(
    f"{BASE_DIR}", "assets", "notfound_nointernet.jpg")
NOTFOUND_INTERNET: str = join(f"{BASE_DIR}", "assets", "notfound_internet.jpg")
FOUND_NOINTERNET: str = join(f"{BASE_DIR}", "assets", "found_nointernet.jpg")
FOUND_INTERNET: str = join(f"{BASE_DIR}", "assets", "found_internet.jpg")

DEBUG_FONT = "Consolas"
RESULTS_FONT = "Segoe UI Emoji"

# Constantes que tienen que ver con los asistentes
DEMO_MODE_OUTPUT: str = '👍 Lo que has logrado;Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n📝 Para mejorar la organización;Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n❓ Para reflexionar;Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n✨ Mejorando correferencias;Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
