import configparser
from typing import Tuple, List, Dict, Optional
from DebugMotorBolsaIA import DebugMotorBolsaIA  # Importar la clase Debug

def leer_numeros_whatsapp():
    """
    Lee los números de teléfono desde el archivo de configuración.
    :return: Lista de números de teléfono.
    """
    try:
        with open('/app/conf/whatsappNotificationListNumber.info', 'r') as file:
            numeros = [line.strip() for line in file if line.strip()]
        return numeros
    except Exception as e:
        print(f"Error al leer los números de WhatsApp: {e}")
        return []



def comparar_y_notificar(resultados_anteriores, resultados_actuales, estrategia):
    """
    Compara los resultados anteriores con los actuales y envía notificaciones si hay cambios.
    :param resultados_anteriores: Diccionario con los resultados anteriores.
    :param resultados_actuales: Diccionario con los resultados actuales.
    :param estrategia: Nombre de la estrategia usada.
    """
    if not resultados_anteriores:
        # Primera ejecución, no hay comparación posible
        mensaje = f"No se encontraron resultados anteriores para la ejecución"
        print(f"{mensaje}")
        return mensaje

    cambios = []
    
    # Comparar resultados para cada mercado
    for mercado in resultados_actuales:
        if mercado not in resultados_anteriores:
            cambios.append(f"Nuevo mercado: {mercado} - Decisión: {resultados_actuales[mercado]['decision']}")
        else:
            if resultados_actuales[mercado]['decision'] != resultados_anteriores[mercado]['decision']:
                cambios.append(
                    f"Cambio en {mercado}: "
                    f"De {resultados_anteriores[mercado]['decision']} "
                    f"a {resultados_actuales[mercado]['decision']}"
                )

    if cambios:
        numeros = leer_numeros_whatsapp()
        if numeros:
            mensaje = f"🔔 *Actualización de Trading ({estrategia})* 🔔\n\n" + "\n".join(cambios)
            print(f"numeros: {numeros}\n mensaje: {mensaje}")
            #whatsapp(numeros, mensaje)
            return numeros, mensaje

        else:
            mensaje = f"No hay números configurados para enviar notificaciones.\nAgregarlos en el archivo /app/conf/whatsappNotificationListNumber.info"
            print(f"{mensaje}")
            return mensaje
