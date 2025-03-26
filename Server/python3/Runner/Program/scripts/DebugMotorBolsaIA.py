import os
import datetime
from helpers.debug_file import escribir_log, limpiar_log
from styles.debug_file import titulo_log, separador_log, formato_paso, formato_parametros, formato_respuesta

class DebugMotorBolsaIA:
    def __init__(self, log_file="../logs/00_MotorBolsaIA.log"):
        # Obtener ruta absoluta y mostrarla
        self.log_file = os.path.abspath(log_file)
        print(f"Ruta del archivo de log: {self.log_file}")  # <-- Nueva línea para debug
        
        # Verificar/crear directorio
        log_dir = os.path.dirname(self.log_file)
        if not os.path.exists(log_dir):
            print(f"Creando directorio: {log_dir}")  # <-- Nueva línea para debug
            os.makedirs(log_dir, exist_ok=True)
        
        limpiar_log(self.log_file)
        self._escribir_titulo()

    def _escribir_titulo(self):
        """Escribe el título del archivo de log con la fecha y hora actual."""
        titulo = titulo_log("00_MotorBolsaIA.py", datetime.datetime.now())
        escribir_log(self.log_file, titulo)

    def escribir_configuracion(self, config):
        """Escribe la configuración con la que se ejecutó el script."""
        escribir_log(self.log_file, "Configuración:")
        for key, value in config.items():
            escribir_log(self.log_file, f"  {key}: {value}")
        escribir_log(self.log_file, separador_log())

    def escribir_paso(self, paso, funcion, parametros, respuesta=None, calculo=None):
        """Escribe los detalles de un paso del proceso."""
        escribir_log(self.log_file, formato_paso(paso))
        escribir_log(self.log_file, f"  Función: {funcion}")
        escribir_log(self.log_file, formato_parametros(parametros))
        if respuesta:
            escribir_log(self.log_file, formato_respuesta(respuesta))
        if calculo:
            escribir_log(self.log_file, f"  Cálculo: {calculo['formula']}")
            escribir_log(self.log_file, f"  Valores: {calculo['valores']}")
            escribir_log(self.log_file, f"  Resultado: {calculo['resultado']}")
        escribir_log(self.log_file, separador_log())