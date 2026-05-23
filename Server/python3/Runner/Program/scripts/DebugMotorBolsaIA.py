import os
import logging  # Agregar esta importación
from datetime import datetime

class DebugMotorBolsaIA:
    def __init__(self, modo_debug=False, log_file=None):
        self.modo_debug = modo_debug
        # Asegurar que log_file tenga un valor por defecto si es None
        self.log_file = log_file or "/app/logs/00_MotorBolsaIA.log"
        
        # Configurar logging si se proporciona archivo de log
        if self.log_file:
            # Crear directorio si no existe
            log_dir = os.path.dirname(self.log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
                
            logging.basicConfig(
                filename=self.log_file,
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
    
    def escribir_paso(self, numero_paso, nombre_paso, detalles=None):
        """Escribe información de un paso del proceso"""
        mensaje = f"PASO {numero_paso}: {nombre_paso}"
        if detalles:
            mensaje += f" - {detalles}"
        
        if self.modo_debug:
            print(f"🔍 {mensaje}")
        
        # Escribir en archivo de log usando la función helper
        from helpers.debug_file import escribir_log, formato_paso
        escribir_log(self.log_file, formato_paso(numero_paso, nombre_paso, detalles))
    
    def escribir_info(self, mensaje):
        """Escribe mensaje informativo"""
        if self.modo_debug:
            print(f"🔍 {mensaje}")
        if self.log_file:
            logging.info(mensaje)
    
    def escribir_error(self, contexto, error):
        """Escribe mensaje de error"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mensaje_error = f"❌ ERROR en {contexto}: {error}"
        
        print(f"{timestamp} {mensaje_error}")
        if self.log_file:
            logging.error(f"{contexto}: {error}")
    
    def escribir_advertencia(self, mensaje):
        """Escribe mensaje de advertencia"""
        if self.modo_debug:
            print(f"⚠️  {mensaje}")
        if self.log_file:
            logging.warning(mensaje)
    
    def escribir_exito(self, mensaje):
        """Escribe mensaje de éxito"""
        if self.modo_debug:
            print(f"✅ {mensaje}")
        if self.log_file:
            logging.info(f"SUCCESS: {mensaje}")
