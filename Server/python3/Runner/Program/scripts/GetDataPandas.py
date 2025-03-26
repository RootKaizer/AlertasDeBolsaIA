import pandas as pd
from ProcesingDataPandas import calcular_rsi, calcular_macd, calcular_media_movil, calcular_bandas_bollinger, calcular_estocastico

def procesar_dataframes(dataframes):
    """
    Procesa los DataFrames y calcula las métricas técnicas para cada símbolo.
    :param dataframes: Diccionario de DataFrames (símbolo: DataFrame).
    :return: Diccionario de DataFrames procesados (símbolo: DataFrame).
    """
    dataframes_procesados = {}

    for symbol, df in dataframes.items():
        print(f"\nProcesando {symbol}...")

        # Calcular RSI
        df = calcular_rsi(df)
        print(f"RSI calculado para {symbol}.")

        # Calcular MACD, MACD Signal y MACD Histogram
        df = calcular_macd(df)
        print(f"MACD calculado para {symbol}.")

        # Calcular Media Móvil
        df = calcular_media_movil(df)
        print(f"Media Móvil calculada para {symbol}.")

        # Calcular Bandas de Bollinger
        df = calcular_bandas_bollinger(df)
        print(f"Bandas de Bollinger calculadas para {symbol}.")

        # Calcular Estocástico
        df = calcular_estocastico(df)
        print(f"Estocástico calculado para {symbol}.")

        # Guardar el DataFrame procesado
        dataframes_procesados[symbol] = df

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