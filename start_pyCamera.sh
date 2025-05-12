#!/bin/bash

PROJECT_DIR="/home/raspi5/pyCamera"

# Activar entorno virtual
source "$PROJECT_DIR/.venv/bin/activate"

# Lanzar antimicrox
antimicrox --hidden --profile "$PROJECT_DIR/botones.joystick.amgp" & ANTIMICROX_PID=$!

# Ejecutar el programa
python3 "$PROJECT_DIR/main.py" -o O -q 1

# Finalizar antimicrox
kill $ANTIMICROX_PID