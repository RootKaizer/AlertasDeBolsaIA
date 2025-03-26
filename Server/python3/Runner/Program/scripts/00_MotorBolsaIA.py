# Libraries
import sys
import configparser
import json
import os
from pathlib import Path
from DebugMotorBolsaIA import DebugMotorBolsaIA

# Core
from GetDataTwelveView import obtener_datos_historicos
from ConverterDataToPandasData import convertir_a_dataframe
from GetDataPandas import procesar_dataframes
from TradingLogicMarket import analizar_dataframes
from NotificationLogicSender import comparar_y_notificar

# Styles
from styles.title_console import mostrar_titulo_estrategia
from styles.exit_console import mostrar_resultados_trading



def cargar_configuracion(estrategia):
    """
    Carga los valores de rsi_under y rsi_upper desde el archivo de propiedades.
    :param estrategia: Nombre de la estrategia (corto_plazo, mediano_plazo, largo_plazo, agresivo, conservador).
    :return: Diccionario con rsi_under, rsi_upper, intervalo y periodo.
    """
    config = configparser.ConfigParser()
    
    # Ruta al archivo de propiedades
    ruta_archivo = "properties/TradingLogicMarket.properties"
    # Ruta archivos temporales en contenedor.
    ruta_archivo_temporal = f"/app/tmp/resultados_anteriores_trading_{estrategia}.tmp"
    
    # Leer el archivo de propiedades
    try:
        config.read(ruta_archivo)
    except Exception as e:
        raise ValueError(f"No se pudo leer el archivo de propiedades: {e}")

    if estrategia not in config:
        raise ValueError(f"Estrategia '{estrategia}' no encontrada en el archivo de propiedades.")

    return {
        "rsi_under": float(config[estrategia]['rsi_under']),
        "rsi_upper": float(config[estrategia]['rsi_upper']),
        "intervalo": config[estrategia]['intervalo'],
        "periodo": config[estrategia]['periodo'],
        "ruta_archivo_temporal": ruta_archivo_temporal
    }



