"""
Configuración centralizada para Frankenstein Lingua
"""

# Configuración de la aplicación
APP_CONFIG = {
    "title": "Frankenstein Lingua",
    "icon": "⚡",
    "subtitle": "Agente de traducción universal entre especies",
    "version": "1.0.1",
    "author": "Equipo Frankenstein Lingua"
}

# Configuración de modelos LLM
LLM_CONFIG = {
    "openai": {
        "default_model": "gpt-4o-mini",
        "temperature": 0.7,
        "max_tokens": 1000
    },
    "mistral": {
        "default_model": "mistral-small-latest",
        "temperature": 0.7,
        "max_tokens": 1000
    }
}

# Umbrales de confianza para clasificación
CONFIDENCE_THRESHOLDS = {
    "muy_alta": 85,  # >= 85%
    "alta": 70,      # 70-84%
    "media": 50,     # 50-69%
    "baja": 30,      # 30-49%
    "muy_baja": 0    # < 30%
}

# Configuración de colores por confianza
CONFIDENCE_COLORS = {
    "muy_alta": "#4CAF50",    # Verde
    "alta": "#8BC34A",        # Verde claro
    "media": "#FFC107",       # Amarillo
    "baja": "#FF9800",        # Naranja
    "muy_baja": "#F44336"     # Rojo
}

# Mensajes del sistema
SYSTEM_MESSAGES = {
    "demo_warning": "🧪 **Modo Demo Activo** - Las traducciones son simuladas. Configura una API key en `.env` para usar IA real.",
    "loading": "🧬 Cosiendo fragmentos de conocimiento...",
    "success": "✅ Traducción completada",
    "error": "❌ Error en la traducción",
}

# Configuración de análisis de sensores
SENSOR_THRESHOLDS = {
    "humedad": {
        "critica": 40,
        "baja": 50,
        "optima_min": 60,
        "optima_max": 80,
        "alta": 90
    },
    "luz": {
        "muy_baja": 5000,
        "baja": 10000,
        "optima_min": 15000,
        "optima_max": 25000,
        "alta": 30000
    },
    "temperatura": {
        "muy_baja": 15,
        "baja": 18,
        "optima_min": 20,
        "optima_max": 26,
        "alta": 30
    }
}

# Límites de la aplicación
APP_LIMITS = {
    "max_frankenstein_sources": 4,
    "max_csv_size_mb": 10,
    "max_observation_length": 2000,
    "session_timeout_minutes": 60
}

def get_confidence_level(confidence: int) -> str:
    """Devuelve el nivel de confianza basado en el valor numérico."""
    if confidence >= CONFIDENCE_THRESHOLDS["muy_alta"]:
        return "muy_alta"
    elif confidence >= CONFIDENCE_THRESHOLDS["alta"]:
        return "alta"
    elif confidence >= CONFIDENCE_THRESHOLDS["media"]:
        return "media"
    elif confidence >= CONFIDENCE_THRESHOLDS["baja"]:
        return "baja"
    else:
        return "muy_baja"

def get_confidence_color(confidence: int) -> str:
    """Devuelve el color asociado al nivel de confianza."""
    level = get_confidence_level(confidence)
    return CONFIDENCE_COLORS[level]
