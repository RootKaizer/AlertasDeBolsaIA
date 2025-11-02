import sys
from helpers.config_loader import cargar_configuracion
from helpers.date_utils import calcular_fechas, validar_intervalo_date
from helpers.api_utils import obtener_historico_mercados_hasta_hoy


def obtener_datos_historicos(intervalo, tiempo_atras, verbose=False, symbols=None):
    # Cargar configuración con verbose
    config_result = cargar_configuracion(verbose=verbose)
    
    # Verificar que la configuración se cargó correctamente
    if not config_result:
        error_msg = "No se pudo cargar la configuración básica (URL o API Key)"
        if verbose:
            print(f"    ❌ {error_msg}")
        else:
            print(f"❌ {error_msg}")
        return None
    
    url_base_path, api_key = config_result
    
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

    # Validar argumentos con la nueva función
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

    # Calcular fechas
    start_date, end_date = calcular_fechas(tiempo_atras)
    if not start_date or not end_date:
        error_msg = f"No se pudieron calcular las fechas para el intervalo {tiempo_atras}"
        if verbose:
            print(f"    ❌ {error_msg}")
        else:
            print(f"❌ {error_msg}")
        return None

    if verbose:
        print(f"    📊 Obteniendo datos para {len(symbols)} símbolos: {symbols}")
        print(f"    📅 Período: {start_date} hasta {end_date}")
        print(f"    ⏱️  Intervalo: {intervalo}")

    # Obtener datos históricos
    historico_mercados_hasta_hoy = {}
    
    for symbol in symbols:
        if verbose:
            print(f"      🔄 Obteniendo datos para {symbol}...")
            
        datos_symbol = obtener_historico_mercados_hasta_hoy(
            url_base_path, symbol, api_key, 
            interval=intervalo, 
            start_date=start_date, 
            end_date=end_date,
            verbose=verbose
        )
        historico_mercados_hasta_hoy[symbol] = datos_symbol
        
        if verbose:
            if datos_symbol is not None:
                if "values" in datos_symbol:
                    print(f"      ✅ Datos obtenidos para {symbol}: {len(datos_symbol['values'])} registros")
                else:
                    print(f"      ✅ Datos obtenidos para {symbol} (formato diferente)")
            else:
                print(f"      ❌ No se pudieron obtener datos para {symbol}")

    # Verificar si al menos algunos símbolos obtuvieron datos
    simbolos_con_datos = [sym for sym, data in historico_mercados_hasta_hoy.items() if data is not None]
    
    if verbose:
        print(f"    ✅ Se obtuvieron datos para {len(simbolos_con_datos)} de {len(symbols)} símbolos")
    
    if not simbolos_con_datos:
        error_msg = "No se pudieron obtener datos para ningún símbolo"
        if verbose:
            print(f"    ❌ {error_msg}")
        else:
            print(f"❌ {error_msg}")
        return None
    
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