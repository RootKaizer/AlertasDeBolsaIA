#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión con Kimi (Moonshot AI) y DeepSeek
uso: python3 testKimiIA.py
"""

import os
import sys


def test_imports():
    """Verificar que las librerías necesarias están instaladas"""
    print("=" * 60)
    print("🔍 VERIFICANDO IMPORTACIONES")
    print("=" * 60)

    librerias = [
        ("numpy", "numpy"),
        ("scipy", "scipy"),
        ("pandas", "pandas"),
        ("matplotlib", "matplotlib"),
        ("openai", "openai"),
    ]

    todas_ok = True
    for nombre, modulo in librerias:
        try:
            mod = __import__(modulo)
            version = getattr(mod, "__version__", "N/A")
            print(f"  ✅ {nombre}: {version}")
        except ImportError as e:
            print(f"  ❌ {nombre}: NO INSTALADO ({e})")
            todas_ok = False

    return todas_ok


def test_kimi_conexion(api_key=None):
    """
    Probar conexión con la API de Kimi (Moonshot AI)

    Args:
        api_key: Clave API de Kimi. Si es None, busca en variable de entorno KIMI_API_KEY
    """
    print()
    print("=" * 60)
    print("🤖 PROBANDO CONEXIÓN CON KIMI (Moonshot AI)")
    print("=" * 60)

    # Obtener API Key
    if api_key is None:
        api_key = os.environ.get("KIMI_API_KEY")

    if not api_key:
        print("  ⚠️  No se encontró API Key.")
        print("     Opciones para proporcionarla:")
        print("     1. Exportar variable de entorno: export KIMI_API_KEY='tu-key'")
        print("     2. Pasar como argumento: python3 testKimiIA.py --key TU_KEY")
        print()
        print("     Para obtener una API Key gratuita:")
        print("     • https://platform.kimi.ai/console/api-keys")
        print("     • https://build.nvidia.com/moonshotai/kimi-k2.5")
        return False

    try:
        from openai import OpenAI

        # Configurar cliente para Kimi (compatible con OpenAI)
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.moonshot.ai/v1"
        )

        print(f"  📝 API Key configurada: {api_key[:8]}...{api_key[-4:]}")
        print("  🌐 Base URL: https://api.moonshot.ai/v1")
        print()
        print("  ⏳ Enviando mensaje de prueba a Kimi K2.5...")
        print()

        # Enviar mensaje de prueba
        response = client.chat.completions.create(
            model="kimi-k2.5",
            messages=[
                {"role": "system", "content": "Eres un asistente útil. Responde de forma breve."},
                {"role": "user", "content": "Di '¡Hola! Soy Kimi y estoy funcionando correctamente.' en español"}
            ],
            max_tokens=100,
            temperature=0.3
        )

        # Mostrar respuesta
        respuesta = response.choices[0].message.content
        tokens_usados = response.usage.total_tokens

        print("  ✅ CONEXIÓN EXITOSA")
        print(f"  📨 Respuesta: {respuesta}")
        print(f"  🔢 Tokens usados: {tokens_usados}")
        return True

    except Exception as e:
        print(f"  ❌ ERROR DE CONEXIÓN: {e}")
        return False


def test_kimi_nvidia(api_key=None):
    """
    Probar conexión con Kimi a través de NVIDIA NIM (gratuito)

    Args:
        api_key: Clave API de NVIDIA. Si es None, busca en variable de entorno NVIDIA_API_KEY
    """
    print()
    print("=" * 60)
    print("🟢 PROBANDO CONEXIÓN CON KIMI VÍA NVIDIA NIM")
    print("=" * 60)

    if api_key is None:
        api_key = os.environ.get("NVIDIA_API_KEY")

    if not api_key:
        print("  ⚠️  No se encontró API Key de NVIDIA.")
        print("     Obtén una gratuita en: https://build.nvidia.com/moonshotai/kimi-k2.5")
        return False

    try:
        from openai import OpenAI

        client = OpenAI(
            api_key=api_key,
            base_url="https://integrate.api.nvidia.com/v1"
        )

        print(f"  📝 API Key NVIDIA: {api_key[:8]}...{api_key[-4:]}")
        print("  🌐 Base URL: https://integrate.api.nvidia.com/v1")
        print()
        print("  ⏳ Enviando mensaje de prueba...")
        print()

        response = client.chat.completions.create(
            model="moonshotai/kimi-k2.5",
            messages=[
                {"role": "user", "content": "Di '¡Hola! Soy Kimi vía NVIDIA NIM.' en español"}
            ],
            max_tokens=100,
            temperature=0.3
        )

        respuesta = response.choices[0].message.content
        print("  ✅ CONEXIÓN EXITOSA CON NVIDIA NIM")
        print(f"  📨 Respuesta: {respuesta}")
        return True

    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        return False


def test_deepseek(api_key=None):
    """
    Probar conexión con la API de DeepSeek

    DeepSeek ofrece $5 en créditos gratuitos al registrarse.
    La API es compatible con el formato de OpenAI.

    Args:
        api_key: Clave API de DeepSeek. Si es None, busca en variable de entorno DEEPSEEK_API_KEY
    """
    print()
    print("=" * 60)
    print("🔷 PROBANDO CONEXIÓN CON DEEPSEEK")
    print("=" * 60)

    if api_key is None:
        api_key = os.environ.get("DEEPSEEK_API_KEY")

    if not api_key:
        print("  ⚠️  No se encontró API Key de DeepSeek.")
        print("     Para obtener una API Key:")
        print("     1. Ve a https://platform.deepseek.com")
        print("     2. Crea una cuenta (te dan $5 en créditos gratis)")
        print("     3. Ve a API Keys y crea una nueva key")
        print("     4. Exporta: export DEEPSEEK_API_KEY='tu-key'")
        print()
        print("     O pasa como argumento:")
        print("     python3 testKimiIA.py --deepseek-key TU_KEY")
        return False

    try:
        from openai import OpenAI

        modelDeep = "deepseek/deepseek-r1:free"

        # Configurar cliente para DeepSeek (compatible con OpenAI)
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )

        print(f"  📝 API Key DeepSeek: {api_key[:8]}...{api_key[-4:]}")
        print("  🌐 Base URL: https://api.deepseek.com/v1")
        print()
        print(f"  ⏳ Enviando mensaje de prueba a {modelDeep}")
        print()

        # Enviar mensaje de prueba
        response = client.chat.completions.create(
            model=modelDeep,  # También disponible: deepseek-reasoner
            messages=[
                {"role": "system", "content": "Eres un asistente útil. Responde de forma breve."},
                {"role": "user", "content": "Di '¡Hola! Soy DeepSeek y estoy funcionando correctamente.' en español"}
            ],
            max_tokens=100,
            temperature=0.3
        )

        # Mostrar respuesta
        respuesta = response.choices[0].message.content
        tokens_usados = response.usage.total_tokens

        print("  ✅ CONEXIÓN EXITOSA CON DEEPSEEK")
        print(f"  📨 Respuesta: {respuesta}")
        print(f"  🔢 Tokens usados: {tokens_usados}")
        return True

    except Exception as e:
        error_str = str(e)
        print(f"  ❌ ERROR DE CONEXIÓN: {error_str}")

        if "401" in error_str or "Unauthorized" in error_str:
            print()
            print("  💡 Error 401: API Key inválida o expirada.")
            print("     Verifica tu key en https://platform.deepseek.com")
        elif "429" in error_str:
            print()
            print("  💡 Error 429: Límite de tasa alcanzado.")
            print("     Espera un momento o verifica tus créditos.")
        elif "insufficient" in error_str.lower() or "balance" in error_str.lower():
            print()
            print("  💡 Saldo insuficiente.")
            print("     Recarga créditos en https://platform.deepseek.com")

        return False


def main():
    """Función principal"""
    print()
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "TEST DE CONEXIÓN IA - KIMI & DEEPSEEK" + " " * 9 + "║")
    print("╚" + "=" * 58 + "╝")
    print()

    # Verificar argumentos
    api_key = None
    nvidia_key = None
    deepseek_key = None

    for i, arg in enumerate(sys.argv):
        if arg == "--key" and i + 1 < len(sys.argv):
            api_key = sys.argv[i + 1]
        if arg == "--nvidia-key" and i + 1 < len(sys.argv):
            nvidia_key = sys.argv[i + 1]
        if arg == "--deepseek-key" and i + 1 < len(sys.argv):
            deepseek_key = sys.argv[i + 1]

    # Paso 1: Verificar imports
    imports_ok = test_imports()

    if not imports_ok:
        print()
        print("❌ Algunas librerías no están instaladas.")
        print("   Ejecuta: pip install openai numpy pandas matplotlib scipy")
        sys.exit(1)

    # Paso 2: Probar conexiones
    kimi_ok = test_kimi_conexion(api_key)
    nvidia_ok = test_kimi_nvidia(nvidia_key)
    deepseek_ok = test_deepseek(deepseek_key)

    # Resumen final
    print()
    print("=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    print(f"  {'✅' if imports_ok else '❌'} Librerías instaladas")
    print(f"  {'✅' if kimi_ok else '⚠️ '} Conexión Kimi API")
    print(f"  {'✅' if nvidia_ok else '⚠️ '} Conexión NVIDIA NIM")
    print(f"  {'✅' if deepseek_ok else '⚠️ '} Conexión DeepSeek")
    print()

    if not any([kimi_ok, nvidia_ok, deepseek_ok]):
        print("💡 NINGUNA CONEXIÓN FUNCIONÓ. Opciones para obtener API Keys:")
        print()
        print("   🤖 KIMI OFICIAL:")
        print("      https://platform.kimi.ai/console/api-keys")
        print("      export KIMI_API_KEY='tu-key'")
        print()
        print("   🟢 NVIDIA NIM (gratis):")
        print("      https://build.nvidia.com/moonshotai/kimi-k2.5")
        print("      export NVIDIA_API_KEY='tu-key'")
        print()
        print("   🔷 DEEPSEEK ($5 gratis al registrarte):")
        print("      https://platform.deepseek.com")
        print("      export DEEPSEEK_API_KEY='tu-key'")
        print()
        print("   Ejemplos de uso:")
        print("   python3 testKimiIA.py --key sk-xxx --nvidia-key nvapi-xxx --deepseek-key sk-xxx")
    else:
        print("🎉 ¡AL MENOS UNA CONEXIÓN FUNCIONA!")
        print("   Puedes empezar a usar IA en tu proyecto.")

    print()


if __name__ == "__main__":
    main()