# =========================================================================
# Librerias
# =========================================================================
import requests
import configparser
import os
import base64

# =========================================================================
# Variables Globales
# =========================================================================
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

def obtener_datos_en_tiempo_real(symbol, api_key):
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




# =========================================================================
# Logica Principal
# =========================================================================
# Llamar la función obtener_datos_en_tiempo_real
datos_mercados = {symbol: obtener_datos_en_tiempo_real(symbol, api_key) for symbol in symbols}
#print(datos_mercados)


# Imprimir los datos obtenidos de la función obtener_datos_en_tiempo_real
print("Precios en tiempo real:")
for symbol, precio in datos_mercados.items():
    if precio is not None:
        print(f"{symbol}: {precio}")
    else:
        print(f"{symbol}: No se pudo obtener el precio")