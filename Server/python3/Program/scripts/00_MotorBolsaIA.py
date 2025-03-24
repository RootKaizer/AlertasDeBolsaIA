# Libraries
import sys
import configparser
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

# Helpers
#from helpers.notificationSender import whatsapp


def cargar_configuracion(estrategia):
    """
    Carga los valores de rsi_under y rsi_upper desde el archivo de propiedades.
    :param estrategia: Nombre de la estrategia (corto_plazo, mediano_plazo, largo_plazo, agresivo, conservador).
    :return: Diccionario con rsi_under, rsi_upper, intervalo y periodo.
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
        "rsi_upper": float(config[estrategia]['rsi_upper']),
        "intervalo": config[estrategia]['intervalo'],
        "periodo": config[estrategia]['periodo']
    }



def main():
    # Inicializar el modo debug
    debug = DebugMotorBolsaIA()

    # Variable para almacenar resultados anteriores
    resultados_anteriores = None

    # Paso 0: Seleccionar estrategia
    estrategia = "mediano_plazo"  # Puedes cambiar esto a "mediano_plazo", "largo_plazo", "agresivo", "conservador"
    
    # Mostrar título de la estrategia
    mostrar_titulo_estrategia(f"Estrategia: {estrategia}")

    # Cargar configuración de la estrategia
    try:
        config_rsi = cargar_configuracion(estrategia)
        rsi_under = config_rsi["rsi_under"]
        rsi_upper = config_rsi["rsi_upper"]
        intervalo = config_rsi["intervalo"]
        periodo = config_rsi["periodo"]
        debug.escribir_configuracion({"estrategia": estrategia, "intervalo": intervalo, "periodo": periodo, "rsi_under": rsi_under, "rsi_upper": rsi_upper})
    except Exception as e:
        print(f"Error al cargar la configuración: {e}")
        return

    # Paso 1: Obtener datos históricos
    debug.escribir_paso(1, "obtener_datos_historicos", {"intervalo": intervalo, "periodo": periodo})
    print("Obteniendo datos históricos...")
    # Ajustamos el intervalo de tiempo para obtener más datos (por ejemplo, 1 año de datos con intervalos de 1 día)
    datos_historicos = obtener_datos_historicos(intervalo, periodo)
    debug.escribir_paso(1, "obtener_datos_historicos", {}, respuesta=f"Datos obtenidos para {len(datos_historicos)} mercados.")
    print(f"Datos históricos obtenidos para {len(datos_historicos)} mercados.")
    
    if not datos_historicos:
        print("No se pudieron obtener los datos históricos.")
        return

    # Paso 2: Convertir datos a DataFrames de pandas
    debug.escribir_paso(2, "convertir_a_dataframe", {"datos_historicos": datos_historicos})
    print("Convirtiendo datos a DataFrames...")
    dataframes = convertir_a_dataframe(datos_historicos)
    debug.escribir_paso(2, "convertir_a_dataframe", {}, respuesta=f"Se convirtieron {len(dataframes)} DataFrames.")
    print(f"Se convirtieron {len(dataframes)} DataFrames.")

    # Paso 3: Procesar DataFrames y calcular métricas
    debug.escribir_paso(3, "procesar_dataframes", {"dataframes": dataframes})
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
    debug.escribir_paso(4, "analizar_dataframes", {"dataframes_procesados": dataframes_procesados, "rsi_under": rsi_under, "rsi_upper": rsi_upper})
    print("\nAplicando lógica de trading...")
    resultados_trading = analizar_dataframes(dataframes_procesados, rsi_under, rsi_upper)
    debug.escribir_paso(4, "analizar_dataframes", {}, respuesta="Lógica de trading aplicada correctamente.")

    # Paso 5: Mostrar resultados
    debug.escribir_paso(5, "mostrar_resultados_trading", {"estrategia": estrategia, "resultados_trading": resultados_trading})
    print("\nMostrar resultados...")
    mostrar_resultados_trading(estrategia, resultados_trading)

    # Paso 6: Comparar con resultados anteriores y notificar si hay cambios
    debug.escribir_paso(6, "comparar_y_notificar", {"estrategia": estrategia, "resultados_anteriores": resultados_anteriores, "resultados_trading": resultados_trading})
    print("\nComparar con resultados anteriores y notificar si hay cambios...")
    whatsapp_message = comparar_y_notificar(resultados_anteriores, resultados_trading, estrategia)
    debug.escribir_paso(6, "comparar_y_notificar", {}, respuesta=f"El mensaje de WhatsApp es: {whatsapp_message}")
    
    # Guardar resultados actuales para la próxima comparación
    resultados_anteriores = resultados_trading



if __name__ == "__main__":
    main()