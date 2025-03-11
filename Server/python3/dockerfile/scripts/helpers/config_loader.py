import configparser
import os
import base64

def cargar_configuracion():
    CONFIG_TWELVEDATA = os.path.join(os.path.dirname(__file__), "../../conf/twelvedata.info")
    CONFIG_SNOITCENNOC = os.path.join(os.path.dirname(__file__), "../../conf/.snoitcennoc.info")

    config_twelvedata = configparser.ConfigParser()
    config_twelvedata.read(CONFIG_TWELVEDATA)

    config_snoitcennoc = configparser.ConfigParser()
    config_snoitcennoc.read(CONFIG_SNOITCENNOC)

    try:
        url_base_path = config_twelvedata.get("TwelveData", "url_base_path")
        symbols = config_twelvedata.get("TwelveData", "symbols").split(",")
        encrypted_api_key = config_snoitcennoc.get("TwelveData", "api_key")
        api_key = base64.b64decode(encrypted_api_key).decode("utf-8")
        return url_base_path, symbols, api_key
    except Exception as e:
        print(f"Error al cargar la configuración: {e}")
        return None, None, None