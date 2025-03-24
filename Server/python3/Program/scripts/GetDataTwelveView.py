import sys
from helpers.config_loader import cargar_configuracion
from helpers.date_utils import calcular_fechas, validar_intervalo_date
from helpers.api_utils import obtener_historico_mercados_hasta_hoy


def obtener_datos_historicos(intervalo, tiempo_atras):
    # Cargar configuración
    url_base_path, symbols, api_key = cargar_configuracion()
    if not url_base_path or not symbols or not api_key:
        return None

    # Validar argumentos con la nueva función
    if not validar_intervalo_date(intervalo):
        print("valor de intervalo erroneo")
        return None
    if not validar_intervalo_date(tiempo_atras):
        print("valor de tiempo_atras erroneo")
        return None

    # Calcular fechas
    start_date, end_date = calcular_fechas(tiempo_atras)
    if not start_date or not end_date:
        print(f"Error: No se pudieron calcular las fechas para el intervalo {tiempo_atras}.")
        return None

    # Obtener datos históricos
    historico_mercados_hasta_hoy = {
        symbol: obtener_historico_mercados_hasta_hoy(url_base_path, symbol, api_key, interval=intervalo, start_date=start_date, end_date=end_date)
        for symbol in symbols
    }
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

    datos_historicos = obtener_datos_historicos(intervalo, tiempo_atras)
    print(datos_historicos)'
'''