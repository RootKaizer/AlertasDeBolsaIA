import pandas as pd
from ProcesingDataPandas import calcular_rsi, calcular_macd, calcular_media_movil, calcular_bandas_bollinger, calcular_estocastico

def procesar_dataframes(dataframes, verbose=False):
    """
    Procesa los DataFrames y calcula las métricas técnicas para cada símbolo.
    :param dataframes: Diccionario de DataFrames (símbolo: DataFrame).
    :param verbose: Si es True, muestra detalles de los cálculos realizados
    :return: Diccionario de DataFrames procesados (símbolo: DataFrame).
    """
    dataframes_procesados = {}

    for symbol, df in dataframes.items():
        # Calcular RSI
        if verbose:
            print(f"\n{'='*60}")
            print(f"📊 PROCESANDO INDICADORES TÉCNICOS PARA: {symbol}")
            print(f"{'='*60}")
            print(f"DataFrame inicial - Shape: {df.shape}")
            print(f"Columnas disponibles: {list(df.columns)}")
            if len(df) > 0:
                print(f"Último registro:")
                print(f"  Close: {df['Close'].iloc[-1]}")
                print(f"  High: {df['High'].iloc[-1]}")
                print(f"  Low: {df['Low'].iloc[-1]}")
                print(f"  Volume: {df['Volume'].iloc[-1]}")
                print(f"  Fecha: {df['datetime'].iloc[-1] if 'datetime' in df.columns else df.index[-1]}")

        if verbose:
            print(f"\n{'─'*50}")
            print(f"🔍 CALCULANDO RSI (Relative Strength Index)")
            print(f"{'─'*50}")
            print(f"Función: calcular_rsi(df, periodo=14)")
            print(f"Datos utilizados:")
            print(f"  - Columna: 'Close' (precios de cierre)")
            if len(df) >= 14:
                print(f"  - Últimos 14 valores Close: {df['Close'].tail(14).tolist()}")
                print(f"  - Rango de precios: {df['Close'].min():.2f} - {df['Close'].max():.2f}")
            else:
                print(f"  - Datos insuficientes para cálculo completo (necesarios 14, disponibles: {len(df)})")

        # Ejecutar función para calcular RSI
        df = calcular_rsi(df)
        
        if verbose and 'RSI' in df.columns and len(df) > 0:
            print(f"Resultado RSI:")
            print(f"  - Último valor RSI: {df['RSI'].iloc[-1]:.2f}")
            print(f"  - Valores RSI recientes: {df['RSI'].tail(5).tolist()}")

        # Calcular MACD, MACD Signal y MACD Histogram
        if verbose:
            print(f"\n{'─'*50}")
            print(f"📈 CALCULANDO MACD (Moving Average Convergence Divergence)")
            print(f"{'─'*50}")
            print(f"Función: calcular_macd(df, periodo_corto=12, periodo_largo=26, periodo_senal=9)")
            print(f"Datos utilizados:")
            print(f"  - Columna: 'Close' (precios de cierre)")
            print(f"  - EMA Corto (12): Media exponencial de 12 períodos")
            print(f"  - EMA Largo (26): Media exponencial de 26 períodos")
            print(f"  - Señal (9): Media exponencial de 9 períodos del MACD")
            if len(df) >= 26:
                print(f"  - Últimos precios Close: {df['Close'].tail(26).tolist()}")
        
        # Ejecutar función para calcular MACD
        df = calcular_macd(df)

        if verbose and 'MACD' in df.columns and len(df) > 0:
            print(f"Resultado MACD:")
            print(f"  - Último MACD: {df['MACD'].iloc[-1]:.4f}")
            print(f"  - Última Señal: {df['MACD_signal'].iloc[-1]:.4f}")
            print(f"  - Último Histograma: {df['MACD_hist'].iloc[-1]:.4f}")

        # Calcular Media Móvil
        if verbose:
            print(f"\n{'─'*50}")
            print(f"📊 CALCULANDO MEDIA MÓVIL SIMPLE")
            print(f"{'─'*50}")
            print(f"Función: calcular_media_movil(df, periodo=20)")
            print(f"Datos utilizados:")
            print(f"  - Columna: 'Close' (precios de cierre)")
            print(f"  - Período: 20 (media de últimos 20 cierres)")
            if len(df) >= 20:
                print(f"  - Últimos 20 valores Close: {df['Close'].tail(20).tolist()}")
        
        # Ejecutar función para calcular Media Movil
        df = calcular_media_movil(df)
        
        if verbose and 'MA' in df.columns and len(df) > 0:
            print(f"Resultado Media Móvil:")
            print(f"  - Última Media Móvil (20): {df['MA'].iloc[-1]:.2f}")
            print(f"  - Precio Actual: {df['Close'].iloc[-1]:.2f}")

        # Calcular Bandas de Bollinger
        if verbose:
            print(f"\n{'─'*50}")
            print(f"📏 CALCULANDO BANDAS DE BOLLINGER")
            print(f"{'─'*50}")
            print(f"Función: calcular_bandas_bollinger(df, periodo=20, desviacion=2)")
            print(f"Datos utilizados:")
            print(f"  - Columna: 'Close' (precios de cierre)")
            print(f"  - Período: 20 (media móvil)")
            print(f"  - Desviación: 2 (bandas a 2 desviaciones estándar)")
            if len(df) >= 20:
                print(f"  - Media Móvil 20: {df['Close'].tail(20).mean():.2f}")
                print(f"  - Desviación Estándar: {df['Close'].tail(20).std():.2f}")
        
        # Ejecutar función para calcular Bandas de Bollinger
        df = calcular_bandas_bollinger(df)
        
        if verbose and 'Bollinger_Upper' in df.columns and len(df) > 0:
            print(f"Resultado Bandas Bollinger:")
            print(f"  - Banda Superior: {df['Bollinger_Upper'].iloc[-1]:.2f}")
            print(f"  - Banda Media: {df['Bollinger_MA'].iloc[-1]:.2f}")
            print(f"  - Banda Inferior: {df['Bollinger_Lower'].iloc[-1]:.2f}")
            print(f"  - Precio Actual: {df['Close'].iloc[-1]:.2f}")
            precio = df['Close'].iloc[-1]
            banda_sup = df['Bollinger_Upper'].iloc[-1]
            banda_inf = df['Bollinger_Lower'].iloc[-1]
            if precio > banda_sup:
                print(f"  - Posición: 🔴 SOBRE COMPRA (por encima de banda superior)")
            elif precio < banda_inf:
                print(f"  - Posición: 🟢 SOBRE VENTA (por debajo de banda inferior)")
            else:
                print(f"  - Posición: ⚪ DENTRO DE LAS BANDAS")

        # Calcular Estocástico
        if verbose:
            print(f"\n{'─'*50}")
            print(f"🎯 CALCULANDO ESTOCÁSTICO")
            print(f"{'─'*50}")
            print(f"Función: calcular_estocastico(df, periodo=14)")
            print(f"Datos utilizados:")
            print(f"  - Columnas: 'High', 'Low', 'Close' (máximos, mínimos y cierres)")
            print(f"  - Período: 14 (rango de 14 períodos)")
            if len(df) >= 14:
                print(f"  - Último High: {df['High'].iloc[-1]:.2f}")
                print(f"  - Último Low: {df['Low'].iloc[-1]:.2f}")
                print(f"  - Mínimo 14 períodos: {df['Low'].tail(14).min():.2f}")
                print(f"  - Máximo 14 períodos: {df['High'].tail(14).max():.2f}")
        
        # Ejecutar función para calcular Estocástico
        df = calcular_estocastico(df)

        if verbose and '%K' in df.columns and len(df) > 0:
            print(f"Resultado Estocástico:")
            print(f"  - %K (Línea rápida): {df['%K'].iloc[-1]:.2f}")
            print(f"  - %D (Línea lenta): {df['%D'].iloc[-1]:.2f}")
            k_value = df['%K'].iloc[-1]
            d_value = df['%D'].iloc[-1]
            if k_value > 80 and d_value > 80:
                print(f"  - Señal: 🔴 SOBRECOMPRADO (ambos > 80)")
            elif k_value < 20 and d_value < 20:
                print(f"  - Señal: 🟢 SOBREVENDIDO (ambos < 20)")
            elif k_value > d_value:
                print(f"  - Señal: 🟢 CRUCE ALCISTA (%K > %D)")
            elif k_value < d_value:
                print(f"  - Señal: 🔴 CRUCE BAJISTA (%K < %D)")
            else:
                print(f"  - Señal: ⚪ NEUTRO")

        if verbose:
            print(f"\n{'─'*50}")
            print(f"📋 RESUMEN FINAL - {symbol}")
            print(f"{'─'*50}")
            print(f"Indicadores calculados:")
            indicadores = ['RSI', 'MACD', 'MACD_signal', 'MACD_hist', 'MA', 'Bollinger_Upper', 'Bollinger_Lower', '%K', '%D']
            for indicador in indicadores:
                if indicador in df.columns and len(df) > 0:
                    valor = df[indicador].iloc[-1]
                    print(f"  - {indicador}: {valor:.4f}" if 'MACD' in indicador else f"  - {indicador}: {valor:.2f}")
            
            print(f"DataFrame final - Shape: {df.shape}")
            print(f"Columnas totales: {list(df.columns)}")

        # Guardar el DataFrame procesado
        dataframes_procesados[symbol] = df

    # Resumen general de todos los símbolos
    if verbose:
        print(f"\n{'='*60}")
        print(f"🎉 RESUMEN GENERAL - TODOS LOS SÍMBOLOS")
        print(f"{'='*60}")
        print(f"Total de símbolos procesados: {len(dataframes_procesados)}")
        for symbol, df in dataframes_procesados.items():
            print(f"\n{symbol}:")
            print(f"  - Registros: {len(df)}")
            print(f"  - Columnas: {len(df.columns)}")
            if len(df) > 0:
                print(f"  - Última fecha: {df['datetime'].iloc[-1] if 'datetime' in df.columns else df.index[-1]}")
                print(f"  - Último precio: {df['Close'].iloc[-1]:.2f}")
                if 'RSI' in df.columns:
                    print(f"  - Último RSI: {df['RSI'].iloc[-1]:.2f}")

    return dataframes_procesados

'''
if __name__ == "__main__":
    # Ejemplo de uso (para pruebas)
    datos_historicos = {
        "AAPL": {
            "values": [
                {"datetime": "2025-03-10 15:30:00", "open": "226.99", "high": "228.64", "low": "226.5", "close": "227.54", "volume": "8057482"},
                {"datetime": "2025-03-10 13:30:00", "open": "225.24", "high": "227.51", "low": "224.42", "close": "226.97", "volume": "12470689"}
            ]
        }
    }'

    from ConverterDataToPandasData import convertir_a_dataframe
    dataframes = convertir_a_dataframe(datos_historicos)
    dataframes_procesados = procesar_dataframes(dataframes)

    for symbol, df in dataframes_procesados.items():
        print(f"\nDatos procesados para {symbol}:")
        print(df.tail())'
'''