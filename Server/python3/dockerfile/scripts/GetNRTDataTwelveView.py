import time

while True:
    # Obtener datos en tiempo real
    datos_mercados = {symbol: obtener_datos_en_tiempo_real(symbol, api_key) for symbol in symbols}

    # Crear un feed de datos para Backtrader
    data = MiFeed(dataname=pd.DataFrame({"close": [precio] for precio in datos_mercados.values()}))
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MiEstrategia)
    cerebro.adddata(data)

    # Ejecutar la estrategia
    cerebro.run()

    time.sleep(60)  # Esperar 1 minuto antes de la siguiente iteración