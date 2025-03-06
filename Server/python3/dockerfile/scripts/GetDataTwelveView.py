# =========================================================================
# Librerias
# =========================================================================
import requests
import configparser
import os
import base64
import re
import sys
import urllib.parse  # Para codificar correctamente la URL
from datetime import datetime, timedelta


# =========================================================================
# Variables Globales
# =========================================================================

# Variables propias del script
opciones_afirmativas_validas = {"y", "yes", "s", "si"}
opciones_modo_ejecucion_validas = {"actual", "time_series", "historico", "historico_ahora"}
valores_time_series_validos = {"1min", "5min", "15min", "30min", "45min", "1h", "2h", "4h", "8h", "1day", "1week", "1month", "1year"}
fecha_regex = re.compile(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$")
formato_fecha_valido = "el formato de fecha valido es YYYY-MM-DD con un mes (01-12) y un día (01-31) o estar vacío"

# obtener archivos relacionados
CONFIG_TWELVEDATA = os.path.join(os.path.dirname(__file__), "../conf/twelvedata.info")
CONFIG_SNOITCENNOC = os.path.join(os.path.dirname(__file__), "../conf/.snoitcennoc.info")

# Asignar el contenido a una variable
config_twelvedata = configparser.ConfigParser()
config_twelvedata.read(CONFIG_TWELVEDATA)

config_snoitcennoc = configparser.ConfigParser()
config_snoitcennoc.read(CONFIG_SNOITCENNOC)


# Leer valores desde el archivo de configuración
try:
    # -- url api finance twelvedata
    url_base_path = config_twelvedata.get("TwelveData", "url_base_path")
    if not url_base_path:
        raise ValueError("No se encontró la clave 'url_base_path' en el archivo de configuración twelvedata.info.")

    # -- lista de mercados a consultar
    symbols = config_twelvedata.get("TwelveData", "symbols")
    if not symbols:
        raise ValueError("No se encontró la clave 'symbols' en el archivo de configuración twelvedata.info.")
    symbols = symbols.split(",")

    # -- log//ing twelveData
    encrypted_api_key = config_snoitcennoc.get("TwelveData", "api_key")
    if not encrypted_api_key:
        raise ValueError("No se encontró la clave 'api_key' en el archivo de configuración .snoitcennoc.info.")

    api_key = base64.b64decode(encrypted_api_key).decode("utf-8")

except Exception as e:
    print(f"Error in file twelvedata.info: {e}")
    exit(1)  # Salir con código de error


# =========================================================================
# Validar Argumentos inciales
# =========================================================================
if len(sys.argv) < 2:
    print(f"Uso: python3 GetDataTwelveView.py {opciones_modo_ejecucion_validas}")
    sys.exit(1)

modo_ejecucion = sys.argv[1].lower()

quieres_conseguir_precio_actual_mercados = "y" if modo_ejecucion == "actual" else "n"
quieres_conseguir_time_series_interval_mercados = "y" if modo_ejecucion == "time_series" else "n"
quieres_conseguir_historico_mercados = "y" if modo_ejecucion == "historico" else "n"
quieres_conseguir_historico_mercados_hasta_hoy = "y" if modo_ejecucion == "historico_ahora" else "n"

if modo_ejecucion not in opciones_modo_ejecucion_validas:
    print(f"Error: {modo_ejecucion} no es un intervalo válido")
    print(f"Error: Elije 1 valor valido: {opciones_modo_ejecucion_validas}")
    sys.exit(1)

"""



if historical_start_date and not fecha_regex.match(historical_start_date):
    print("Error: historical_start_date debe tener el formato YYYY-MM-DD o estar vacío")
    sys.exit(1)

if historical_end_date and not fecha_regex.match(historical_end_date):
    print("Error: historical_end_date debe tener el formato YYYY-MM-DD o estar vacío")
    sys.exit(1)
"""



# =========================================================================
# Funciones
# =========================================================================
def convertir_a_segundos(intervalo):
    conversion = {
        "min": 60,
        "h": 60 * 60,
        "day": 24 * 60 * 60,
        "week": 7 * 24 * 60 * 60,
        "month": 30 * 24 * 60 * 60,  # Aproximado a 30 días
        "year": 365 * 24 * 60 * 60  # Aproximado a 365 días
    }
    
    # Extraer número y unidad usando regex
    match = re.match(r"(\d+)([a-zA-Z]+)", intervalo)
    if not match:
        return None  # Formato inválido
    
    cantidad, unidad = match.groups()
    cantidad = int(cantidad)

    # Verificar si la unidad es válida
    if unidad not in conversion:
        return None
    
    return cantidad * conversion[unidad]



def calcular_fechas(intervalo):
    segundos = convertir_a_segundos(intervalo)
    if segundos is None:
        return None, None  # Valor inválido

    # Obtener la fecha actual
    end_date = datetime.now().strftime("%Y-%m-%dT%H:%M")

    # Calcular start_date restando los segundos
    start_date = (datetime.now() - timedelta(seconds=segundos)).strftime("%Y-%m-%dT%H:%M")

    # Codificar el espacio como %20 para URLs
    end_date_encoded = urllib.parse.quote(end_date)
    start_date_encoded = urllib.parse.quote(start_date)

    return start_date_encoded, end_date_encoded



def obtener_precio_en_tiempo_real(symbol, api_key):
    url = f"{url_base_path}/price?symbol={symbol}&apikey={api_key}"
    try:
        response = requests.get(url).json()
        #print(f"Respuesta de la API para {symbol}: {response}")  # Imprimir la respuesta completa
        # Verificar si la respuesta contiene un error
        if "code" in response and response["code"] != 200:
            print(f"Error en la API para {symbol}: {response.get('message', 'Error desconocido')}")
            return None

        # Verificar si la respuesta contiene la clave "price"
        if "price" in response:
            return float(response["price"])
        else:
            print(f"Error: La respuesta no contiene 'price' para {symbol}. Respuesta: {response}")
            return None
    except Exception as e:
        print(f"Error al obtener datos para {symbol}: {e}")
        return None



def obtener_time_series_interval_mercados(symbol, api_key, interval):
    # obtener url
    url = f"{url_base_path}/time_series?symbol={symbol}&interval={interval}&apikey={api_key}"
    #print(f"{url}")

    try:
        response = requests.get(url).json()
        #print(f"Respuesta de la API para {symbol}: {response}")  # Imprimir la respuesta completa
        # Verificar si la respuesta contiene un error
        if "code" in response and response["code"] != 200:
            print(f"Error en la API para {symbol}: {response.get('message', 'Error desconocido')}")
            return None

        # Verificar si la respuesta contiene los datos esperados
        if "values" in response:
            data = response["values"][0]  # Tomamos el primer dato disponible (última actualización)
            result = {
                'datetime': data.get('datetime', None),  # No usar columna de fecha
                'open': data.get('open', -1),             # No usar columna de apertura
                'high': data.get('high', -1),             # No usar columna de máximo
                'low': data.get('low', -1),               # No usar columna de mínimo
                'close': data.get('close', 0),            # Usar la columna de cierre (índice 0)
                'volume': data.get('volume', -1),         # No usar columna de volumen
                'openinterest': data.get('openinterest', -1)  # No usar columna de interés abierto
            }
            return result
        else:
            print(f"Error: La respuesta no contiene 'values' para {symbol}. Respuesta: {response}")
            return None
    except Exception as e:
        print(f"Error al obtener datos para {symbol}: {e}")
        return None



def obtener_historico_mercados(symbol, api_key, interval, start_date=None, end_date=None):
    # url base
    url = f"{url_base_path}/time_series?symbol={symbol}&interval={interval}&apikey={api_key}"
    # Agregar las fechas si se proporcionan
    if start_date:
        url += f"&start_date={start_date}"
    if end_date:
        url += f"&end_date={end_date}"
    
    print(f"URL de consulta: {url}")
    
    try:
        response = requests.get(url).json()
        
        if "code" in response and response["code"] != 200:
            print(f"Error en la API para {symbol}: {response.get('message', 'Error desconocido')}")
            return None
        
        return response  # Retornar toda la respuesta incluyendo metadata y valores
    
    except Exception as e:
        print(f"Error al obtener datos para {symbol}: {e}")
        return None



def obtener_historico_mercados_hasta_hoy(symbol, api_key, interval, start_date=None, end_date=None):
    # url base
    url = f"{url_base_path}/time_series?symbol={symbol}&interval={interval}&apikey={api_key}"
    # Agregar las fechas si se proporcionan
    if start_date:
        url += f"&start_date={start_date}"
    if end_date:
        url += f"&end_date={end_date}"
    
    print(f"URL de consulta: {url}")
    
    try:
        response = requests.get(url).json()
        
        if "code" in response and response["code"] != 200:
            print(f"Error en la API para {symbol}: {response.get('message', 'Error desconocido')}")
            return None
        
        return response  # Retornar toda la respuesta incluyendo metadata y valores
    
    except Exception as e:
        print(f"Error al obtener datos para {symbol}: {e}")
        return None




# =========================================================================
# Logica Principal
# =========================================================================
print("=======================================")
print(f"Modo de ejecución: {modo_ejecucion}")
print("=======================================")


# Validación para ejecutar la función precio_actual_mercados
if quieres_conseguir_precio_actual_mercados in opciones_afirmativas_validas:
    print("Llamar la función obtener_datos_en_tiempo_real")
    precio_actual_mercados = {symbol: obtener_precio_en_tiempo_real(symbol, api_key) for symbol in symbols}
    # Imprimir resultado
    print("=======================================")
    print("Precios en tiempo real:")
    for symbol, precio in precio_actual_mercados.items():
        if precio is not None:
            print(f"{symbol}: {precio}")
        else:
            print(f"{symbol}: No se pudo obtener el precio")
    print("")
    print("")





# Validación para ejecutar la función quieres_conseguir_time_series_interval_mercados
if quieres_conseguir_time_series_interval_mercados in opciones_afirmativas_validas:
    print("Llamar la función time_series_interval_mercados")
    # Validar Cantidad de Argumentos inciales
    if len(sys.argv) < 3:
        print(f"Uso: python3 GetDataTwelveView.py {modo_ejecucion} interval({', '.join(valores_time_series_validos)})")
        sys.exit(1)
    # asignar valor del arcgumento 2 como intervalo
    time_series_interval = sys.argv[2]
    # validar que las variables tenga un valor valido
    if time_series_interval not in valores_time_series_validos:
        print(f"Error: {time_series_interval} no es un intervalo válido")
        sys.exit(1)

    time_series_interval_mercados = {symbol: obtener_time_series_interval_mercados(symbol, api_key, interval=time_series_interval) for symbol in symbols}
    # Imprimir los datos obtenidos de la función obtener_datos_en_tiempo_real
    print("=======================================")
    print(f"Datos de series de tiempo para intervalo de {time_series_interval}:")
    for symbol, datos in time_series_interval_mercados.items():
        if datos is not None:
            print(f"\nDatos para {symbol}:")
            print(f"  Fecha y hora: {datos['datetime']}")
            print(f"  Apertura: {datos['open']}")
            print(f"  Máximo: {datos['high']}")
            print(f"  Mínimo: {datos['low']}")
            print(f"  Cierre: {datos['close']}")
            print(f"  Volumen: {datos['volume']}")
            print(f"  Interés abierto: {datos['openinterest']}")
        else:
            print(f"{symbol}: No se pudo obtener los datos")
    print("")
    print("")





# Validación para ejecutar la función quieres_conseguir_historico_mercados
if quieres_conseguir_historico_mercados in opciones_afirmativas_validas:
    print("Llamar la función historico_mercados")
    # Validar Cantidad de Argumentos inciales
    if len(sys.argv) < 3:
        print(f"Uso: python3 GetDataTwelveView.py {modo_ejecucion} interval({', '.join(valores_time_series_validos)}) start_date(YYYY-MM-DD) end_date(YYYY-MM-DD)")
        sys.exit(1)
    # asignar valor del arcgumentos
    time_series_interval = sys.argv[2]
    historical_start_date = sys.argv[3]
    historical_end_date = sys.argv[4]

    # validar que las variables tenga un valor valido
    if time_series_interval not in valores_time_series_validos:
        print(f"Error: {time_series_interval} no es un intervalo válido >> {valores_time_series_validos}")
        sys.exit(1)
    if historical_start_date and not fecha_regex.match(historical_start_date):
        print(f"Error: historical_start_date debe tener {formato_fecha_valido}")
        sys.exit(1)
    if historical_end_date and not fecha_regex.match(historical_end_date):
        print(f"Error: historical_end_date debe tener {formato_fecha_valido}")
        sys.exit(1)


    # Ejecutar Funcion
    historico_mercados = {
        symbol: obtener_historico_mercados(symbol, api_key, interval=time_series_interval, start_date=historical_start_date, end_date=historical_end_date)
        for symbol in symbols
    }


    # Imprimir los datos obtenidos de la función obtener_datos_en_tiempo_real
    print("=======================================")
    print(f"Histórico del mercados, para el intervalo {time_series_interval}")
    print(f"desde '{historical_start_date}' - hasta '{historical_end_date}'")
    print("-------------------------------------------------------------------")
    #print(f"{historico_mercados.items()}")
    for symbol, historico in historico_mercados.items():  # 🔹 Usar el diccionario correcto aquí
        #print("analizando registro por registro")
        if isinstance(historico, dict) and 'values' in historico:
            #print("aprobado la verificación de lista")
            print("\n\n*************")
            print(f"Histórico para {symbol}:")
            print("*************")
            if historico['values']:
                for registro in historico['values']:  # ✅ Ahora está correctamente indentado
                    if isinstance(registro, dict):  # Verificar que registro sea un diccionario
                        print(f"Fecha: {registro.get('datetime', 'N/A')}, Apertura: {registro.get('open', 'N/A')}, "
                            f"Alto: {registro.get('high', 'N/A')}, Bajo: {registro.get('low', 'N/A')}, "
                            f"Cierre: {registro.get('close', 'N/A')}, Volumen: {registro.get('volume', 'N/A')}")
                    else:
                        print("Error: Registro no es un diccionario")
            else:
                print("Error: Los datos no contienen 'values' o no son del tipo esperado")
    print("")
    print("")





# Validación para ejecutar la función quieres_conseguir_time_series_interval_mercados
if quieres_conseguir_historico_mercados_hasta_hoy in opciones_afirmativas_validas:
    print("Llamar la función historico_mercados hasta hoy")
    # Validar Cantidad de Argumentos inciales
    if len(sys.argv) < 3:
        print(f"Uso: python3 GetDataTwelveView.py {modo_ejecucion} interval({', '.join(valores_time_series_validos)}) time_ago({', '.join(valores_time_series_validos)})")
        sys.exit(1)
    # asignar valor del arcgumentos
    time_series_interval = sys.argv[2]
    time_ago = sys.argv[3]
    

    # validar que las variables tenga un valor valido
    if time_series_interval not in valores_time_series_validos:
        print(f"Error: {time_series_interval} no es un intervalo válido >> {valores_time_series_validos}")
        sys.exit(1)
    if time_ago not in valores_time_series_validos:
        print(f"Error: {time_ago} no es un intervalo válido >> {valores_time_series_validos}")
        sys.exit(1)

    # Trasnformar intervalo de tiempo a fechas
    # Ejemplo de uso
    start_date, end_date = calcular_fechas(time_ago)
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}") 


    # Ejecutar Funcion
    historico_mercados_hasta_hoy = {
        symbol: obtener_historico_mercados_hasta_hoy(symbol, api_key, interval=time_series_interval, start_date=start_date, end_date=end_date)
        for symbol in symbols
    }


    # Imprimir los datos obtenidos de la función obtener_datos_en_tiempo_real
    print("=======================================")
    print(f"Histórico del mercados, para el intervalo {time_series_interval}")
    print(f"desde '{start_date}' - hasta '{start_date}'")
    print("-------------------------------------------------------------------")
    #print(f"{historico_mercados.items()}")
    for symbol, historico in historico_mercados_hasta_hoy.items():  # 🔹 Usar el diccionario correcto aquí
        #print("analizando registro por registro")
        if isinstance(historico, dict) and 'values' in historico:
            #print("aprobado la verificación de lista")
            print("\n\n*************")
            print(f"Histórico para {symbol}:")
            print("*************")
            if historico['values']:
                for registro in historico['values']:  # ✅ Ahora está correctamente indentado
                    if isinstance(registro, dict):  # Verificar que registro sea un diccionario
                        print(f"Fecha: {registro.get('datetime', 'N/A')}, Apertura: {registro.get('open', 'N/A')}, "
                            f"Alto: {registro.get('high', 'N/A')}, Bajo: {registro.get('low', 'N/A')}, "
                            f"Cierre: {registro.get('close', 'N/A')}, Volumen: {registro.get('volume', 'N/A')}")
                    else:
                        print("Error: Registro no es un diccionario")
            else:
                print("Error: Los datos no contienen 'values' o no son del tipo esperado")
    print("")
    print("")
