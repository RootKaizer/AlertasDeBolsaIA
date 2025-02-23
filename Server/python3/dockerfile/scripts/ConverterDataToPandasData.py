import backtrader as bt
import pandas as pd

# Crear un feed de datos para Backtrader
class MiFeed(bt.feeds.PandasData):
    params = (
        ('datetime', None),  # No usar columna de fecha
        ('open', -1),       # No usar columna de apertura
        ('high', -1),       # No usar columna de máximo
        ('low', -1),        # No usar columna de mínimo
        ('close', 0),       # Usar la columna de cierre (índice 0)
        ('volume', -1),     # No usar columna de volumen
        ('openinterest', -1),  # No usar columna de interés abierto
    )

# Convertir los datos en un DataFrame de Pandas
datos = {"close": [100, 101, 102, 103]}  # Ejemplo de datos
df = pd.DataFrame(datos)

# Crear el feed de datos
data = MiFeed(dataname=df)