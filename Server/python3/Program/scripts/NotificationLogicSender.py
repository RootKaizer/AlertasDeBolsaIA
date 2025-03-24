# NotificationLogicSender.py
from typing import Union, Tuple, List, Dict
import configparser

def leer_numeros_whatsapp(ruta_archivo: str = '/app/conf/whatsappNotificationListNumber.info') -> List[str]:
    """
    Lee los números de teléfono desde el archivo de configuración.
    
    Args:
        ruta_archivo: Ruta al archivo con los números de WhatsApp
        
    Returns:
        Lista de números de teléfono
    """
    try:
        with open(ruta_archivo, 'r') as file:
            numeros = [line.strip() for line in file if line.strip()]
        return numeros
    except Exception as e:
        print(f"Error al leer los números de WhatsApp: {e}")
        return []

def comparar_y_notificar(
    resultados_anteriores: Dict,
    resultados_actuales: Dict,
    estrategia: str
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
        mensaje = "No se encontraron resultados anteriores para la ejecución"
        print(mensaje)
        return mensaje

    cambios = []
    
    # Comparar resultados para cada mercado
    for mercado in resultados_actuales:
        if mercado not in resultados_anteriores:
            cambios.append(f"Nuevo mercado: {mercado} - Decisión: {resultados_actuales[mercado]['decision']}")
        elif resultados_actuales[mercado]['decision'] != resultados_anteriores[mercado]['decision']:
            cambios.append(
                f"Cambio en {mercado}: "
                f"De {resultados_anteriores[mercado]['decision']} "
                f"a {resultados_actuales[mercado]['decision']}"
            )

    # Si no hay cambios
    if not cambios:
        return "No se detectaron cambios significativos desde la última ejecución."

    # Si hay cambios, preparar notificación
    numeros = leer_numeros_whatsapp()
    
    if not numeros:
        mensaje = "No hay números configurados para enviar notificaciones."
        print(mensaje)
        return mensaje
    
    mensaje = f"🔔 *Actualización de Trading ({estrategia})* 🔔\n\n" + "\n".join(cambios)
    print(f"Preparado para enviar a {len(numeros)} números:\n{mensaje}")
    
    return numeros, mensaje


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