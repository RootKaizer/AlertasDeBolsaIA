import pandas as pd
from datetime import datetime

def convertir_a_dataframe(datos_historicos, verbose=False):
    """
    Convierte los datos históricos en un diccionario de DataFrames de pandas.
    :param datos_historicos: Diccionario con los datos obtenidos de GetDataTwelveView.py
    :param verbose: Si es True, muestra detalles de los cálculos y conversiones
    :return: Diccionario con DataFrames por símbolo.
    """
    if not datos_historicos:
        if verbose:
            print("❌ No hay datos históricos para convertir")
        return {}
    
    dataframes = {}
    
    for symbol, data in datos_historicos.items():
        if verbose:
            print(f"\n{'='*50}")
            print(f"PROCESANDO SÍMBOLO: {symbol}")
            print(f"{'='*50}")
        
        if 'values' not in data or not data['values']:
            if verbose:
                print(f"❌ No hay datos válidos para {symbol}")
            continue
        
        if 'values' in data:
            # Crear DataFrame
            df = pd.DataFrame(data['values'])

            # Mostrar datos de entrada si verbose está activado
            if verbose:
                print(f"DATOS DE ENTRADA PARA {symbol}:")
                print(f"Número de registros: {len(df)}")
                if len(df) > 0:
                    primer_registro = df.iloc[0]
                    print("Primer registro:")
                    print(f"  datetime: {primer_registro['datetime']}")
                    print(f"  open: {primer_registro['open']:.5f}")
                    print(f"  high: {primer_registro['high']:.5f}")
                    print(f"  low: {primer_registro['low']:.5f}")
                    print(f"  close: {primer_registro['close']:.5f}")
                    print(f"  volume: {primer_registro['volume']}")
                
            # Conversión de datetime
            if verbose:
                print(f"\nCÁLCULO: Conversión de datetime")
                print(f"  Función: pd.to_datetime(df['datetime'], errors='coerce')")
                print(f"  Valores de entrada: {len(df)} registros de fecha/hora")
                if len(df) > 0:
                    print(f"  Ejemplo: {df['datetime'].iloc[0]}")

            df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')  # Convertir a formato de fecha y hora

            # Verificar si hay fechas que no se pudieron parsear
            fechas_invalidas = df['datetime'].isna().sum()
            if fechas_invalidas > 0:
                if verbose:
                    print(f"⚠️  Advertencia: {fechas_invalidas} fechas no pudieron ser parseadas automáticamente")
                    print("🔄 Intentando parsing manual para fechas problemáticas...")
                
                # Método de respaldo: parsing manual para fechas problemáticas
                for idx in df[df['datetime'].isna()].index:
                    fecha_original = df.loc[idx, 'datetime']
                    try:
                        # Limpiar formato de fecha (ej: "2025-10-16 04:00:00:00" -> "2025-10-16 04:00:00")
                        fecha_limpia = str(fecha_original).rstrip(':00')
                        if len(fecha_limpia) == 19:  # Formato YYYY-MM-DD HH:MM:SS
                            df.loc[idx, 'datetime'] = pd.to_datetime(fecha_limpia, errors='coerce')
                        elif len(fecha_limpia) == 16:  # Formato YYYY-MM-DD HH:MM
                            df.loc[idx, 'datetime'] = pd.to_datetime(fecha_limpia + ':00', errors='coerce')
                        elif len(fecha_limpia) == 10:  # Formato YYYY-MM-DD
                            df.loc[idx, 'datetime'] = pd.to_datetime(fecha_limpia + ' 00:00:00', errors='coerce')
                    except:
                        continue
                
                # Contar fechas aún inválidas después del parsing manual
                fechas_invalidas_final = df['datetime'].isna().sum()
                if fechas_invalidas_final > 0:
                    if verbose:
                        print(f"❌ {fechas_invalidas_final} fechas aún no pudieron ser parseadas")
                    # Eliminar filas con fechas inválidas
                    df = df.dropna(subset=['datetime'])
                    if verbose:
                        print(f"✅ Filas restantes después de limpieza: {len(df)}")

            # Renombrar columnas
            if verbose:
                print(f"\nCÁLCULO: Renombrado de columnas")
                print(f"  Función: df.rename(columns=mapping_dict)")
                column_mapping = {
                    'open': 'Open',
                    'high': 'High', 
                    'low': 'Low',
                    'close': 'Close',
                    'volume': 'Volume'
                }
                print(f"  Mapeo aplicado: {column_mapping}")
                print(f"  Columnas antes: {list(df.columns)}")
            
            df = df.rename(columns={
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'close': 'Close',
                'volume': 'Volume'
            })

            if verbose:
                print(f"  Columnas después: {list(df.columns)}")
            
            # Conversión de tipos de datos numéricos
            if verbose:
                print(f"\nCÁLCULO: Conversión de tipos numéricos")
                print(f"  Función: df[columns].astype(float)")
                numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                print(f"  Columnas convertidas: {numeric_columns}")
                if len(df) > 0:
                    for col in numeric_columns:
                        if col in df.columns:
                            print(f"  {col}: '{df[col].iloc[0]}' -> {float(df[col].iloc[0])}")

            df[['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']].astype(float)  # Convertir valores numéricos

            # Ordenar por fecha
            if verbose:
                print(f"\nCÁLCULO: Ordenamiento por fecha")
                print(f"  Función: df.sort_values(by='datetime')")
                print(f"  Registros antes: {len(df)}")
                if len(df) > 1:
                    print(f"  Rango temporal: {df['datetime'].min()} a {df['datetime'].max()}")
            
            df = df.sort_values(by='datetime')

            if verbose:
                print(f"  Registros después: {len(df)}")
                if len(df) > 1:
                    print(f"  Rango temporal ordenado: {df['datetime'].min()} a {df['datetime'].max()}")
            
            # Resumen final
            if verbose:
                print(f"\nRESUMEN PARA {symbol}:")
                print(f"  DataFrame shape: {df.shape}")
                print(f"  Columnas: {list(df.columns)}")
                print(f"  Tipos de datos:")
                for col in df.columns:
                    print(f"    {col}: {df[col].dtype}")
                print(f"  Rango de fechas: {df['datetime'].min()} a {df['datetime'].max()}")
                if len(df) > 0:
                    print(f"  Último precio Close: {df['Close'].iloc[-1]}")

            dataframes[symbol] = df
        else:
            if verbose:
                print(f"ADVERTENCIA: No se encontraron valores para {symbol}")
            else:
                print(f"Advertencia: No se encontraron valores para {symbol}")
    
    if verbose:
        print(f"\n{'='*50}")
        print(f"RESUMEN GENERAL")
        print(f"{'='*50}")
        print(f"Total de símbolos procesados: {len(dataframes)}")
        print(f"Símbolos: {list(dataframes.keys())}")
        for symbol, df in dataframes.items():
            print(f"  {symbol}: {len(df)} registros, shape {df.shape}")
    
    return dataframes


