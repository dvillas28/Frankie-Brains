# FRANKIE Brains

Software de camara con integración IA. Por Daniel Villaseñor C durante 2025-1.

## [Linux Only] Instalación de fonts utilizadas

Este programa utiliza la fuente `Segoe UI Emoji` para mostrar resultados. Esta se encuentra de forma nativa en Windows. En Linux, se puede descargar desde [esta repo](https://github.com/mrbvrz/segoe-ui-linux#)

## Instalación para desarrollo

Es necesaria tener una instalación previa de Python `3.11.X` o superior.
Primero, clonar este repositorio y hacer `cd` en la carpeta creada.

### `.env`

Primero es necesario definir algunas variables de entorno en un archivo `.env`

```bash
OPENAI_API_KEY="" # Si se esta ocupando el asistente GPT
GEMINI_API_KEY="" # Si se esta ocupando el asistente gemini
```

### Linux - Activación del entorno

```bash
python3 -m venv .venv                   # crear entorno
source .venv/bin/activate               # activar entorno
pip install -r requirements.txt         # instalacion dependencias
```

### Windows - Activación del entorno

```powershell
py -m venv .venv                        # crear entorno
.\.venv\Scripts\Activate.ps1            # activar entorno
pip install -r requirements.txt         # instalacion dependencias
```

## Ejecución

```bash
python3 main.py [-options]     # linux
py main.py [-h] [-options]     # windows
```

### Opciones

```txt
options:
  -h, --help            show this help message and exit
  
  -q {0,1}, --quality {0,1}
                        Parametro de calidad de la camara. Low: 0, High: 1. Valor default: 0
  
  -o {n,o,s,e}, --orientation {n,o,s,e}
                        Parametro de orientación de la camara. Valor default: n (norte)   
  
  -s, --show            Mostrar camara. Valor default: False

  -d, --debug           Modo debug. Mostrar información de la pantalla (controles y variables). Valor default:
                        False

  -a ASSISTANT, --assistant ASSISTANT
                        Asistente. Elegir asistente de IA a utilizar
  
  -t, --demo            Modo demostración. El asistente no es ocupado. Se utiliza un output de demostración. Valor default: False

```

### Controles para el modo debug

- `<0>`: tomar foto y pasarla por el prompt `PLANIFICACION` de `utils/prompts.py`
- `<1>`: tomar foto y pasarla por el prompt `REVISION` de `utils/prompts.py`
- `<q>`: cerrar programa
- `<s>`: mostrar camara
- `<d>`: modo debug
- `<Esc>`: Fullscreen
- `<Arrow Keys>`: Rotar video

## Ejecución en boot bajo comando y en Raspberry PI

_Ojo_: Se requieren que estén los botones USB conectados previamente y tener una instalación de `antimicrox`

_Ojo_ 2: Intrucciones compatibles solamente con X11

### Script de instalación Raspberry PI

Ejecutar el script de instalación:

```bash
chmod +x install.sh
./install.sh
```

Este script:

1. Crea un _symlink_ al ejecutable `start_pyCamera.sh` en el directorio `~/bin` para poder ejecutar el programa globalmente con el comando `pycamera`

2. Crea un archivo `.desktop` para que el programa se ejecute en boot.

### Script de desinstalación

Ejecutar el script de desinstalación:

```bash
chmod +x uninstall.sh
./uninstall.sh
```

Este script elimina el _symlink_ `pycamera` y el archivo `.desktop` creados por el script anterior.
