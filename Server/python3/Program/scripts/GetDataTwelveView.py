import sys
from helpers.config_loader import cargar_configuracion_apis
from helpers.date_utils import calcular_fechas, validar_intervalo_date
from helpers.api_utils import obtener_mejores_datos, obtener_historico_mercados_hasta_hoy



def obtener_datos_historicos(intervalo, tiempo_atras, verbose=False, symbols=None):
    # Cargar configuración de todas las APIs
    config_apis = cargar_configuracion_apis(verbose=verbose)
    
    # Verificar que la configuración se cargó correctamente
    if not config_apis:
        error_msg = "No se pudo cargar la configuración de ninguna API"
        if verbose:
            print(f"    ❌ {error_msg}")
        else:
            print(f"❌ {error_msg}")
        return None
    
    # Verificar que se proporcionaron símbolos (obligatorio)
    if symbols is None:
        error_msg = "No se proporcionaron símbolos para analizar"
        if verbose:
            print(f"    ❌ {error_msg}")
        else:
            print(f"❌ {error_msg}")
        return None
    
    if not symbols:
        error_msg = "La lista de símbolos está vacía"
        if verbose:
            print(f"    ❌ {error_msg}")
        else:
            print(f"❌ {error_msg}")
        return None

    # Validar argumentos
    if not validar_intervalo_date(intervalo):
        error_msg = "Valor de intervalo erróneo"
        if verbose:
            print(f"    ❌ {error_msg}")
        else:
            print(f"❌ {error_msg}")
        return None
        
    if not validar_intervalo_date(tiempo_atras):
        error_msg = "Valor de tiempo_atras erróneo"
        if verbose:
            print(f"    ❌ {error_msg}")
        else:
            print(f"❌ {error_msg}")
        return None

    if verbose:
        print(f"    📊 Obteniendo datos para {len(symbols)} símbolos: {symbols}")
        print(f"    📅 tiempo_atras: {tiempo_atras}")
        print(f"    ⏱️ Intervalo: {intervalo}")
        print(f"    🌍 Timezone: UTC")
        print(f"    🌍 APIs disponibles: {list(config_apis.keys())}")

    # Obtener datos históricos
    historico_mercados_hasta_hoy = {}
    simbolos_fallidos = []
    
    for symbol in symbols:
        if verbose:
            print(f"      🔄 Obteniendo datos para {symbol}...")

        # Usar la función que prueba múltiples APIs
        # Usar la función que prueba múltiples APIs
        datos_symbol = obtener_mejores_datos(
            symbol=symbol,
            intervalo=intervalo,
            tiempo_atras=tiempo_atras,
            config_apis=config_apis,
            timezone="UTC",
            verbose=verbose
        )
        
        # SOLO agregar símbolos que tengan datos válidos
        if datos_symbol is not None and 'values' in datos_symbol and datos_symbol['values']:
            historico_mercados_hasta_hoy[symbol] = datos_symbol
            if verbose:
                print(f"      ✅ Datos obtenidos para {symbol}: {len(datos_symbol['values'])} registros")
        else:
            simbolos_fallidos.append(symbol)
            if verbose:
                print(f"      ❌ No se pudieron obtener datos válidos para {symbol}")

    # Verificar si al menos algunos símbolos obtuvieron datos
    simbolos_con_datos = list(historico_mercados_hasta_hoy.keys())
    
    if verbose:
        print(f"    ✅ Se obtuvieron datos para {len(simbolos_con_datos)} de {len(symbols)} símbolos")
        if simbolos_fallidos:
            print(f"    ❌ Símbolos fallidos: {simbolos_fallidos}")
    
    if not simbolos_con_datos:
        error_msg = "No se pudieron obtener datos para ningún símbolo"
        if verbose:
            print(f"    ❌ {error_msg}")
        else:
            print(f"❌ {error_msg}")
        return None
    
    if verbose:
        print(f"    🎯 Símbolos exitosos para análisis: {simbolos_con_datos}")
    
    return historico_mercados_hasta_hoy


'''
# Ejecución independiente (para pruebas)
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 GetDataTwelveView.py <intervalo> <tiempo_atras>")
        print(f"valores acpetado intervalo: {valores_time_series_validos}")
        print(f"valores acpetado tiempo atras: {valores_time_series_validos}")
        sys.exit(1)

    intervalo = sys.argv[1]
    tiempo_atras = sys.argv[2]
    verbose = sys.argv[3]
    symbols = sys.argv[4]

    datos_historicos = obtener_datos_historicos(intervalo, tiempo_atras, verbose=False, symbols=None)
    print(datos_historicos)'
'''