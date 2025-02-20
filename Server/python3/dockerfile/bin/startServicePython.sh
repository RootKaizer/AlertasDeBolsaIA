#!/bin/bash

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


# validación proceso de python3
ps -fea |grep python3  >> "$LOG_FILE"
