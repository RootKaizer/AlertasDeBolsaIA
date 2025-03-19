# Libraries
import sys
import configparser

# Core
from GetDataTwelveView import obtener_datos_historicos
from ConverterDataToPandasData import convertir_a_dataframe
from GetDataPandas import procesar_dataframes
from TradingLogicMarket import determinar_accion_rsi, determinar_accion_macd, determinar_accion_precio, determinar_accion_estocastico

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
    print("Procesando datos y calculando métricas...")
    dataframes_procesados = procesar_dataframes(dataframes)

    # Paso 4: Aplicar lógica de trading y mostrar resultados
    print("\nAplicando lógica de trading...")
    resultados_trading = {}  # Diccionario para almacenar las acciones recomendadas por símbolo

    for symbol, df in dataframes_procesados.items():
        print(f"\nAnalizando {symbol}...")

        # Obtener los últimos valores para aplicar la lógica de trading
        rsi = df['RSI'].iloc[-1]
        macd = df['MACD'].iloc[-1]
        macd_signal = df['MACD_signal'].iloc[-1]
        precio_actual = df['Close'].iloc[-1]
        precio_anterior = df['Close'].iloc[-2]
        estocastico_k = df['%K'].iloc[-1]
        estocastico_d = df['%D'].iloc[-1]

        # Determinar las acciones individuales
        accion_rsi, descripcion_rsi = determinar_accion_rsi(rsi, rsi_under, rsi_upper)
        accion_macd, descripcion_macd = determinar_accion_macd(macd, macd_signal)
        accion_precio, descripcion_precio = determinar_accion_precio(precio_actual, precio_anterior)
        accion_estocastico, descripcion_estocastico = determinar_accion_estocastico(estocastico_k, estocastico_d)

            # Guardar los resultados (acciones y descripciones)
        resultados_trading[symbol] = {
            "RSI": {"accion": accion_rsi, "descripcion": descripcion_rsi},
            "MACD": {"accion": accion_macd, "descripcion": descripcion_macd},
            "Precio": {"accion": accion_precio, "descripcion": descripcion_precio},
            "Estocástico": {"accion": accion_estocastico, "descripcion": descripcion_estocastico}
        }

    # Paso 5: Mostrar resultados
    mostrar_resultados_trading(estrategia, resultados_trading)



if __name__ == "__main__":
    main()