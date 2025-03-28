# NotificationLogicSender.py
from typing import Union, Tuple, List, Dict
import configparser
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
    
    Args:
        resultados_anteriores: Diccionario con los resultados anteriores
        resultados_actuales: Diccionario con los resultados actuales
        estrategia: Nombre de la estrategia usada
        
    Returns:
        str: Mensaje de estado si no hay cambios o números
        Tuple[List[str], str]: Lista de números y mensaje si hay cambios
    """
    # Caso: primera ejecución sin resultados anteriores
    if not resultados_anteriores:
        return "Primera ejecución - No hay resultados anteriores para comparar"

    cambios = []
    cambios_detallados = []
    
    # Comparar resultados para cada mercado de forma segura
    for mercado, datos_actuales in resultados_actuales.items():
        # Verificar si existe la clave 'decision' en los datos actuales
        if 'decision' not in datos_actuales:
            continue
            
        # Caso: nuevo mercado
        if mercado not in resultados_anteriores:
            cambios.append(f"Nuevo mercado: {mercado} - Decisión: {datos_actuales['decision']}")
            cambios_detallados.append({
                'mercado': mercado,
                'tipo': 'nuevo',
                'anterior': None,
                'actual': datos_actuales['decision']
            })
        else:
            # Verificar si existe la clave 'decision' en los datos anteriores
            datos_anteriores = resultados_anteriores.get(mercado, {})
            if 'decision' in datos_anteriores and datos_anteriores['decision'] != datos_actuales['decision']:
                cambios.append(
                    f"Cambio en {mercado}: "
                    f"De {datos_anteriores['decision']} "
                    f"a {datos_actuales['decision']}"
                )
                cambios_detallados.append({
                    'mercado': mercado,
                    'tipo': 'cambio',
                    'anterior': datos_anteriores['decision'],
                    'actual': datos_actuales['decision']
                })

    # Leer números de WhatsApp
    numeros = leer_numeros_whatsapp(mobile_list_notification)
    
    if not numeros:
        return "No hay números configurados para enviar notificaciones."
    
    # Si no hay cambios
    if not cambios:
        mensaje = "No se detectaron cambios significativos desde la última ejecución."
        # solo activar si quieres depurar mensaje que va para el whatsapp
        registrar_en_log(log_whatsapp_message, numeros, mensaje, cambios_detallados, estrategia)
        return mensaje
    
    # Construir mensaje final
    mensaje = f"🔔 *Actualización de Trading ({estrategia})* 🔔\n\n" + "\n".join(cambios)

    # Registrar en el log solo si hay cambios y números
    registrar_en_log(log_whatsapp_message, numeros, mensaje, cambios_detallados, estrategia)

    return numeros, mensaje



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
    


def registrar_en_log(log_whatsapp_message: str, numeros: List[str], mensaje: str, cambios: List[Dict], estrategia: str):
    """
    Registra los detalles del mensaje enviado en un archivo de log.
    
    Args:
        numeros: Lista de números a los que se envió el mensaje
        mensaje: Mensaje enviado
        cambios: Lista de diccionarios con los cambios detectados
        estrategia: Estrategia utilizada
    """
    log_file = Path(log_whatsapp_message)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Obtener fecha y hora actual en zona horaria de Bogotá
    tz_bogota = pytz.timezone('America/Bogota')
    fecha_hora = datetime.now(tz_bogota).strftime('%Y-%m-%d %H:%M:%S %Z')
    
    # Crear entrada de log
    log_entry = {
        'fecha_hora': fecha_hora,
        'estrategia': estrategia,
        'numeros_destino': numeros,
        'mensaje': mensaje,
        'cambios': cambios
    }
    
    # Escribir en el archivo de log
    try:
        with open(log_file, 'a') as f:
            # Si el archivo está vacío, comenzamos con un array JSON
            if log_file.stat().st_size == 0:
                f.write('[\n')
                json.dump(log_entry, f, indent=4, ensure_ascii=False)
            else:
                # Si no está vacío, agregamos una coma y la nueva entrada
                f.write(',\n')
                json.dump(log_entry, f, indent=4, ensure_ascii=False)
            
            # Cerramos el array JSON si es la primera vez que escribimos
            if log_file.stat().st_size == 0:
                f.write('\n]')
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