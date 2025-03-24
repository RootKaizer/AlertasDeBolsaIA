import pandas as pd
import numpy as np

def calcular_rsi(df, periodo=14):
    """
    Calcula el RSI (Relative Strength Index) para un DataFrame de pandas.
    :param df: DataFrame con datos de mercado.
    :param periodo: Período para calcular el RSI (por defecto 14).
    :return: DataFrame con una columna adicional 'RSI'.
    """
    delta = df['Close'].diff()
    ganancia = (delta.where(delta > 0, 0)).rolling(window=periodo).mean()
    perdida = (-delta.where(delta < 0, 0)).rolling(window=periodo).mean()
    
    rs = ganancia / perdida
    rsi = 100 - (100 / (1 + rs))
    
    df['RSI'] = rsi
    return df

def calcular_macd(df, periodo_corto=12, periodo_largo=26, periodo_senal=9):
    """
    Calcula el MACD, la señal MACD y el histograma MACD para un DataFrame de pandas.
    :param df: DataFrame con datos de mercado.
    :param periodo_corto: Período corto para el MACD (por defecto 12).
    :param periodo_largo: Período largo para el MACD (por defecto 26).
    :param periodo_senal: Período para la señal MACD (por defecto 9).
    :return: DataFrame con columnas adicionales 'MACD', 'MACD_signal' y 'MACD_hist'.
    """
    df['MACD'] = df['Close'].ewm(span=periodo_corto, adjust=False).mean() - df['Close'].ewm(span=periodo_largo, adjust=False).mean()
    df['MACD_signal'] = df['MACD'].ewm(span=periodo_senal, adjust=False).mean()
    df['MACD_hist'] = df['MACD'] - df['MACD_signal']
    return df

def calcular_media_movil(df, periodo=20):
    """
    Calcula la media móvil simple para un DataFrame de pandas.
    :param df: DataFrame con datos de mercado.
    :param periodo: Período para la media móvil (por defecto 20).
    :return: DataFrame con una columna adicional 'MA'.
    """
    df['MA'] = df['Close'].rolling(window=periodo).mean()
    return df

def calcular_bandas_bollinger(df, periodo=20, desviacion=2):
    """
    Calcula las Bandas de Bollinger para un DataFrame de pandas.
    :param df: DataFrame con datos de mercado.
    :param periodo: Período para la media móvil (por defecto 20).
    :param desviacion: Desviación estándar para las bandas (por defecto 2).
    :return: DataFrame con columnas adicionales 'Bollinger_Upper' y 'Bollinger_Lower'.
    """
    df['Bollinger_MA'] = df['Close'].rolling(window=periodo).mean()
    df['Bollinger_Upper'] = df['Bollinger_MA'] + (df['Close'].rolling(window=periodo).std() * desviacion)
    df['Bollinger_Lower'] = df['Bollinger_MA'] - (df['Close'].rolling(window=periodo).std() * desviacion)
    return df

def calcular_estocastico(df, periodo=14):
    """
    Calcula el indicador Estocástico para un DataFrame de pandas.
    :param df: DataFrame con datos de mercado.
    :param periodo: Período para el cálculo (por defecto 14).
    :return: DataFrame con columnas adicionales '%K' y '%D'.
    """
    df['%K'] = 100 * (df['Close'] - df['Low'].rolling(window=periodo).min()) / (df['High'].rolling(window=periodo).max() - df['Low'].rolling(window=periodo).min())
    df['%D'] = df['%K'].rolling(window=3).mean()
    return df

'''
# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo de datos simulados
    datos_historicos = {
        "AAPL": {
            "values": [
                {"datetime": "2025-03-10 15:30:00", "open": "226.99", "high": "228.64", "low": "226.5", "close": "227.54", "volume": "8057482"},
                {"datetime": "2025-03-10 13:30:00", "open": "225.24", "high": "227.51", "low": "224.42", "close": "226.97", "volume": "12470689"}
            ]
        }
    }
    
    # Convertir a DataFrame
    dataframes = convertir_a_dataframe(datos_historicos)
    for symbol, df in dataframes.items():
        print(f"\nDatos de {symbol}:")
        print(df)
        
        # Calcular métricas
        df = calcular_rsi(df)
        df = calcular_macd(df)
        df = calcular_media_movil(df)
        df = calcular_bandas_bollinger(df)
        df = calcular_estocastico(df)
        
        print(f"\nDatos de {symbol} con métricas calculadas:")
        print(df)
'''