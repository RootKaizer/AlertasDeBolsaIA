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



def cargar_configuracion_alpha_vantage(verbose=False):
    """
    Carga la configuración específica para Alpha Vantage desde .snoitcennoc.info
    """
    CONFIG_SNOITCENNOC = os.path.join(os.path.dirname(__file__), "../../conf/.snoitcennoc.info")
    
    config_snoitcennoc = configparser.ConfigParser()
    config_snoitcennoc.read(CONFIG_SNOITCENNOC)

    try:
        # Cargar API Key de Alpha Vantage desde .snoitcennoc.info
        encrypted_api_key = config_snoitcennoc.get("AlphaVantage", "api_key")
        api_key = base64.b64decode(encrypted_api_key).decode("utf-8")
        
        if verbose:
            print(f"    ✅ API Key de Alpha Vantage cargada correctamente")
            
        return api_key
        
    except configparser.NoSectionError:
        if verbose:
            print(f"    ⚠️  No se encontró la sección 'AlphaVantage' en .snoitcennoc.info")
        return None
        
    except configparser.NoOptionError:
        if verbose:
            print(f"    ⚠️  No se encontró la opción 'api_key' en la sección AlphaVantage")
        return None
        
    except Exception as e:
        if verbose:
            print(f"    ❌ Error cargando configuración Alpha Vantage: {e}")
        return None



def cargar_configuracion_apis(verbose=False):
    """
    Carga configuración para todas las APIs disponibles
    """
    config_apis = {}
    
    # Cargar Twelve Data (configuración principal)
    config_result = cargar_configuracion(verbose=verbose)
    if config_result:
        url_base_path, api_key = config_result
        config_apis['twelvedata'] = {
            'url_base_path': url_base_path,
            'api_key': api_key
        }
        if verbose:
            print("    ✅ Configuración Twelve Data cargada")
    
    # Cargar Alpha Vantage
    alpha_key = cargar_configuracion_alpha_vantage(verbose=verbose)
    if alpha_key:
        config_apis['alpha_vantage'] = {'api_key': alpha_key}
        if verbose:
            print("    ✅ Configuración Alpha Vantage cargada")
    elif verbose:
        print("    ⚠️  Alpha Vantage no configurado")
    
    # Yahoo Finance no necesita API key, siempre disponible
    config_apis['yahoo_finance'] = {'enabled': True}
    if verbose:
        print("    ✅ Yahoo Finance disponible")
    
    return config_apis