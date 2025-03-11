import pandas as pd

def convertir_a_dataframe(datos_historicos):
    """
    Convierte los datos históricos en un diccionario de DataFrames de pandas.
    :param datos_historicos: Diccionario con los datos obtenidos de GetDataTwelveView.py
    :return: Diccionario con DataFrames por símbolo.
    """
    dataframes = {}
    
    for symbol, data in datos_historicos.items():
        if 'values' in data:
            df = pd.DataFrame(data['values'])
            df['datetime'] = pd.to_datetime(df['datetime'])  # Convertir a formato de fecha y hora
            # Asegúrate de que los nombres de las columnas sean correctos
            df = df.rename(columns={
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'close': 'Close',  # Asegúrate de que sea 'Close'
                'volume': 'Volume'
            })
            df[['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']].astype(float)  # Convertir valores numéricos
            df = df.sort_values(by='datetime')  # Ordenar por fecha y hora
            dataframes[symbol] = df
        else:
            print(f"Advertencia: No se encontraron valores para {symbol}")
    
    return dataframes


def convertir_a_backtrader(df):
    """
    Convierte un DataFrame de pandas en un formato compatible con Backtrader.
    :param df: DataFrame con datos de mercado.
    :return: DataFrame formateado para Backtrader.
    """
    df = df.copy()
    df.set_index('datetime', inplace=True)  # Establecer datetime como índice
    df.rename(columns={
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'volume': 'Volume'
    }, inplace=True)  # Renombrar columnas para Backtrader
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
    
    dataframes = convertir_a_dataframe(datos_historicos)
    for symbol, df in dataframes.items():
        print(f"\nDatos de {symbol}:")
        print(df)
        
        bt_df = convertir_a_backtrader(df)
        print(f"\nDatos de {symbol} para Backtrader:")
        print(bt_df)
'''