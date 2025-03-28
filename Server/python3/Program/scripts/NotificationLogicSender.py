# NotificationLogicSender.py
from typing import Union, Tuple, List, Dict, Any
import json
from pathlib import Path
from datetime import datetime
import pytz


def comparar_y_notificar(
    resultados_anteriores: Dict,
    resultados_actuales: Dict,
    estrategia: str,
    mobile_list_notification: str,
    log_whatsapp_message: str
) -> Union[str, Tuple[List[str], str]]:
    """
    Compara los resultados anteriores con los actuales y prepara notificaciones si hay cambios.
    """
    if not resultados_anteriores:
        return "Primera ejecución - No hay resultados anteriores para comparar"

    cambios = []
    comparacion_completa = generar_comparacion_completa(resultados_anteriores, resultados_actuales)
    
    # Verificar si hay cambios
    hay_cambios = False
    for mercado, datos in comparacion_completa.items():
        for indicador, valores in datos['analisis_comparativo'].items():
            if valores['anterior'] != valores['actual']:
                cambios.append(
                    f"Cambio en {mercado} ({indicador}): "
                    f"De {valores['anterior'].get('accion', 'N/A')} "
                    f"a {valores['actual'].get('accion', 'N/A')}"
                )
                hay_cambios = True
    
    if not hay_cambios:
        resultado = "No se detectaron cambios significativos desde la última ejecución."
        numeros = leer_numeros_whatsapp(mobile_list_notification)
        registrar_en_log(log_whatsapp_message, numeros if numeros else [], resultado, list(comparacion_completa.values()), estrategia)
        return resultado if not numeros else (numeros, resultado)

    numeros = leer_numeros_whatsapp(mobile_list_notification)
    if not numeros:
        return "No hay números configurados para enviar notificaciones."
    
    mensaje = f"🔔 *Actualización de Trading ({estrategia})* 🔔\n\n" + "\n".join(cambios)
    registrar_en_log(log_whatsapp_message, numeros, mensaje, list(comparacion_completa.values()), estrategia)
    
    return numeros, mensaje



def generar_comparacion_completa(anteriores: Dict, actuales: Dict) -> Dict[str, Any]:
    """
    Genera una comparación completa de todos los mercados e indicadores.
    """
    todos_mercados = set(anteriores.keys()).union(set(actuales.keys()))
    comparacion = {}
    
    for mercado in todos_mercados:
        datos_anteriores = anteriores.get(mercado, {})
        datos_actuales = actuales.get(mercado, {})
        
        comparacion[mercado] = {
            'mercado': mercado,
            'analisis_comparativo': {}
        }
        
        todos_indicadores = set(datos_anteriores.keys()).union(set(datos_actuales.keys()))
        
        for indicador in todos_indicadores:
            comparacion[mercado]['analisis_comparativo'][indicador] = {
                'anterior': datos_anteriores.get(indicador, {}),
                'actual': datos_actuales.get(indicador, {})
            }
    
    return comparacion



def leer_numeros_whatsapp(ruta_archivo: str) -> List[str]:
    """
    Lee los números de teléfono desde el archivo de configuración.
    """
    try:
        with open(ruta_archivo, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"Error al leer números WhatsApp: {e}")
        return []
    


def registrar_en_log(log_whatsapp_message, numeros: List[str], mensaje: str, cambios: List[Dict[str, Any]], estrategia: str):
    """Registra los detalles del mensaje enviado en un archivo de log."""
    log_file = Path(log_whatsapp_message)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    tz_bogota = pytz.timezone('America/Bogota')
    fecha_hora = datetime.now(tz_bogota).strftime('%Y-%m-%d %H:%M:%S %Z')
    
    log_entry = {
        'fecha_hora': fecha_hora,
        'estrategia': estrategia,
        'numeros_destino': numeros,
        'mensaje': mensaje,
        'comparacion_completa': cambios
    }
    
    try:
        if not log_file.exists():
            # crea un nuevo log
            with open(log_file, 'w') as f:
                json.dump([log_entry], f, indent=4, ensure_ascii=False)
        else:
            # encuentra un log y continua escribiendo
            with open(log_file, 'r+') as f:
                try:
                    data = json.load(f)
                    data.append(log_entry)
                    f.seek(0)
                    json.dump(data, f, indent=4, ensure_ascii=False)
                except json.JSONDecodeError:
                    json.dump([log_entry], f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error al escribir en el archivo de log: {e}")








'''
# Ejemplo de uso para pruebas
if __name__ == "__main__":
    # Datos de prueba
    resultados_test_antes = {
        "AAPL": {"decision": "COMPRA", "precio": 150.50},
        "MSFT": {"decision": "VENTA", "precio": 250.75}
    }
    
    resultados_test_ahora = {
        "AAPL": {"decision": "VENTA", "precio": 152.30},
        "MSFT": {"decision": "VENTA", "precio": 255.20},
        "GOOG": {"decision": "COMPRA", "precio": 2800.00}
    }
    
    # Prueba 1: Con cambios
    print("\nPrueba 1: Con cambios")
    resultado = comparar_y_notificar(
        resultados_test_antes,
        resultados_test_ahora,
        "mediano_plazo"
    )
    print("\nResultado:", resultado)
    
    # Prueba 2: Sin cambios
    print("\nPrueba 2: Sin cambios")
    resultado = comparar_y_notificar(
        resultados_test_ahora,
        resultados_test_ahora,  # Mismos datos
        "mediano_plazo"
    )
    print("\nResultado:", resultado)
    
    # Prueba 3: Primera ejecución
    print("\nPrueba 3: Primera ejecución")
    resultado = comparar_y_notificar(
        None,
        resultados_test_ahora,
        "mediano_plazo"
    )
    print("\nResultado:", resultado)'
'''