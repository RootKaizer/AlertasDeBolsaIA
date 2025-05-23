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
        return F"vender", f"RSI({rsi:.2f}) está por encima del umbral superior({rsi_upper:.2f}), indicando sobrecompra."
    elif rsi < rsi_under:
        return "comprar", f"RSI({rsi:.2f}) está por debajo del umbral inferior({rsi_under:.2f}), indicando sobreventa."
    else:
        return "hold", f"RSI({rsi:.2f}) está dentro del rango normal ({rsi_under:.2f} < RSI < {rsi_upper:.2f}), no se recomienda acción."

def determinar_accion_macd(macd, macd_signal):
    """
    Determina la acción a tomar basada en el MACD.
    :param macd: Valor del MACD.
    :param macd_signal: Valor de la señal MACD.
    :return: Acción recomendada (str) y descripción (str).
    """
    if macd > macd_signal:
        return "comprar", f"MACD({macd:.2f}) está por encima de la señal({macd_signal:.2f}), indicando tendencia alcista."
    elif macd < macd_signal:
        return "vender", f"MACD({macd:.2f}) está por debajo de la señal({macd_signal:.2f}), indicando tendencia bajista."
    else:
        return "hold", f"MACD({macd:.2f}) es igual a la señal({macd_signal:.2f}), indicando estabilidad."

def determinar_accion_precio(precio_actual, precio_anterior):
    """
    Determina la acción a tomar basada en el precio.
    :param precio_actual: Precio actual de cierre.
    :param precio_anterior: Precio de cierre anterior.
    :return: Acción recomendada (str) y descripción (str).
    """
    if precio_actual > precio_anterior:
        return f"comprar", f"El precio actual({precio_actual:.2f}) es mayor que el anterior({precio_anterior:.2f}), indicando tendencia alcista."
    elif precio_actual < precio_anterior:
        return f"vender", f"El precio actual({precio_actual:.2f}) es menor que el anterior({precio_anterior:.2f}), indicando tendencia bajista."
    else:
        return f"hold", f"El precio actual({precio_actual:.2f}) es meigual que el anterior({precio_anterior:.2f}), indicando estabilidad."

def determinar_accion_estocastico(estocastico_k, estocastico_d):
    """
    Determina la acción a tomar basada en el Estocástico.
    :param estocastico_k: Valor del %K del Estocástico.
    :param estocastico_d: Valor del %D del Estocástico.
    :return: Acción recomendada (str) y descripción (str).
    """
    if estocastico_k > estocastico_d:
        return "comprar", f"%K({estocastico_k:.2f}) está por encima de %D({estocastico_d:.2f}), indicando tendencia alcista."
    elif estocastico_k < estocastico_d:
        return "vender", f"%K({estocastico_k:.2f}) está por debajo de %D({estocastico_d:.2f}), indicando tendencia bajista."
    else:
        return "vender", f"%K({estocastico_k:.2f}) es igual al %D({estocastico_d:.2f}), indicando estabilidad."



def analizar_dataframes(dataframes_procesados, rsi_under=30, rsi_upper=70):
    """
    Analiza los DataFrames procesados y devuelve un diccionario con los resultados del análisis.
    :param dataframes_procesados: Diccionario de DataFrames procesados, donde las claves son los símbolos.
    :param rsi_under: Umbral inferior para el RSI (por defecto 30).
    :param rsi_upper: Umbral superior para el RSI (por defecto 70).
    :return: Diccionario con los resultados del análisis por símbolo.
    """
    resultados_trading = {}  # Diccionario para almacenar las acciones recomendadas por símbolo

    for symbol, df in dataframes_procesados.items():
        print(f"\nAnalizando {symbol}...")

        # Obtener los últimos valores para aplicar la lógica de trading
        rsi = df['RSI'].iloc[-1]
        macd = df['MACD'].iloc[-1]
        macd_signal = df['MACD_signal'].iloc[-1]
        precio_actual = df['Close'].iloc[-1]
        precio_anterior = df['Close'].iloc[-2]
        estocastico_k = df['%K'].iloc[-1]
        estocastico_d = df['%D'].iloc[-1]

        # Determinar las acciones individuales
        accion_rsi, descripcion_rsi = determinar_accion_rsi(rsi, rsi_under, rsi_upper)
        accion_macd, descripcion_macd = determinar_accion_macd(macd, macd_signal)
        accion_precio, descripcion_precio = determinar_accion_precio(precio_actual, precio_anterior)
        accion_estocastico, descripcion_estocastico = determinar_accion_estocastico(estocastico_k, estocastico_d)

        # Guardar los resultados (acciones y descripciones)
        resultados_trading[symbol] = {
            "RSI": {"accion": accion_rsi, "descripcion": descripcion_rsi},
            "MACD": {"accion": accion_macd, "descripcion": descripcion_macd},
            "Precio": {"accion": accion_precio, "descripcion": descripcion_precio},
            "Estocástico": {"accion": accion_estocastico, "descripcion": descripcion_estocastico}
        }

    return resultados_trading

'''
if __name__ == "__main__":
    # Ejemplo de datos de prueba
    import pandas as pd

    # Crear un DataFrame de ejemplo
    data = {
        'RSI': [35, 40, 45],
        'MACD': [0.5, 0.6, 0.7],
        'MACD_signal': [0.4, 0.5, 0.6],
        'Close': [100, 105, 110],
        '%K': [80, 85, 90],
        '%D': [75, 80, 85]
    }
    df_ejemplo = pd.DataFrame(data)

    # Crear un diccionario de DataFrames procesados (simulando dataframes_procesados)
    dataframes_procesados = {
        "AAPL": df_ejemplo,
        "GOOGL": df_ejemplo
    }

    # Llamar a la función analizar_dataframes con los datos de prueba
    resultados_trading = analizar_dataframes(dataframes_procesados, rsi_under=30, rsi_upper=70)

    # Mostrar los resultados
    print("\nResultados del análisis:")
    for symbol, acciones in resultados_trading.items():
        print(f"\n{symbol}:")
        print(f"  RSI: Acción: {acciones['RSI']['accion']} - Descripción: {acciones['RSI']['descripcion']}")
        print(f"  MACD: Acción: {acciones['MACD']['accion']} - Descripción: {acciones['MACD']['descripcion']}")
        print(f"  Precio: Acción: {acciones['Precio']['accion']} - Descripción: {acciones['Precio']['descripcion']}")
        print(f"  Estocástico: Acción: {acciones['Estocástico']['accion']} - Descripción: {acciones['Estocástico']['descripcion']}")
        
'''