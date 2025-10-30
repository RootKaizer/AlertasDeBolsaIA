# Libraries
import sys
import configparser
import json
import os
from pathlib import Path

# Core
from GetDataTwelveView import obtener_datos_historicos
from ConverterDataToPandasData import convertir_a_dataframe
from GetDataPandas import procesar_dataframes
from TradingLogicMarket import analizar_dataframes

# Styles
from styles.title_console import mostrar_titulo_estrategia



def cargar_configuracion(estrategia):
    """
    Carga los valores de rsi_under y rsi_upper desde el archivo de propiedades.
    :param estrategia: Nombre de la estrategia (corto_plazo, mediano_plazo, largo_plazo, agresivo, conservador).
    :return: Diccionario con todos los parámetros de configuración.
    """
    config = configparser.ConfigParser()
    
    # Ruta al archivo de propiedades
    ruta_archivo = "/app/scripts/properties/TradingLogicMarket.properties"
    # Ruta archivos temporales en contenedor.
    ruta_archivo_temporal = f"/app/tmp/resultados_anteriores_trading_{estrategia}.tmp"
    mobile_notification_list_file = '/app/conf/whatsappNotificationListNumber.info'  # Valor por defecto
    whatsapp_message_log_file = '/app/logs/.SenderWhatsappMessage.log'  # Valor por defecto
    
    # Leer el archivo de propiedades
    try:
        config.read(ruta_archivo)
    except Exception as e:
        raise ValueError(f"No se pudo leer el archivo de propiedades: {e}")

    if estrategia not in config:
        raise ValueError(f"Estrategia '{estrategia}' no encontrada en el archivo de propiedades.")
    
    # Cargar combinaciones estratégicas
    combinacion_indicadores = config[estrategia].get('combinacion_indicadores', 'rsi, macd, media_movil, bollinger, estocastico, volatilidad')
    combinacion_nombres = config[estrategia].get('combinacion_nombres', 'Default_Strategy')

    return {
        "rsi_under": float(config[estrategia]['rsi_under']),
        "rsi_upper": float(config[estrategia]['rsi_upper']),
        "intervalo": config[estrategia]['intervalo'],
        "periodo": config[estrategia]['periodo'],
        # Nuevos parámetros para indicadores técnicos
        "rsi_periodo": int(config[estrategia].get('rsi_periodo', '14')),
        "macd_periodo_corto": int(config[estrategia].get('macd_periodo_corto', '12')),
        "macd_periodo_largo": int(config[estrategia].get('macd_periodo_largo', '26')),
        "macd_periodo_senal": int(config[estrategia].get('macd_periodo_senal', '9')),
        "media_movil_periodo": int(config[estrategia].get('media_movil_periodo', '20')),
        "bollinger_periodo": int(config[estrategia].get('bollinger_periodo', '20')),
        "bollinger_desviacion": float(config[estrategia].get('bollinger_desviacion', '2.0')),
        "estocastico_periodo": int(config[estrategia].get('estocastico_periodo', '14')),
        # Nuevos parámetros para indicadores avanzados (valores por defecto)
        "ichimoku_conversion": int(config[estrategia].get('ichimoku_conversion', '9')),
        "ichimoku_base": int(config[estrategia].get('ichimoku_base', '26')),
        "ichimoku_span_b": int(config[estrategia].get('ichimoku_span_b', '52')),
        "ichimoku_displacement": int(config[estrategia].get('ichimoku_displacement', '26')),
        "williams_periodo": int(config[estrategia].get('williams_periodo', '14')),
        "adx_periodo": int(config[estrategia].get('adx_periodo', '14')),
        "parabolic_acceleration": float(config[estrategia].get('parabolic_acceleration', '0.02')),
        "parabolic_maximum": float(config[estrategia].get('parabolic_maximum', '0.2')),
        # Combinaciones estratégicas
        "combinacion_indicadores": [x.strip() for x in combinacion_indicadores.split(',')],
        "combinacion_nombres": [x.strip() for x in combinacion_nombres.split(',')],
        # Rutas de archivos
        "ruta_archivo_temporal": ruta_archivo_temporal,
        "mobile_notification_list_file": mobile_notification_list_file,
        "whatsapp_message_log_file": whatsapp_message_log_file
    }



