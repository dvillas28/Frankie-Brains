# pyCamera

Daniel Villaseñor C.

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

### Controles

- `<p>: tomar foto`
- `<q>: cerrar programa`
- `<s>: mostrar camara`
- `<d>: modo debug`
- `<Esc>: Fullscreen`
- `<Arrow Keys>: Rotar video`

## [Opcional] Configurar programa para ejecuión en boot
