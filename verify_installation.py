#!/usr/bin/env python
"""
Script de verificación de instalación para Frankenstein Lingua
"""

print("🔬 Verificando instalación de Frankenstein Lingua...\n")

# Test 1: Importar dependencias
print("1️⃣ Verificando dependencias...")
try:
    import streamlit
    import langchain
    import pandas
    import pytest
    print("   ✅ Todas las dependencias importadas correctamente\n")
except ImportError as e:
    print(f"   ❌ Error importando dependencias: {e}\n")
    exit(1)

# Test 2: Cargar base de conocimiento
print("2️⃣ Verificando base de conocimiento...")
try:
    from agent.tools import cargar_patrones
    patrones = cargar_patrones()
    print(f"   ✅ {len(patrones)} patrones cargados correctamente\n")
except Exception as e:
    print(f"   ❌ Error cargando patrones: {e}\n")
    exit(1)

# Test 3: Inicializar agente
print("3️⃣ Verificando agente en modo demo...")
try:
    from agent.frankenstein_agent import FrankensteinAgent
    agente = FrankensteinAgent(llm_provider="demo")
    print(f"   ✅ Agente inicializado correctamente\n")
except Exception as e:
    print(f"   ❌ Error inicializando agente: {e}\n")
    exit(1)

# Test 4: Traducción simple
print("4️⃣ Probando traducción simple...")
try:
    resultado = agente.traducir("Un perro ladrando")
    assert 'tipo_ser' in resultado
    assert 'traduccion' in resultado
    assert 'confianza' in resultado
    assert 'disclaimer' in resultado
    print(f"   ✅ Tipo detectado: {resultado['tipo_ser']}")
    print(f"   ✅ Confianza: {resultado['confianza']}%")
    print(f"   ✅ Disclaimer presente: {len(resultado['disclaimer']) > 50}\n")
except Exception as e:
    print(f"   ❌ Error en traducción: {e}\n")
    exit(1)

# Test 5: Modo Frankenstein
print("5️⃣ Probando modo Frankenstein...")
try:
    resultado = agente.traducir_frankenstein(
        ["Un perro ladrando", "Una planta con hojas caídas"]
    )
    assert 'tipo_ser' in resultado
    assert 'frankenstein' in resultado['tipo_ser'].lower() or 'híbrido' in resultado['tipo_ser']
    print(f"   ✅ Tipo combinado: {resultado['tipo_ser']}")
    print(f"   ✅ Traducciones individuales: {len(resultado['traducciones_individuales'])}\n")
except Exception as e:
    print(f"   ❌ Error en modo Frankenstein: {e}\n")
    exit(1)

# Resumen final
print("=" * 60)
print("✅ ¡INSTALACIÓN VERIFICADA CON ÉXITO!")
print("=" * 60)
print("\n📋 Siguiente paso:")
print("   Ejecuta: streamlit run app.py")
print("\n🎬 Para probar rápidamente:")
print("   Ve a la pestaña '🎬 Guion Demo' y presiona los botones\n")
