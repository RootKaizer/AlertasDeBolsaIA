import pandas as pd
from ProcesingDataPandas import calcular_rsi, calcular_macd, calcular_media_movil, calcular_bandas_bollinger, calcular_estocastico

def procesar_dataframes(dataframes, verbose=False, **kwargs):
    """
    Procesa los DataFrames y calcula las métricas técnicas para cada símbolo.
    :param dataframes: Diccionario de DataFrames (símbolo: DataFrame).
    :param verbose: Si es True, muestra detalles de los cálculos realizados
    :param kwargs: Parámetros para los indicadores técnicos
    :return: Diccionario de DataFrames procesados (símbolo: DataFrame).
    """

    # Extraer parámetros con valores por defecto
    rsi_periodo = kwargs.get('rsi_periodo', 14)
    macd_periodo_corto = kwargs.get('macd_periodo_corto', 12)
    macd_periodo_largo = kwargs.get('macd_periodo_largo', 26)
    macd_periodo_senal = kwargs.get('macd_periodo_senal', 9)
    media_movil_periodo = kwargs.get('media_movil_periodo', 20)
    bollinger_periodo = kwargs.get('bollinger_periodo', 20)
    bollinger_desviacion = kwargs.get('bollinger_desviacion', 2.0)
    estocastico_periodo = kwargs.get('estocastico_periodo', 14)
    
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
            print(f"\n{'='*60}")
            print(f"📊 PROCESANDO INDICADORES TÉCNICOS PARA: {symbol}")
            print(f"{'='*60}")
            print(f"DataFrame inicial - Shape: {df.shape}")
            print(f"Parámetros de la estrategia:")
            print(f"  - RSI período: {rsi_periodo}")
            print(f"  - MACD: {macd_periodo_corto}/{macd_periodo_largo}/{macd_periodo_senal}")
            print(f"  - Media Móvil: {media_movil_periodo}")
            print(f"  - Bollinger: {bollinger_periodo}/{bollinger_desviacion}")
            print(f"  - Estocástico: {estocastico_periodo}")

        
        # Calcular RSI con parámetros específicos
        df = calcular_rsi(df, periodo=rsi_periodo, verbose=verbose, symbol=symbol)

        # Calcular MACD con parámetros específicos
        df = calcular_macd(df, 
                          periodo_corto=macd_periodo_corto, 
                          periodo_largo=macd_periodo_largo, 
                          periodo_senal=macd_periodo_senal, 
                          verbose=verbose, 
                          symbol=symbol)

        # Calcular Media Móvil con parámetros específicos
        df = calcular_media_movil(df, periodo=media_movil_periodo, verbose=verbose, symbol=symbol)

        # Calcular Bandas de Bollinger con parámetros específicos
        df = calcular_bandas_bollinger(df, 
                                     periodo=bollinger_periodo, 
                                     desviacion=bollinger_desviacion, 
                                     verbose=verbose, 
                                     symbol=symbol)

        # Calcular Estocástico con parámetros específicos
        df = calcular_estocastico(df, periodo=estocastico_periodo, verbose=verbose, symbol=symbol)

        

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