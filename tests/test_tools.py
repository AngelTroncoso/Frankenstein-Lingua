"""
Tests para las herramientas del agente
"""
import pytest
from agent.tools import buscar_patrones, evaluar_sensores, cargar_patrones
import tempfile
import os


def test_cargar_patrones():
    """Verifica que se carguen correctamente los patrones de la base de conocimiento."""
    patrones = cargar_patrones()
    assert len(patrones) >= 15, "Debe haber al menos 15 patrones"
    assert all('id' in p for p in patrones), "Todos los patrones deben tener ID"
    assert all('tipo' in p for p in patrones), "Todos los patrones deben tener tipo"
    assert all('especie' in p for p in patrones), "Todos los patrones deben tener especie"


def test_buscar_patrones_por_especie():
    """Verifica la búsqueda de patrones por especie específica."""
    resultado = buscar_patrones("perro", "ladrido agudo")
    
    assert resultado['encontrados'] > 0, "Debe encontrar patrones de perro"
    assert 'patrones' in resultado
    assert len(resultado['patrones']) > 0
    assert resultado['patrones'][0]['especie'] == 'perro'


def test_buscar_patrones_por_tipo():
    """Verifica la búsqueda de patrones por tipo general."""
    resultado = buscar_patrones("animal", "sonido")
    
    assert resultado['encontrados'] > 0, "Debe encontrar patrones de animales"
    assert all(p['tipo'] == 'animal' for p in resultado['patrones'])


def test_evaluar_sensores_csv_valido():
    """Verifica el análisis de un CSV válido con datos de sensores."""
    # Crear CSV temporal
    csv_content = """timestamp,humedad_suelo,luz_lux,temperatura_c
2024-01-15 08:00,65,8000,22
2024-01-15 09:00,63,12000,23
2024-01-15 10:00,35,5000,24"""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write(csv_content)
        temp_path = f.name
    
    try:
        resultado = evaluar_sensores(temp_path)
        
        assert 'estadisticas' in resultado
        assert 'anomalias' in resultado
        assert resultado['registros_analizados'] == 3
        assert len(resultado['anomalias']) > 0, "Debe detectar anomalías con humedad baja"
        
    finally:
        os.unlink(temp_path)


def test_evaluar_sensores_csv_invalido():
    """Verifica el manejo de errores con CSV inválido."""
    # CSV sin columnas requeridas
    csv_content = """fecha,valor
2024-01-15,100"""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write(csv_content)
        temp_path = f.name
    
    try:
        resultado = evaluar_sensores(temp_path)
        assert 'error' in resultado
    finally:
        os.unlink(temp_path)


def test_buscar_patrones_sin_coincidencias():
    """Verifica el comportamiento cuando no hay coincidencias."""
    resultado = buscar_patrones("especie_inexistente_xyz", "señal_inexistente")
    
    assert 'encontrados' in resultado
    assert resultado['encontrados'] >= 0
    assert 'patrones' in resultado


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
