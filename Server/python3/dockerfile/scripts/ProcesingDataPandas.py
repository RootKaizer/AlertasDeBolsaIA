import pandas as pd
import numpy as np

def calcular_indicadores(df):
    # Calcular SMA
    df['sma'] = df['close'].rolling(window=20).mean()

    # Calcular RSI
    delta = df['close'].diff()
    ganancia = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    perdida = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = ganancia / perdida
    df['rsi'] = 100 - (100 / (1 + rs))

    # Calcular MACD
    ema_rapida = df['close'].ewm(span=12, adjust=False).mean()
    ema_lenta = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = ema_rapida - ema_lenta
    df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['macd_hist'] = df['macd'] - df['macd_signal']

    return df

def determinar_accion(rsi, macd, sma, precio_actual):
    acciones = []

    # Lógica para RSI
    if rsi > 70:
        acciones.append("vender")
    elif rsi < 30:
        acciones.append("comprar")
    else:
        acciones.append("hold")

    # Lógica para MACD
    if macd > 0:
        acciones.append("comprar")
    else:
        acciones.append("vender")

    # Lógica para SMA
    if precio_actual > sma:
        acciones.append("comprar")
    else:
        acciones.append("vender")

    return acciones

def procesar_dataframes(dataframes):
    resultados = {}
    for symbol, df in dataframes.items():
        df = calcular_indicadores(df)
        ultimo_indice = df.index[-1]
        rsi = df['rsi'].iloc[-1]
        macd = df['macd'].iloc[-1]
        sma = df['sma'].iloc[-1]
        precio_actual = df['close'].iloc[-1]

        acciones = determinar_accion(rsi, macd, sma, precio_actual)
        resultados[symbol] = acciones
    return resultados

if __name__ == "__main__":
    # Esto es solo para pruebas, no se usará en el script maestro
    dataframes = {
        "AAPL": pd.DataFrame([{"close": 235.32}, {"close": 234.50}, ...]),
        "TSLA": pd.DataFrame([{"close": 261.17}, {"close": 260.45}, ...])
    }
    resultados = procesar_dataframes(dataframes)
    print(resultados)
    