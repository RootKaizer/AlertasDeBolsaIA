# Crear una instancia de cerebro (motor de Backtrader)
cerebro = bt.Cerebro()

# Agregar la estrategia
cerebro.addstrategy(MiEstrategia)

# Cargar los datos en tiempo real
data = MiFeed(dataname=pd.DataFrame({"close": [precio] for precio in datos_mercados.values()}))
cerebro.adddata(data)

# Ejecutar la estrategia
cerebro.run()