import requests

def obtener_historico_mercados_hasta_hoy(url_base_path, symbol, api_key, interval, start_date=None, end_date=None, verbose=False):
    url = f"{url_base_path}/time_series?symbol={symbol}&interval={interval}&apikey={api_key}"
    if start_date:
        url += f"&start_date={start_date}"
    if end_date:
        url += f"&end_date={end_date}"
    
    if verbose:
        print(f"    🌐 Consultando API para {symbol}: {url.replace(api_key, 'API_KEY_REDACTED')}")
    
    try:
        response = requests.get(url).json()
        
        if verbose:
            print(f"    📥 Respuesta recibida para {symbol}")
        
        if "code" in response and response["code"] != 200:
            error_msg = f"Error en la API para {symbol}: {response.get('message', 'Error desconocido')}"
            if verbose:
                print(f"    ❌ {error_msg}")
            return None
        
        if verbose:
            if "values" in response:
                print(f"    ✅ Datos obtenidos para {symbol}: {len(response['values'])} registros")
            else:
                print(f"    ⚠️  Respuesta inesperada para {symbol}: {response.keys()}")
                
        return response
        
    except Exception as e:
        error_msg = f"Error al obtener datos para {symbol}: {e}"
        if verbose:
            print(f"    ❌ {error_msg}")
        return None