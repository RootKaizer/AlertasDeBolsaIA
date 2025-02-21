#!/bin/bash

# Verificar si el script se ejecuta con sh en lugar de bash
if [ -z "$BASH_VERSION" ]; then
    echo "Error: Este script debe ejecutarse con bash y no con sh." >&2
    exit 1
fi

# Variables
LIBRARY_NAME="TA-Lib"
LOG_FILE="/tmp/logs/startServicepython.log"

# Crear directorio de logs si no existe
mkdir -p "$(dirname "$LOG_FILE")"

# Función para registrar mensajes en el log con separación de procesos
log_message() {
    echo "=================================================" >> "$LOG_FILE"
    echo "[Proceso: $1]" >> "$LOG_FILE"
    echo "=================================================" >> "$LOG_FILE"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] - $2" >> "$LOG_FILE"
}


# Iniciar Python3 en segundo plano
log_message "Inicio de Python3" "Iniciando Python3..."

python3 -m venv /tmp/venv  >> "$LOG_FILE"
source /tmp/venv/bin/activate >> "$LOG_FILE"


# Validar entorno virtual
if [ ! -f /tmp/venv/bin/python3 ]; then
    log_message "Error" "No se encontró el binario de Python en el entorno virtual"
    exit 1
fi