def obtener_indices_mercado(estrategia, modo_debug=False):
    """
    Función principal que obtiene y analiza los índices del mercado.
    
    :param estrategia: Nombre de la estrategia a utilizar
    :param modo_debug: Si es True, muestra detalles del proceso
    :return: Diccionario con los resultados del análisis técnico
    """
    # Mostrar título de la estrategia
    mostrar_titulo_estrategia(f"Estrategia: {estrategia}")

    # Cargar configuración de la estrategia
    try:
        config = cargar_configuracion(estrategia)
        rsi_under = config["rsi_under"]
        rsi_upper = config["rsi_upper"]
        intervalo = config["intervalo"]
        periodo = config["periodo"]
        # Nuevos parámetros para indicadores técnicos
        rsi_periodo = config["rsi_periodo"]
        macd_periodo_corto = config["macd_periodo_corto"]
        macd_periodo_largo = config["macd_periodo_largo"]
        macd_periodo_senal = config["macd_periodo_senal"]
        media_movil_periodo = config["media_movil_periodo"]
        bollinger_periodo = config["bollinger_periodo"]
        bollinger_desviacion = config["bollinger_desviacion"]
        estocastico_periodo = config["estocastico_periodo"]
         # Nuevos parámetros para indicadores avanzados
        ichimoku_conversion = config["ichimoku_conversion"]
        ichimoku_base = config["ichimoku_base"]
        ichimoku_span_b = config["ichimoku_span_b"]
        ichimoku_displacement = config["ichimoku_displacement"]
        williams_periodo = config["williams_periodo"]
        adx_periodo = config["adx_periodo"]
        parabolic_acceleration = config["parabolic_acceleration"]
        parabolic_maximum = config["parabolic_maximum"]
        # Combinaciones estratégicas
        combinacion_indicadores = config["combinacion_indicadores"]
        combinacion_nombres = config["combinacion_nombres"]
        
    except Exception as e:
        print(f"Error al cargar la configuración: {e}")
        return None
    


    # Paso 1: Obtener datos históricos
    print("Obteniendo datos históricos...")
    datos_historicos = obtener_datos_historicos(intervalo, periodo)
    print(f"Datos históricos obtenidos para {len(datos_historicos)} mercados.")
    
    if not datos_historicos:
        print("No se pudieron obtener los datos históricos.")
        return None
    


    # Paso 2: Convertir datos a DataFrames de pandas
    print("Convirtiendo datos a DataFrames...")
    dataframes = convertir_a_dataframe(datos_historicos, modo_debug)
    print(f"Se convirtieron {len(dataframes)} DataFrames.")



    # Paso 3: Procesar DataFrames y calcular métricas
    print("\nCalculando indicadores técnicos...")

    if modo_debug:
        print("🔍 MODO DEBUG ACTIVADO PARA INDICADORES TÉCNICOS")
        print(f"📊 Parámetros utilizados:")
        print(f"  - RSI período: {rsi_periodo}")
        print(f"  - MACD corto/largo/señal: {macd_periodo_corto}/{macd_periodo_largo}/{macd_periodo_senal}")
        print(f"  - Media móvil período: {media_movil_periodo}")
        print(f"  - Bollinger período/desviación: {bollinger_periodo}/{bollinger_desviacion}")
        print(f"  - Estocástico período: {estocastico_periodo}")
        print(f"  - Ichimoku: {ichimoku_conversion}/{ichimoku_base}/{ichimoku_span_b}")
        print(f"  - Williams %R período: {williams_periodo}")
        print(f"  - ADX período: {adx_periodo}")
        print(f"  - Parabolic SAR: acc={parabolic_acceleration}, max={parabolic_maximum}")
        print(f"  - Combinación: {combinacion_indicadores}")
    
    # funcion que calcula los valores de los indicadores.
    indicadores_de_bolsa_caldulados = procesar_dataframes(
        dataframes, 
        rsi_periodo=rsi_periodo,
        macd_periodo_corto=macd_periodo_corto,
        macd_periodo_largo=macd_periodo_largo,
        macd_periodo_senal=macd_periodo_senal,
        media_movil_periodo=media_movil_periodo,
        bollinger_periodo=bollinger_periodo,
        bollinger_desviacion=bollinger_desviacion,
        estocastico_periodo=estocastico_periodo,
        ichimoku_conversion=ichimoku_conversion,
        ichimoku_base=ichimoku_base,
        ichimoku_span_b=ichimoku_span_b,
        ichimoku_displacement=ichimoku_displacement,
        williams_periodo=williams_periodo,
        adx_periodo=adx_periodo,
        parabolic_acceleration=parabolic_acceleration,
        parabolic_maximum=parabolic_maximum,
        verbose=modo_debug
    )



    # Paso 4: Aplicar lógica de trading
    parametros_analisis = {
    'rsi_under': rsi_under,
    'rsi_upper': rsi_upper,
    'rsi_periodo': rsi_periodo,
    'macd_periodo_corto': macd_periodo_corto,
    'macd_periodo_largo': macd_periodo_largo,
    'macd_periodo_senal': macd_periodo_senal,
    'media_movil_periodo': media_movil_periodo,
    'bollinger_periodo': bollinger_periodo,
    'bollinger_desviacion': bollinger_desviacion,
    'estocastico_periodo': estocastico_periodo,
    'combinacion_indicadores': combinacion_indicadores,
    'combinacion_nombres': combinacion_nombres,
    'periodo_volatilidad': 20
    }

    resultados_trading = analizar_dataframes(
        indicadores_de_bolsa_caldulados, 
        verbose=modo_debug,
        **parametros_analisis
    )

    print(f"\n✅ ANÁLISIS COMPLETADO para estrategia: {estrategia}")
    print(f"   Símbolos procesados: {len(resultados_trading)}")
    print(f"   Combinación utilizada: {', '.join(combinacion_nombres)}")

    return resultados_trading