def convertir_a_backtrader(df, verbose=False):
    """
    Convierte un DataFrame de pandas en un formato compatible con Backtrader.
    :param df: DataFrame con datos de mercado.
    :param verbose: Si es True, muestra detalles de los cálculos realizados
    :return: DataFrame formateado para Backtrader.
    """
    if verbose:
            print(f"\n{'='*50}")
            print(f"CONVERSIÓN A BACKTRADER")
            print(f"{'='*50}")
            print(f"DataFrame original shape: {df.shape}")
            print(f"Columnas originales: {list(df.columns)}")
    
    df = df.copy()

    # Establecer datetime como índice
    if verbose:
        print(f"\nCÁLCULO: Establecer datetime como índice")
        print(f"  Función: df.set_index('datetime', inplace=True)")
        print(f"  Tipo de índice antes: {type(df.index)}")
    
    df.set_index('datetime', inplace=True)  # Establecer datetime como índice

    if verbose:
        print(f"  Tipo de índice después: {type(df.index)}")
        print(f"  Primer valor del índice: {df.index[0] if len(df) > 0 else 'N/A'}")

    
    df.rename(columns={
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'volume': 'Volume'
    }, inplace=True)  # Renombrar columnas para Backtrader

    if verbose:
        print(f"\nCÁLCULO: Verificación de nombres de columnas")
        print(f"  Columnas actuales: {list(df.columns)}")
        print(f"  No se requiere renombrado adicional")
    
    if verbose:
        print(f"\nRESUMEN CONVERSIÓN BACKTRADER:")
        print(f"  DataFrame final shape: {df.shape}")
        print(f"  Columnas: {list(df.columns)}")
        print(f"  Índice: {type(df.index)}")
        if len(df) > 0:
            print(f"  Rango temporal: {df.index.min()} a {df.index.max()}")
    
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