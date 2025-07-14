#!/bin/bash

# El nombre 'pyCamera' viene del nombre antiguo del proyecto y es el nombre del directorio actualmente
# en la Raspi. 
# TODO: Cambiar a 'Frankie-Brains' cuando sea necesario (crear nuevamente el ejecutable y la ejecución en boot)
PROJECT_DIR="/home/$USER/pyCamera"

# Activar entorno virtual
source "$PROJECT_DIR/.venv/bin/activate"

# Lanzar antimicrox
antimicrox --hidden --profile "$PROJECT_DIR/botones.joystick.amgp" & ANTIMICROX_PID=$!

# Ejecutar el programa
python3 "$PROJECT_DIR/main.py" -o E -q 1 -a gemini

# Finalizar antimicrox
kill $ANTIMICROX_PID