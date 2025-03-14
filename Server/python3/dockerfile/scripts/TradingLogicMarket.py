import sys

def determinar_accion_rsi(rsi, rsi_under=30, rsi_upper=70):
    """
    Determina la acción a tomar basada en el RSI.
    :param rsi: Valor del RSI.
    :param rsi_under: Umbral inferior para comprar (por defecto 30).
    :param rsi_upper: Umbral superior para vender (por defecto 70).
    :return: Acción recomendada (str) y descripción (str).
    """
    if rsi > rsi_upper:
        return "vender", "RSI está por encima del umbral superior, indicando sobrecompra."
    elif rsi < rsi_under:
        return "comprar", "RSI está por debajo del umbral inferior, indicando sobreventa."
    else:
        return "hold", "RSI está dentro del rango normal, no se recomienda acción."

def determinar_accion_macd(macd, macd_signal):
    """
    Determina la acción a tomar basada en el MACD.
    :param macd: Valor del MACD.
    :param macd_signal: Valor de la señal MACD.
    :return: Acción recomendada (str) y descripción (str).
    """
    if macd > macd_signal:
        return "comprar", "MACD está por encima de la señal, indicando tendencia alcista."
    else:
        return "vender", "MACD está por debajo de la señal, indicando tendencia bajista."

def determinar_accion_precio(precio_actual, precio_anterior):
    """
    Determina la acción a tomar basada en el precio.
    :param precio_actual: Precio actual de cierre.
    :param precio_anterior: Precio de cierre anterior.
    :return: Acción recomendada (str) y descripción (str).
    """
    if precio_actual > precio_anterior:
        return "comprar", "El precio actual es mayor que el anterior, indicando tendencia alcista."
    else:
        return "vender", "El precio actual es menor que el anterior, indicando tendencia bajista."

def determinar_accion_estocastico(estocastico_k, estocastico_d):
    """
    Determina la acción a tomar basada en el Estocástico.
    :param estocastico_k: Valor del %K del Estocástico.
    :param estocastico_d: Valor del %D del Estocástico.
    :return: Acción recomendada (str) y descripción (str).
    """
    if estocastico_k > estocastico_d:
        return "comprar", "%K está por encima de %D, indicando tendencia alcista."
    else:
        return "vender", "%K está por debajo de %D, indicando tendencia bajista."


'''
if __name__ == "__main__":
    # Verificar que se hayan proporcionado los argumentos necesarios
    if len(sys.argv) < 8:
        print("Uso: python TradingLogicMarket.py <rsi> <macd> <macd_signal> <precio_actual> <precio_anterior> <estocastico_k> <estocastico_d>")
        sys.exit(1)

    # Obtener los valores de los argumentos
    rsi = float(sys.argv[1])
    macd = float(sys.argv[2])
    macd_signal = float(sys.argv[3])
    precio_actual = float(sys.argv[4])
    precio_anterior = float(sys.argv[5])
    estocastico_k = float(sys.argv[6])
    estocastico_d = float(sys.argv[7])

    # Determinar las acciones individuales
    accion_rsi = determinar_accion_rsi(rsi)
    accion_macd = determinar_accion_macd(macd, macd_signal)
    accion_precio = determinar_accion_precio(precio_actual, precio_anterior)
    accion_estocastico = determinar_accion_estocastico(estocastico_k, estocastico_d)

    # Imprimir los resultados individuales
    print(f"Análisis RSI: Acción: {accion_rsi['accion']}, Descripción: {accion_rsi['description']}")
    print(f"Análisis MACD: Acción: {accion_macd['accion']}, Descripción: {accion_macd['description']}")
    print(f"Análisis Precio: Acción: {accion_precio['accion']}, Descripción: {accion_precio['description']}")
    print(f"Análisis Estocástico: Acción: {accion_estocastico['accion']}, Descripción: {accion_estocastico['description']}")'
'''