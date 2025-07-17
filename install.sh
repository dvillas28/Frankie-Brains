#!/bin/bash
# filepath: /home/dvillasc/Frankie-Brains/install.sh

# Variables
SCRIPT_NAME="start_pyCamera.sh"
SYMLINK_NAME="pycamera"
BIN_DIR="$HOME/bin"
DESKTOP_FILE="$HOME/.config/autostart/pycamera.desktop"

# Verificar si el script start_pyCamera.sh existe
if [ ! -f "$SCRIPT_NAME" ]; then
    echo "Error: El script $SCRIPT_NAME no existe en el directorio actual."
    exit 1
fi

# Hacer que el script sea ejecutable
chmod +x "$SCRIPT_NAME"
echo "El script $SCRIPT_NAME ahora es ejecutable."

# Crear el directorio bin si no existe
mkdir -p "$BIN_DIR"
echo "Directorio $BIN_DIR creado o ya existente."

# Crear el symlink en ~/bin
ln -sf "$(pwd)/$SCRIPT_NAME" "$BIN_DIR/$SYMLINK_NAME"
echo "Symlink creado: $BIN_DIR/$SYMLINK_NAME -> $(pwd)/$SCRIPT_NAME"

# Agregar ~/bin al PATH si no está ya configurado
if ! grep -q 'export PATH="$HOME/bin:$PATH"' "$HOME/.bashrc"; then
    echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.bashrc"
    echo "Se agregó $BIN_DIR al PATH en ~/.bashrc."
    source "$HOME/.bashrc"
else
    echo "$BIN_DIR ya está en el PATH."
fi

# Crear el archivo .desktop para ejecución al inicio
mkdir -p "$(dirname "$DESKTOP_FILE")"
cat > "$DESKTOP_FILE" <<EOL
[Desktop Entry]
Type=Application
Exec=$BIN_DIR/$SYMLINK_NAME
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Script de inicio de pyCamera
Comment=Ejecuta pyCamera al inicio
Terminal=true
EOL
echo "Archivo .desktop creado en $DESKTOP_FILE."

echo "Instalación completada. Puedes ejecutar el programa con el comando: $SYMLINK_NAME"