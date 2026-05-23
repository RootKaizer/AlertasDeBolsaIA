import os

import os
from datetime import datetime

def limpiar_log(log_file):
    """Borra el archivo de log si existe y lo crea vacío. Si el directorio no existe, lo crea."""
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
        os.chmod(log_dir, 0o777)  # Permisos para el directorio
    
    with open(log_file, "w") as f:
        f.write("")
    os.chmod(log_file, 0o666)  # Establecer permisos rw-rw-rw-

def escribir_log(log_file, mensaje):
    """Escribe un mensaje en el archivo de log."""
    with open(log_file, "a") as f:
        f.write(mensaje + "\n")

def formato_paso(numero_paso, nombre_paso, detalles=None):
    """Formatea la información de un paso para el log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensaje = f"[{timestamp}] PASO {numero_paso}: {nombre_paso}"
    if detalles:
        mensaje += f" - {detalles}"
    return mensaje