
import sys
from GetDataTwelveView import obtener_datos_historicos
#from ConverterDataToPandasData import convertir_a_dataframe
#from ProcesingDataPandas import procesar_dataframes


def main():
    # Paso 1: Obtener datos históricos
    print("Obteniendo datos históricos...")
    datos_historicos = obtener_datos_historicos("2h", "1day")
    print(f"{datos_historicos}")
    if not datos_historicos:
        print("No se pudieron obtener los datos históricos.")
        return

    # Paso 2: Convertir datos a DataFrames de pandas
    #print("Convirtiendo datos a DataFrames...")
    #dataframes = ConverterDataToPandasData.convertir_a_dataframe(datos_historicos)

    # Paso 3: Procesar DataFrames y aplicar lógica de trading
    #print("Procesando datos y aplicando lógica de trading...")
    #resultados = ProcesingDataPandas.procesar_dataframes(dataframes)

    # Paso 4: Mostrar resultados
    #print("\nResultados finales:")
    #for symbol, acciones in resultados.items():
    #    print(f"{symbol}: {acciones}")

if __name__ == "__main__":
    main()