import requests

def obtener_historico_mercados_hasta_hoy(url_base_path, symbol, api_key, interval, start_date=None, end_date=None):
    url = f"{url_base_path}/time_series?symbol={symbol}&interval={interval}&apikey={api_key}"
    if start_date:
        url += f"&start_date={start_date}"
    if end_date:
        url += f"&end_date={end_date}"
    try:
        response = requests.get(url).json()
        if "code" in response and response["code"] != 200:
            print(f"Error en la API para {symbol}: {response.get('message', 'Error desconocido')}")
            return None
        return response
    except Exception as e:
        print(f"Error al obtener datos para {symbol}: {e}")
        return None