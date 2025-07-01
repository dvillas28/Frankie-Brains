# FRANKIE Brains

Software de camara con integración IA. Por Daniel Villaseñor C durante 2025-1.

## `.env`

Primero es necesario definir algunas variables de entorno en un archivo `.env`

```bash
OPENAI_API_KEY="" # Si se esta ocupando el asistente GPT
GEMINI_API_KEY="" # Si se esta ocupando el asistente gemini

DEBUG_FONT=""
RESULTS_FONT=""
```

### _Fonts_ recomendadas

- Para el modo debug, se recomienda utilizar `Consolas`
- Para mostrar los resultados, se recomienda utilizar
  - `Segoe UI Emoji`: _font_ nativa para si se esta desarrollando en Windows
  - `Noto Color Emoji`: _font_ alternativa para Linux. Se tiene que instalar

```bash
# Instalación en distribuciones basadas en Debian/Ubuntu
sudo apt install fonts-noto-color-emoji

# Luego en .env se debe incluir el path donde fue instalada la font
RESULTS_FONT = "/usr/share/fonts/noto/NotoColorEmoji.ttf"
```

## _Features_

- Si al capturar la imagen, se muestra un _flasheo_ rojo, indicando que esta salio borrosa
- Si al capturar la imagen, se muestra un _flasheo_ verde, indicando que esta salio nitída

## Instalación

Es necesaria tener una instalación previa de Python `3.11.X` o superior.
Primero, clonar este repositorio y hacer `cd` en la carpeta creada.

### Linux

```bash
python3 -m venv .venv                   # crear entorno
source .venv/bin/activate               # activar entorno
pip install -r requirements.txt         # instalacion dependencias
```

### Windows

```powershell
py -m venv .venv                        # crear entorno
.\.venv\Scripts\Activate.ps1            # activar entorno
pip install -r requirements.txt         # instalacion dependencias
```

## Ejecución

```bash
python3 camera_pygame.py [-options]     # linux
py camera_pygame.py [-h] [-options]     # windows
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
```

### Controles para el modo debug

- `<p>`: tomar foto
- `<q>`: cerrar programa
- `<s>`: mostrar camara
- `<d>`: modo debug
- `<Esc>`: Fullscreen
- `<Arrow Keys>`: Rotar video

## [Opcional] [Linux Only] Ejecución bajo comando

_Ojo_: Se requieren que estén los botones USB conectados previamente y tener una instalación de `antimicrox`

```bash
chmod +x start_pyCamera.sh             # convertir script bash en ejecutable
./start_pyCamera.sh                    # ejecutar script (desde cualquier lugar)
```

### Ejecución global

1. Crear un _symlink_ al ejecutable del repositorio

```bash
mkdir -p ~/bin # crear un directorio de binarios de usuario (si no existe)
ln -s /home/nombre_usuario/pyCamera/start_pyCamera.sh ~/bin/pycamera # crear un symlink (pycamera) al ejecutable original
```

2. Luego se agrega el _symlink_ `pycamera` al `PATH`. Agregar esta linea al final de `~/.bashrc`

```bash
export PATH="$HOME/bin:$PATH"
```

3. Y luego ejecutar

```bash
source ~/.bashrc
```

### Instrucciones para ejecutar en boot

_Ojo_: Intrucciones compatibles solamente con X11

Se asume que existe el ejecutable `start_pyCamera.sh` creado en la sección anterior

1. Crear un archivo `.desktop` con las configuraciones necesarias

```bash
mkdir -p ~/.config/autostart          # crear el directorio (si no existe)
nano pycamera.desktop                 # crear archivo de para iniciar en el escritorio
```

2. El archivo `pycamera.desktop` debe contener:

```txt
[Desktop Entry]
Type=Application
Exec=/home/raspi5/bin/pycamera
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Script de inicio de pyCamera
Comment=Ejecuta pyCamera al inicio
Terminal=true
```
