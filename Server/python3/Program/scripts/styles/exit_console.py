# styles/exit_console.py

def mostrar_resultados_trading(estrategia, resultados_trading, tiempo_ejecucion):
    """
    Muestra los resultados del análisis de trading en la consola.
    :param estrategia: Nombre de la estrategia utilizada.
    :param resultados_trading: Diccionario con los resultados del análisis por símbolo.
    """
    print(f"Estrategia Analizada: {estrategia} \nResultados {tiempo_ejecucion}:")
    for symbol, acciones in resultados_trading.items():
        print(f"\n{symbol}:")
        print(f"  RSI: Acción: {acciones['RSI']['accion']} - Descripción: {acciones['RSI']['descripcion']}")
        print(f"  MACD: Acción: {acciones['MACD']['accion']} - Descripción: {acciones['MACD']['descripcion']}")
        print(f"  Precio: Acción: {acciones['Precio']['accion']} - Descripción: {acciones['Precio']['descripcion']}")
        print(f"  Estocástico: Acción: {acciones['Estocástico']['accion']} - Descripción: {acciones['Estocástico']['descripcion']}")