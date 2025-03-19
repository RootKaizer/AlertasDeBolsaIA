# Libraries
import sys
import configparser

# Core
from GetDataTwelveView import obtener_datos_historicos
from ConverterDataToPandasData import convertir_a_dataframe
from GetDataPandas import procesar_dataframes
from TradingLogicMarket import analizar_dataframes

# Styles
from styles.title_console import mostrar_titulo_estrategia
from styles.exit_console import mostrar_resultados_trading


def cargar_configuracion(estrategia):
    """
    Carga los valores de rsi_under y rsi_upper desde el archivo de propiedades.
    :param estrategia: Nombre de la estrategia (corto_plazo, mediano_plazo, largo_plazo, agresivo, conservador).
    :return: Diccionario con rsi_under y rsi_upper.
    """
    config = configparser.ConfigParser()
    
    # Ruta al archivo de propiedades
    ruta_archivo = "properties/TradingLogicMarket.properties"
    
    # Leer el archivo de propiedades
    try:
        config.read(ruta_archivo)
    except Exception as e:
        raise ValueError(f"No se pudo leer el archivo de propiedades: {e}")

    if estrategia not in config:
        raise ValueError(f"Estrategia '{estrategia}' no encontrada en el archivo de propiedades.")

    return {
        "rsi_under": float(config[estrategia]['rsi_under']),
        "rsi_upper": float(config[estrategia]['rsi_upper'])
    }



def main():
    # Paso 0: Seleccionar estrategia
    estrategia = "corto_plazo"  # Puedes cambiar esto a "mediano_plazo", "largo_plazo", "agresivo", "conservador"
    
    # Mostrar título de la estrategia
    mostrar_titulo_estrategia(f"Estrategia: {estrategia}")

    # Cargar configuración de la estrategia
    try:
        config_rsi = cargar_configuracion(estrategia)
        rsi_under = config_rsi["rsi_under"]
        rsi_upper = config_rsi["rsi_upper"]
    except Exception as e:
        print(f"Error al cargar la configuración: {e}")
        return

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
    print("\ncalculando Datos .....")
    print("RSI.")
    print("MACD.")
    print("MACD_signal.")
    print("Precio Actual.")
    print("Precio Anterior.")
    print("Estocastico K.")
    print("Estocastico D.")
    dataframes_procesados = procesar_dataframes(dataframes)

    # Paso 4: Aplicar lógica de trading
    print("\nAplicando lógica de trading...")
    resultados_trading = analizar_dataframes(dataframes_procesados, rsi_under, rsi_upper)

    # Paso 5: Mostrar resultados
    mostrar_resultados_trading(estrategia, resultados_trading)



if __name__ == "__main__":
    main()