def cargar_resultados_anteriores(resultados, ruta_archivo):
    """
    Carga los resultados anteriores desde archivo temporal si existe.
    
    Args:
        estrategia: Nombre de la estrategia para el nombre del archivo
        
    Returns:
        Diccionario con resultados anteriores o None si no existe el archivo
    """
    try:
        ruta_archivo = Path(ruta_archivo)
    
        if not ruta_archivo.exists():
            return resultados
    
        with open(ruta_archivo, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error al cargar resultados anteriores: {e}")
        return None



def guardar_resultados_temporales(resultados, ruta_archivo):
    """
    Guarda los resultados en un archivo temporal para la próxima ejecución.
    
    Args:
        resultados: Diccionario con resultados a guardar
        estrategia: Nombre de la estrategia para el nombre del archivo
    """
    try:
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
        
        ruta_archivo = Path(ruta_archivo)
        
        with open(ruta_archivo, 'w') as file:
            json.dump(resultados, file)
    except Exception as e:
        print(f"Error al guardar resultados temporales: {e}")



def main():
    # Inicializar el modo debug
    debug = DebugMotorBolsaIA()

    # Paso 0: Seleccionar estrategia
    estrategia = "mediano_plazo"  # Puedes cambiar esto a "mediano_plazo", "largo_plazo", "agresivo", "conservador"

     
    # Mostrar título de la estrategia
    mostrar_titulo_estrategia(f"Estrategia: {estrategia}")

    # Cargar configuración de la estrategia
    try:
        config = cargar_configuracion(estrategia)
        rsi_under = config["rsi_under"]
        rsi_upper = config["rsi_upper"]
        intervalo = config["intervalo"]
        periodo = config["periodo"]
        ruta_archivo_temporal = config["ruta_archivo_temporal"]
        
        debug.escribir_configuracion({
            "estrategia": estrategia, 
            "intervalo": intervalo, 
            "periodo": periodo, 
            "rsi_under": rsi_under, 
            "rsi_upper": rsi_upper,
            "ruta_archivo_temporal": ruta_archivo_temporal
        })
    except Exception as e:
        print(f"Error al cargar la configuración: {e}")
        return

    # Paso 1: Obtener datos históricos
    debug.escribir_paso(1, "obtener_datos_historicos", {
        "intervalo": intervalo, 
        "periodo": periodo
        })
    print("Obteniendo datos históricos...")
    # Ajustamos el intervalo de tiempo para obtener más datos (por ejemplo, 1 año de datos con intervalos de 1 día)
    datos_historicos = obtener_datos_historicos(intervalo, periodo)
    debug.escribir_paso(1, "obtener_datos_historicos", {}, respuesta=f"Datos obtenidos para {len(datos_historicos)} mercados.")
    print(f"Datos históricos obtenidos para {len(datos_historicos)} mercados.")
    
    if not datos_historicos:
        print("No se pudieron obtener los datos históricos.")
        return

    # Paso 2: Convertir datos a DataFrames de pandas
    debug.escribir_paso(2, "convertir_a_dataframe", {
        "datos_historicos": datos_historicos
        })
    print("Convirtiendo datos a DataFrames...")
    dataframes = convertir_a_dataframe(datos_historicos)
    debug.escribir_paso(2, "convertir_a_dataframe", {}, respuesta=f"Se convirtieron {len(dataframes)} DataFrames.")
    print(f"Se convirtieron {len(dataframes)} DataFrames.")

    # Paso 3: Procesar DataFrames y calcular métricas
    debug.escribir_paso(3, "procesar_dataframes", {
        "dataframes": dataframes
        })
    print("\ncalculando Datos .....")
    print("RSI.")
    print("MACD.")
    print("MACD_signal.")
    print("Precio Actual.")
    print("Precio Anterior.")
    print("Estocastico K.")
    print("Estocastico D.")
    dataframes_procesados = procesar_dataframes(dataframes)
    debug.escribir_paso(3, "procesar_dataframes", {}, respuesta="DataFrames procesados correctamente.")

    # Paso 4: Aplicar lógica de trading
    debug.escribir_paso(4, "analizar_dataframes", {
        "dataframes_procesados": dataframes_procesados, 
        "rsi_under": rsi_under, 
        "rsi_upper": rsi_upper
        })
    print("\nAplicando lógica de trading...")
    resultados_trading = analizar_dataframes(dataframes_procesados, rsi_under, rsi_upper)
    debug.escribir_paso(4, "analizar_dataframes", {}, respuesta="Lógica de trading aplicada correctamente.")

    # Paso 5: Mostrar resultados
    debug.escribir_paso(5, "mostrar_resultados_trading", {
        "estrategia": estrategia,
        "resultados_trading": resultados_trading
        })
    print("\nMostrar resultados...")
    mostrar_resultados_trading(estrategia, resultados_trading)

    # Paso 6: Comparar con resultados anteriores y notificar
        # Variable para almacenar resultados anteriores
    resultados_anteriores = cargar_resultados_anteriores(resultados_trading, ruta_archivo_temporal)
    print("\nComparando con resultados anteriores...")
    try:
        resultado_notificacion = comparar_y_notificar(resultados_anteriores, resultados_trading, estrategia)
        
        if isinstance(resultado_notificacion, tuple):
            numeros, mensaje = resultado_notificacion
            debug.escribir_paso(6, "comparar_y_notificar", {
                                                    "estrategia": estrategia, 
                                                    "resultados_anteriores": resultados_anteriores,
                                                    "\nresultados_trading": resultados_trading
                                                    }, 
                               respuesta=f"Notificación para {len(numeros)} números")
            print(f"\nPreparado para enviar a {len(numeros)} números:")
            print(mensaje)
        else:
            debug.escribir_paso(6, "comparar_y_notificar", {
                                                    "estrategia": estrategia, 
                                                    "resultados_anteriores": resultados_anteriores,
                                                    ".. ": "..",
                                                    "resultados_trading": resultados_trading,
                                                    "-- ": "--"
                                                    }, 
                              respuesta=resultado_notificacion)
            print(f"\n{resultado_notificacion}")
            
    except Exception as e:
        error_msg = f"Error en comparación: {str(e)}"
        print(f"\n{error_msg}")
        debug.escribir_paso(6, "comparar_y_notificar", {}, 
                          respuesta=error_msg)
    
    # Guardar resultados actuales para la próxima ejecución
    guardar_resultados_temporales(resultados_trading, ruta_archivo_temporal)



if __name__ == "__main__":
    main()