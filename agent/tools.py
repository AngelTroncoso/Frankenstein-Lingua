"""
Herramientas del agente Frankenstein Lingua
"""
import json
import pandas as pd
from typing import Dict, List, Any
from pathlib import Path


def cargar_patrones() -> List[Dict[str, Any]]:
    """Carga la base de conocimiento de patrones de comunicación."""
    ruta = Path(__file__).parent.parent / "data" / "patrones.json"
    with open(ruta, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['patrones']


def buscar_patrones(especie_o_tipo: str, señal: str) -> Dict[str, Any]:
    """
    Busca patrones coincidentes en la base de conocimiento.
    
    Args:
        especie_o_tipo: Especie específica o tipo general (animal/planta/hongo)
        señal: Descripción de la señal observada
    
    Returns:
        Diccionario con patrones encontrados y metadatos
    """
    patrones = cargar_patrones()
    especie_o_tipo = especie_o_tipo.lower()
    señal = señal.lower()
    
    resultados = []
    
    # Búsqueda exacta por especie
    for patron in patrones:
        if patron['especie'].lower() == especie_o_tipo:
            # Coincidencia de palabras clave en la señal
            palabras_señal = set(señal.split())
            palabras_patron = set(patron['señal'].lower().split())
            coincidencias = palabras_señal & palabras_patron
            
            if coincidencias:
                score = len(coincidencias) / max(len(palabras_señal), len(palabras_patron))
                resultados.append({
                    **patron,
                    'score': score
                })
    
    # Si no hay resultados exactos, buscar por tipo
    if not resultados:
        for patron in patrones:
            if patron['tipo'].lower() == especie_o_tipo:
                palabras_señal = set(señal.split())
                palabras_patron = set(patron['señal'].lower().split())
                coincidencias = palabras_señal & palabras_patron
                
                if coincidencias or especie_o_tipo in ['animal', 'planta', 'hongo']:
                    score = len(coincidencias) / max(len(palabras_señal), 1) if coincidencias else 0.3
                    resultados.append({
                        **patron,
                        'score': score
                    })
    
    # Ordenar por score
    resultados.sort(key=lambda x: x['score'], reverse=True)
    
    return {
        'encontrados': len(resultados),
        'patrones': resultados[:3],  # Top 3 resultados
        'query': {
            'especie_o_tipo': especie_o_tipo,
            'señal': señal
        }
    }


def evaluar_sensores(csv_path: str) -> Dict[str, Any]:
    """
    Analiza datos de sensores de una planta desde un CSV.
    
    Args:
        csv_path: Ruta al archivo CSV con columnas: 
                  timestamp, humedad_suelo, luz_lux, temperatura_c
    
    Returns:
        Diccionario con estadísticas y anomalías detectadas
    """
    try:
        df = pd.read_csv(csv_path)
        
        # Validar columnas requeridas
        columnas_requeridas = ['humedad_suelo', 'luz_lux', 'temperatura_c']
        for col in columnas_requeridas:
            if col not in df.columns:
                return {
                    'error': f'Columna requerida no encontrada: {col}',
                    'columnas_disponibles': list(df.columns)
                }
        
        # Calcular estadísticas
        estadisticas = {
            'humedad_suelo': {
                'promedio': float(df['humedad_suelo'].mean()),
                'minimo': float(df['humedad_suelo'].min()),
                'maximo': float(df['humedad_suelo'].max()),
                'actual': float(df['humedad_suelo'].iloc[-1])
            },
            'luz_lux': {
                'promedio': float(df['luz_lux'].mean()),
                'minimo': float(df['luz_lux'].min()),
                'maximo': float(df['luz_lux'].max()),
                'actual': float(df['luz_lux'].iloc[-1])
            },
            'temperatura_c': {
                'promedio': float(df['temperatura_c'].mean()),
                'minimo': float(df['temperatura_c'].min()),
                'maximo': float(df['temperatura_c'].max()),
                'actual': float(df['temperatura_c'].iloc[-1])
            }
        }
        
        # Detectar anomalías
        anomalias = []
        
        # Humedad crítica
        if estadisticas['humedad_suelo']['actual'] < 40:
            anomalias.append({
                'tipo': 'humedad_critica',
                'severidad': 'alta',
                'mensaje': f"Humedad del suelo muy baja: {estadisticas['humedad_suelo']['actual']}%"
            })
        elif estadisticas['humedad_suelo']['actual'] < 50:
            anomalias.append({
                'tipo': 'humedad_baja',
                'severidad': 'media',
                'mensaje': f"Humedad del suelo baja: {estadisticas['humedad_suelo']['actual']}%"
            })
        
        # Luz insuficiente
        if estadisticas['luz_lux']['actual'] < 5000:
            anomalias.append({
                'tipo': 'luz_insuficiente',
                'severidad': 'media',
                'mensaje': f"Luz baja: {estadisticas['luz_lux']['actual']} lux"
            })
        
        # Temperatura extrema
        if estadisticas['temperatura_c']['actual'] < 15:
            anomalias.append({
                'tipo': 'temperatura_baja',
                'severidad': 'media',
                'mensaje': f"Temperatura baja: {estadisticas['temperatura_c']['actual']}°C"
            })
        elif estadisticas['temperatura_c']['actual'] > 30:
            anomalias.append({
                'tipo': 'temperatura_alta',
                'severidad': 'media',
                'mensaje': f"Temperatura alta: {estadisticas['temperatura_c']['actual']}°C"
            })
        
        # Tendencia de humedad
        if len(df) >= 3:
            ultimos_3 = df['humedad_suelo'].tail(3).tolist()
            if all(ultimos_3[i] > ultimos_3[i+1] for i in range(len(ultimos_3)-1)):
                anomalias.append({
                    'tipo': 'tendencia_seca',
                    'severidad': 'alta',
                    'mensaje': 'La humedad está descendiendo constantemente'
                })
        
        return {
            'registros_analizados': len(df),
            'periodo': {
                'inicio': str(df.iloc[0]['timestamp']) if 'timestamp' in df.columns else 'N/A',
                'fin': str(df.iloc[-1]['timestamp']) if 'timestamp' in df.columns else 'N/A'
            },
            'estadisticas': estadisticas,
            'anomalias': anomalias,
            'salud_general': 'critica' if any(a['severidad'] == 'alta' for a in anomalias) else 
                           'precaucion' if anomalias else 'buena'
        }
        
    except Exception as e:
        return {
            'error': f'Error al procesar CSV: {str(e)}'
        }


# Descriptor de herramientas para el agente
TOOLS_DESCRIPTION = [
    {
        'name': 'buscar_patrones',
        'description': 'Busca en la base de conocimiento patrones de comunicación de seres vivos. '
                      'Usa esto cuando necesites interpretar una señal de un animal, planta u hongo. '
                      'Proporciona la especie específica o el tipo general (animal/planta/hongo) y la descripción de la señal.',
        'parameters': {
            'especie_o_tipo': 'Especie específica (ej: "perro", "tomate") o tipo general (ej: "animal", "planta")',
            'señal': 'Descripción de la señal observada (ej: "ladrido agudo", "hojas enrolladas")'
        }
    },
    {
        'name': 'evaluar_sensores',
        'description': 'Analiza datos de sensores de una planta desde un archivo CSV. '
                      'El CSV debe tener columnas: timestamp, humedad_suelo, luz_lux, temperatura_c. '
                      'Devuelve estadísticas y detecta anomalías.',
        'parameters': {
            'csv_path': 'Ruta al archivo CSV con datos de sensores'
        }
    }
]
