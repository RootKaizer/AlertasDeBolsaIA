
import sys
from GetDataTwelveView import obtener_datos_historicos
from ConverterDataToPandasData import convertir_a_dataframe
from ProcesingDataPandas import calcular_rsi, calcular_macd, calcular_media_movil, calcular_bandas_bollinger, calcular_estocastico

def main():
    # Paso 1: Obtener datos históricos
    print("Obteniendo datos históricos...")
    # Ajustamos el intervalo de tiempo para obtener más datos (por ejemplo, 1 año de datos con intervalos de 1 día)
    datos_historicos = obtener_datos_historicos("1day", "1year")
    print(f"Datos históricos obtenidos para {len(datos_historicos)} símbolos.")
    
    if not datos_historicos:
        print("No se pudieron obtener los datos históricos.")
        return

    # Paso 2: Convertir datos a DataFrames de pandas
    print("Convirtiendo datos a DataFrames...")
    dataframes = convertir_a_dataframe(datos_historicos)
    print(f"Se convirtieron {len(dataframes)} DataFrames.")

    # Paso 3: Procesar DataFrames y calcular métricas
    print("Procesando datos y calculando métricas...")
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
        dataframes[symbol] = df

    # Paso 4: Mostrar resultados
    print("\nResultados finales:")
    for symbol, df in dataframes.items():
        print(f"\nDatos procesados para {symbol}:")
        print(df.tail())  # Mostrar las últimas filas del DataFrame para verificar los cálculos

if __name__ == "__main__":
    main()