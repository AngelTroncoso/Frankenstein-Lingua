"""
Tests para el agente Frankenstein
"""
import pytest
from agent.frankenstein_agent import FrankensteinAgent


def test_agent_inicializacion_demo():
    """Verifica que el agente se inicialice correctamente en modo demo."""
    agente = FrankensteinAgent(llm_provider="demo")
    assert agente.demo_mode == True
    assert agente.provider == "demo"


def test_traducir_simple_demo():
    """Verifica traducción simple en modo demo."""
    agente = FrankensteinAgent(llm_provider="demo")
    resultado = agente.traducir("Un perro ladrando")
    
    assert 'tipo_ser' in resultado
    assert 'traduccion' in resultado
    assert 'confianza' in resultado
    assert 'evidencia' in resultado
    assert 'disclaimer' in resultado
    assert resultado['modo'] == 'demo'


def test_traducir_frankenstein_demo():
    """Verifica traducción Frankenstein en modo demo."""
    agente = FrankensteinAgent(llm_provider="demo")
    observaciones = [
        "Un perro ladrando",
        "Una planta con hojas caídas"
    ]
    resultado = agente.traducir_frankenstein(observaciones)
    
    assert 'tipo_ser' in resultado
    assert 'frankenstein' in resultado['tipo_ser'].lower() or 'híbrido' in resultado['tipo_ser']
    assert 'traduccion' in resultado
    assert 'traducciones_individuales' in resultado
    assert len(resultado['traducciones_individuales']) == 2


def test_disclaimer_presente():
    """Verifica que todas las traducciones incluyan disclaimer."""
    agente = FrankensteinAgent(llm_provider="demo")
    resultado = agente.traducir("Un gato ronroneando")
    
    assert 'disclaimer' in resultado
    assert len(resultado['disclaimer']) > 50
    assert 'educativo' in resultado['disclaimer'].lower() or 'demostración' in resultado['disclaimer'].lower()


def test_confianza_rango_valido():
    """Verifica que el nivel de confianza esté en rango válido."""
    agente = FrankensteinAgent(llm_provider="demo")
    resultado = agente.traducir("Un elefante emitiendo infrasonidos")
    
    assert 'confianza' in resultado
    assert 0 <= resultado['confianza'] <= 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
