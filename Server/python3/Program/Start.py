#!/usr/bin/env python3
"""
Script principal que coordina el sistema completo de análisis de mercados.
"""

import sys
import os

# Agregar la carpeta scripts al path para importar los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from scripts.DebugMotorBolsaIA import DebugMotorBolsaIA
from scripts.NotificationLogicSender import comparar_y_notificar
from scripts.styles.title_console import mostrar_titulo_estrategia
from scripts.styles.exit_console import mostrar_resultados_trading
from scripts.ObtenerIndicesDelMercado import obtener_indices_mercado



def mostrar_uso():
    """
    Muestra el uso correcto del script
    """
    print("🚀 SISTEMA DE ANÁLISIS DE MERCADOS - USO:")
    print("python Start.py <estrategia> [debug]")
    print("")
    print("📋 ESTRATEGIAS DISPONIBLES:")
    print("   - corto_plazo     (Trading intradía)")
    print("   - mediano_plazo   (Swing trading)") 
    print("   - largo_plazo     (Inversión a largo plazo)")
    print("   - agresivo        (Scalping alto riesgo)")
    print("   - conservador     (Inversión conservadora)")
    print("")
    print("🔍 OPCIONES DEBUG:")
    print("   - true/1/yes/y/verdadero  -> Activar modo debug")
    print("   - false/0/no/n/falso       -> Modo normal (por defecto)")
    print("")
    print("💡 EJEMPLOS:")
    print("   python Start.py mediano_plazo")
    print("   python Start.py corto_plazo true")
    print("   python Start.py agresivo 1")



def main():
    """
    Función principal del sistema
    """
    # Paso 0: Verificar argumentos de línea de comandos
    if len(sys.argv) < 2:
        print("❌ ERROR: Debes especificar una estrategia")
        mostrar_uso()
        return
    
    # Primer parámetro: estrategia
    estrategia = sys.argv[1].lower()
    
    # Estrategias válidas
    estrategias_validas = ['corto_plazo', 'mediano_plazo', 'largo_plazo', 'agresivo', 'conservador']
    
    if estrategia not in estrategias_validas:
        print(f"❌ ERROR: Estrategia '{estrategia}' no válida")
        mostrar_uso()
        return
    
    # Segundo parámetro: modo debug (opcional)
    modo_debug = False
    if len(sys.argv) > 2:
        debug_arg = sys.argv[2].lower()
        if debug_arg in ['true', '1', 'yes', 'y', 'verdadero']:
            modo_debug = True
            print("🔍 MODO DEBUG ACTIVADO")
        elif debug_arg in ['false', '0', 'no', 'n', 'falso']:
            modo_debug = False
            print("⚡ MODO NORMAL")
        else:
            print(f"⚠️  Argumento de debug no reconocido: {debug_arg}. Usando modo normal.")
    else:
        print("⚡ MODO NORMAL (por defecto)")
    
    # Inicializar el modo debug
    debug = DebugMotorBolsaIA()
    
    # Mostrar banner del sistema
    mostrar_titulo_estrategia("SISTEMA DE ANÁLISIS DE MERCADOS")
    print(f"🎯 Estrategia seleccionada: {estrategia.upper()}")
    print(f"🔍 Modo debug: {'ACTIVADO' if modo_debug else 'DESACTIVADO'}")
    print("=" * 80)

    try:
        # Paso 1: Obtener índices del mercado
        debug.escribir_paso(1, "obtener_indices_mercado", {
            "estrategia": estrategia,
            "modo_debug": modo_debug
        })
        
        print("\n📊 PASO 1: Obteniendo índices del mercado...")
        resultados_trading = obtener_indices_mercado(estrategia, modo_debug)
        
        if not resultados_trading:
            print("❌ Error al obtener los índices del mercado")
            return
        
        debug.escribir_paso(1, "obtener_indices_mercado", {}, 
                          respuesta=f"Índices obtenidos: {len(resultados_trading)} símbolos")

        # Paso 2: Mostrar resultados
        debug.escribir_paso(2, "mostrar_resultados", {
            "estrategia": estrategia,
            "resultados_count": len(resultados_trading)
        })
        
        print(f"\n📈 PASO 2: Mostrando resultados para {len(resultados_trading)} símbolos...")
        mostrar_resultados_trading(estrategia, resultados_trading, "actuales")

        '''
        # Paso 3: Notificaciones (opcional - puedes comentar si no quieres notificaciones)
        debug.escribir_paso(3, "procesar_notificaciones", {
            "estrategia": estrategia
        })
        
        print(f"\n🔔 PASO 3: Procesando notificaciones...")
        # Aquí puedes agregar la lógica de notificaciones si la necesitas
        # resultado_notificacion = comparar_y_notificar(...)
        
        print("✅ PROCESO COMPLETADO EXITOSAMENTE")
        '''
        
        return resultados_trading

    except Exception as e:
        print(f"❌ ERROR en el proceso principal: {e}")
        debug.escribir_error("main", str(e))
        return None

if __name__ == "__main__":
    main()