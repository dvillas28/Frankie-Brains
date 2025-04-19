# pyCamera

Daniel Villaseñor C.

## Ejecución

```bash
python3 camera_pygame.py [-h] [-q] [-o] # linux
py camera_pygame.py [-h] [-q] [-o]      # windows
```

```
options:
  -h, --help            show this help message and exit
  -q {0,1}, --quality {0,1}
                        Parametro de calidad de la camara. Low: 0, High: 1. Valor default: 0
  -o {n,o,s,e}, --orientation {n,o,s,e}
                        Parametro de orientación de la camara. Valor default: n (norte)   
```

## Controles

- `p: Tomar foto`
- `<Esc>: Fullscreen`
- `<Arrow Keys>: Rotar video`
- `q: Cerrar programa`
