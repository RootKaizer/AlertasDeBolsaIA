# =========================================================================
# Librerias
# =========================================================================
import requests
import configparser
import os
import base64
import re

# =========================================================================
# Variables Globales
# =========================================================================

# Variables propias del script
opciones_afirmativas_validas = {"y", "yes", "s", "si"}

# obtener archivos relacionados
CONFIG_TWELVEDATA = os.path.join(os.path.dirname(__file__), "../conf/twelvedata.info")
CONFIG_SNOITCENNOC = os.path.join(os.path.dirname(__file__), "../conf/.snoitcennoc.info")

# Asignar el contenido a una variable
config_twelvedata = configparser.ConfigParser()
config_twelvedata.read(CONFIG_TWELVEDATA)

config_snoitcennoc = configparser.ConfigParser()
config_snoitcennoc.read(CONFIG_SNOITCENNOC)


# Leer valores desde el archivo de configuración
# -- url api finance twelvedata
try:
    url_base_path = config_twelvedata.get("TwelveData", "url_base_path")
    if not url_base_path:
        raise ValueError("No se encontró la clave 'url_base_path' en el archivo de configuración twelvedata.info.")
except Exception as e:
    print(f"Error in file twelvedata.info: {e}")
    exit(1)  # Salir con código de error

# -- Listado de mercados a monitorear
try:
    symbols = config_twelvedata.get("TwelveData", "symbols")
    if not symbols:
        raise ValueError("No se encontró la clave 'symbols' en el archivo de configuración twelvedata.info.")
    symbols = symbols.split(",")
except Exception as e:
    print(f"Error in file twelvedata.info: {e}")
    exit(1)  # Salir con código de error

# -- valor time_series_interval
try:
    time_series_interval = config_twelvedata.get("TwelveData", "time_series_interval")
    if not time_series_interval:
        raise ValueError("No se encontró la clave 'time_series_interval' en el archivo de configuración twelvedata.info.")
    time_series_interval = re.sub(r"['\"]", "", time_series_interval.strip())
except Exception as e:
    print(f"Error in file twelvedata.info: {e}")
    exit(1)  # Salir con código de error

# -- valor quieres_conseguir_precio_actual_mercados
try:
    quieres_conseguir_precio_actual_mercados = config_twelvedata.get("OptionsRun", "quieres_conseguir_precio_actual_mercados")
    if not quieres_conseguir_precio_actual_mercados:
        raise ValueError("No se encontró la clave 'quieres_conseguir_precio_actual_mercados' en el archivo de configuración twelvedata.info.")
    quieres_conseguir_precio_actual_mercados = re.sub(r"['\"]", "", quieres_conseguir_precio_actual_mercados.strip().lower())
except Exception as e:
    print(f"Error in file twelvedata.info: {e}")
    exit(1)  # Salir con código de error

# -- valor quieres_conseguir_time_series_interval_mercados
try:
    quieres_conseguir_time_series_interval_mercados = config_twelvedata.get("OptionsRun", "quieres_conseguir_time_series_interval_mercados")
    if not quieres_conseguir_time_series_interval_mercados:
        raise ValueError("No se encontró la clave 'quieres_conseguir_time_series_interval_mercados' en el archivo de configuración twelvedata.info.")
    quieres_conseguir_time_series_interval_mercados = re.sub(r"['\"]", "", quieres_conseguir_time_series_interval_mercados.strip().lower())
except Exception as e:
    print(f"Error in file twelvedata.info: {e}")
    exit(1)  # Salir con código de error


# -- sin importancia T.T
try:
    encrypted_api_key = config_snoitcennoc.get("TwelveData", "api_key")
    if not encrypted_api_key:
        raise ValueError("No se encontró la clave 'api_key' en el archivo de configuración .snoitcennoc.info.")
except Exception as e:
    print(f"Error in file .snoitcennoc.info: {e}")
    exit(1)  # Salir con código de error
api_key = base64.b64decode(encrypted_api_key).decode("utf-8")




# =========================================================================
# Funciones
# =========================================================================
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



def obtener_time_series_interval_mercados(symbol, api_key):
    url = f"{url_base_path}/time_series?symbol={symbol}&interval={time_series_interval}&apikey={api_key}"
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




# =========================================================================
# Logica Principal
# =========================================================================
print("=======================================")
print(f"La configuración de la ejecución es: ")
print(f"Elegiste conseguir datos del precio actual de mercados: {quieres_conseguir_precio_actual_mercados}")
print(f"Elegiste conseguir time series interval de mercados: {quieres_conseguir_time_series_interval_mercados}")
print("=======================================")
print(f"")
print(f"")

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
    time_series_interval_mercados = {symbol: obtener_time_series_interval_mercados(symbol, api_key) for symbol in symbols}
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
