# styles/exit_console.py
import pandas as pd

def mostrar_resultados_trading(estrategia, resultados, tipo="actuales"):
    """
    Muestra los resultados del análisis de trading de forma organizada.
    
    :param estrategia: Nombre de la estrategia utilizada
    :param resultados: Diccionario con los DataFrames de resultados
    :param tipo: Tipo de resultados ("actuales" o "anteriores")
    """
    print(f"\n{'='*80}")
    print(f"📊 RESULTADOS {tipo.upper()} - ESTRATEGIA: {estrategia.upper()}")
    print(f"{'='*80}")
    
    for symbol, df in resultados.items():
        if len(df) == 0:
            continue
            
        ultimo = df.iloc[-1]
        
        print(f"\n🎯 {symbol}:")
        print(f"  📈 Precio: {ultimo['Close']:.2f}")
        print(f"  📅 Fecha: {ultimo['datetime']}")
        
        # Mostrar estrategias disponibles de forma segura
        estrategias_disponibles = [col for col in df.columns if col.startswith('estrategia_') and not col.endswith(('_valor', '_descripcion'))]
        
        for estrategia_col in estrategias_disponibles:
            if estrategia_col in ultimo and not pd.isna(ultimo[estrategia_col]):
                # Obtener la descripción si existe
                desc_col = f"{estrategia_col}_descripcion"
                descripcion = ultimo[desc_col] if desc_col in ultimo and not pd.isna(ultimo[desc_col]) else "Sin descripción"
                
                print(f"  {estrategia_col.replace('estrategia_', '').upper()}: {ultimo[estrategia_col]} - {descripcion}")
        
        # Mostrar estrategia mayoritaria si existe
        if 'estrategia_mayoritaria' in ultimo and not pd.isna(ultimo['estrategia_mayoritaria']):
            print(f"  🎯 ESTRATEGIA MAYORITARIA: {ultimo['estrategia_mayoritaria']}")
        
        # Mostrar fuerza de señal si existe
        if 'fuerza_señal' in ultimo and not pd.isna(ultimo['fuerza_señal']):
            fuerza = ultimo['fuerza_señal']
            if fuerza > 0.5:
                intensidad = "MUY FUERTE 🟢"
            elif fuerza > 0.2:
                intensidad = "FUERTE 🟡"
            elif fuerza > -0.2:
                intensidad = "NEUTRA ⚪"
            elif fuerza > -0.5:
                intensidad = "DÉBIL 🟠"
            else:
                intensidad = "MUY DÉBIL 🔴"
            print(f"  💪 FUERZA DE SEÑAL: {fuerza:.2f} ({intensidad})")
    
    print(f"\n{'='*80}")
    print(f"Total símbolos analizados: {len(resultados)}")
    print(f"{'='*80}")