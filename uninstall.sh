#!/bin/bash
# filepath: /home/dvillasc/Frankie-Brains/uninstall.sh

# Variables
SYMLINK_NAME="pycamera"
BIN_DIR="$HOME/bin"
DESKTOP_FILE="$HOME/.config/autostart/pycamera.desktop"

# Eliminar el symlink en ~/bin
if [ -L "$BIN_DIR/$SYMLINK_NAME" ]; then
    rm "$BIN_DIR/$SYMLINK_NAME"
    echo "Symlink $BIN_DIR/$SYMLINK_NAME eliminado."
else
    echo "Symlink $BIN_DIR/$SYMLINK_NAME no encontrado."
fi

# Eliminar el archivo .desktop para ejecución al inicio
if [ -f "$DESKTOP_FILE" ]; then
    rm "$DESKTOP_FILE"
    echo "Archivo .desktop $DESKTOP_FILE eliminado."
else
    echo "Archivo .desktop $DESKTOP_FILE no encontrado."
fi

# Verificar si el directorio ~/bin está vacío y eliminarlo si es necesario
if [ -d "$BIN_DIR" ] && [ -z "$(ls -A "$BIN_DIR")" ]; then
    rmdir "$BIN_DIR"
    echo "Directorio $BIN_DIR eliminado porque estaba vacío."
else
    echo "Directorio $BIN_DIR no está vacío o no existe, no se eliminó."
fi

# Nota sobre PATH
echo "Nota: Si deseas eliminar $BIN_DIR del PATH, edita manualmente ~/.bashrc y elimina la línea: export PATH=\"\$HOME/bin:\$PATH\""

echo "Desinstalación completada."