# Función de compatibilidad para mantener el funcionamiento actual
def main(estrategia, modo_debug=False):
    """
    Función principal para compatibilidad con llamadas externas.
    
    :param estrategia: Nombre de la estrategia
    :param modo_debug: Si es True, activa modo debug
    :return: Resultados del análisis técnico
    """
    return obtener_indices_mercado(estrategia, modo_debug)



"""
if __name__ == "__main__":
    # Este bloque solo se ejecuta si el script se ejecuta directamente
    # (útil para pruebas, pero normalmente será llamado por Start.py)
    
    # Verificar argumentos de línea de comandos
    if len(sys.argv) < 2:
        print("🚀 USO: python 00_ObtenerIndicesDelMercado.py <estrategia> [debug]")
        print("")
        print("📋 ESTRATEGIAS DISPONIBLES:")
        print("   - corto_plazo     (Trading intradía)")
        print("   - mediano_plazo   (Swing trading)") 
        print("   - largo_plazo     (Inversión a largo plazo)")
        print("   - agresivo        (Scalping alto riesgo)")
        print("   - conservador     (Inversión conservadora)")
        sys.exit(1)
    
    # Primer parámetro: estrategia
    estrategia = sys.argv[1].lower()
    
    # Segundo parámetro: modo debug (opcional)
    modo_debug = False
    if len(sys.argv) > 2:
        debug_arg = sys.argv[2].lower()
        if debug_arg in ['true', '1', 'yes', 'y', 'verdadero']:
            modo_debug = True
    
    # Ejecutar análisis
    resultados = obtener_indices_mercado(estrategia, modo_debug)
    
    if resultados:
        print(f"\n🎯 Análisis completado exitosamente. Símbolos procesados: {len(resultados)}")
    else:
        print("\n❌ Error en el análisis de índices del mercado")
        sys.exit(1)
[file content end]
"""

