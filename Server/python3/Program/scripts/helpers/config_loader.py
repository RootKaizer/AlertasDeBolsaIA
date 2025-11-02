import configparser
import os
import base64

def cargar_configuracion(verbose=False):
    CONFIG_TWELVEDATA = os.path.join(os.path.dirname(__file__), "../../conf/twelvedata.info")
    CONFIG_SNOITCENNOC = os.path.join(os.path.dirname(__file__), "../../conf/.snoitcennoc.info")

    config_twelvedata = configparser.ConfigParser()
    config_twelvedata.read(CONFIG_TWELVEDATA)

    config_snoitcennoc = configparser.ConfigParser()
    config_snoitcennoc.read(CONFIG_SNOITCENNOC)

    try:
        # Cargar URL base (obligatorio)
        url_base_path = config_twelvedata.get("TwelveData", "url_base_path")
        if verbose:
            print(f"    ✅ URL base cargada: {url_base_path}")
        
        # Cargar API Key (obligatorio)
        encrypted_api_key = config_snoitcennoc.get("TwelveData", "api_key")
        api_key = base64.b64decode(encrypted_api_key).decode("utf-8")
        if verbose:
            print(f"    ✅ API Key cargada correctamente")
        
        # SOLO retornar url_base_path y api_key, symbols se maneja desde estrategias
        return url_base_path, api_key
        
    except configparser.NoSectionError as e:
        error_msg = f"No se encontró la sección 'TwelveData' en los archivos de configuración: {e}"
        if verbose:
            print(f"    ❌ {error_msg}")
        else:
            print(f"❌ {error_msg}")
        return None, None
        
    except configparser.NoOptionError as e:
        error_msg = f"Falta una opción obligatoria en la configuración: {e}"
        if verbose:
            print(f"    ❌ {error_msg}")
        else:
            print(f"❌ {error_msg}")
        return None, None
        
    except Exception as e:
        error_msg = f"Error inesperado al cargar la configuración: {e}"
        if verbose:
            print(f"    ❌ {error_msg}")
        else:
            print(f"❌ {error_msg}")
        return None, None