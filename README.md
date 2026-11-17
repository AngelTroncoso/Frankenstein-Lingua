# ⚡ Frankenstein Lingua

**Agente de lenguaje universal entre especies**

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-11%2F11%20passing-brightgreen.svg)](tests/)
[![Patrones](https://img.shields.io/badge/patrones-25-blue.svg)](data/patrones.json)
[![Deployment](https://img.shields.io/badge/deployment-Streamlit%20Cloud-ff4b4b.svg)](https://share.streamlit.io)

Un sistema experimental que interpreta señales de comunicación de animales, plantas y hongos, traduciéndolas a lenguaje humano comprensible mediante IA y conocimiento científico curado.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 🎯 Concepto

Este proyecto es un **prototipo educativo y creativo** que "cose" fragmentos de conocimiento de diferentes especies (como el Dr. Frankenstein) para generar interpretaciones de sus formas de comunicación. Cada traducción incluye:

- ✅ Nivel de confianza (0-100%)
- ✅ Evidencia científica utilizada
- ✅ Disclaimer visible sobre limitaciones
- ✅ Sugerencias de acción práctica

**⚠️ IMPORTANTE:** Este sistema NO afirma traducir literalmente a los animales. Es una herramienta educativa que combina etología, botánica, micología e IA para generar interpretaciones informadas pero creativas.

---

## 🚀 Características

### Funcionalidades Principales

1. **🔬 Traducción Simple**
   - Entrada de texto libre describiendo observaciones
   - Soporte opcional para CSV con lecturas de sensores (plantas)
   - Traducción con confianza, evidencia y disclaimer

2. **⚡ Modo Frankenstein**
   - Combina señales de 2-4 seres vivos diferentes
   - Genera una traducción integrada única
   - Muestra traducciones individuales y combinadas

3. **📊 Análisis de Sensores**
   - Lectura de CSV con datos de humedad, luz y temperatura
   - Detección automática de anomalías
   - Estadísticas y tendencias

4. **📜 Historial de Sesión**
   - Registro de todas las traducciones
   - Exportación a CSV para análisis posterior

5. **🎬 Guion de Demo**
   - 3 ejemplos predefinidos listos para probar
   - Demo completa en menos de 2 minutos

### Base de Conocimiento

- 📚 **15+ patrones curados** de animales, plantas y hongos
- 🔬 Cada patrón incluye fuente científica
- 🌍 Cobertura: mamíferos, aves, insectos, plantas ornamentales/comestibles, hongos

---

## 🏗️ Arquitectura

```
frankenstein-lingua/
├── app.py                    # Interfaz Streamlit (UI principal)
├── agent/
│   ├── __init__.py
│   ├── frankenstein_agent.py # Orquestador del agente con LangGraph
│   └── tools.py              # Herramientas: buscar_patrones, evaluar_sensores
├── data/
│   ├── patrones.json         # Base de conocimiento (15 patrones)
│   └── sensores_ejemplo.csv  # Datos de ejemplo para plantas
├── tests/
│   ├── __init__.py
│   ├── test_tools.py         # Tests de herramientas
│   └── test_agent.py         # Tests del agente
├── requirements.txt
├── .env.example
└── README.md
```

### Flujo del Sistema

```
Usuario → Streamlit UI → FrankensteinAgent
                              ↓
                    [Detecta tipo de ser vivo]
                              ↓
                    ┌─────────┴─────────┐
                    ↓                   ↓
            buscar_patrones()    evaluar_sensores()
                    ↓                   ↓
            Base JSON (15 patrones)  CSV sensors
                    ↓                   ↓
                    └─────────┬─────────┘
                              ↓
                    LLM (OpenAI/Mistral) o Demo
                              ↓
              Traducción + Confianza + Disclaimer
```

---

## ⚙️ Instalación Local

### Requisitos Previos

- Python 3.11 o superior
- pip (gestor de paquetes)

### Paso 1: Clonar o descargar el proyecto

```bash
git clone <tu-repositorio>
cd frankenstein-lingua
```

### Paso 2: Crear entorno virtual (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tu editor favorito
# Configurar LLM_PROVIDER y agregar tu API key
```

**Opciones de configuración:**

```env
# Opción 1: Usar OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=tu-clave-aqui
OPENAI_MODEL=gpt-4o-mini

# Opción 2: Usar Mistral
LLM_PROVIDER=mistral
MISTRAL_API_KEY=tu-clave-aqui
MISTRAL_MODEL=mistral-small-latest

# Opción 3: Modo Demo (sin API key)
# No configurar nada, funciona con respuestas simuladas
```

### Paso 5: Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

---

## 🧪 Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar con verbosidad
pytest -v

# Ejecutar tests específicos
pytest tests/test_tools.py
pytest tests/test_agent.py
```

**Tests incluidos:**
- ✅ Carga de base de conocimiento
- ✅ Búsqueda de patrones por especie y tipo
- ✅ Análisis de CSV de sensores
- ✅ Inicialización del agente en modo demo
- ✅ Traducciones simples y Frankenstein
- ✅ Validación de disclaimer y confianza

---

## 🌐 Despliegue en Streamlit Community Cloud

### Paso 1: Preparar el repositorio

1. Sube tu código a GitHub (repositorio público o privado)
2. Asegúrate de incluir:
   - `app.py`
   - `requirements.txt`
   - Carpetas `agent/` y `data/`

### Paso 2: Crear cuenta en Streamlit

1. Visita [share.streamlit.io](https://share.streamlit.io)
2. Inicia sesión con GitHub

### Paso 3: Desplegar la app

1. Click en **"New app"**
2. Selecciona tu repositorio: `tu-usuario/frankenstein-lingua`
3. Branch: `main` (o la que uses)
4. Main file path: `app.py`
5. Click en **"Deploy"**

### Paso 4: Configurar Secrets (API keys)

1. En tu app desplegada, ve a **Settings → Secrets**
2. Agrega tus credenciales en formato TOML:

```toml
LLM_PROVIDER = "openai"
OPENAI_API_KEY = "sk-tu-clave-aqui"
OPENAI_MODEL = "gpt-4o-mini"
```

3. Click en **"Save"**

### Paso 5: Verificar despliegue

- La app se reiniciará automáticamente
- Accede a través de la URL proporcionada: `https://tu-app.streamlit.app`
- Verifica que el modo LLM esté activo (no demo)

**⏱️ Tiempo estimado de despliegue:** 5-10 minutos

---

## 🎬 Guion de Demo (2 minutos)

### Ejemplo 1: Animal (30 segundos)
```
Pestaña: Traducción Simple
Entrada: "Mi perro está ladrando de forma aguda y repetida mientras mira hacia la puerta"
Resultado: Traducción + confianza ~85% + evidencia etológica
```

### Ejemplo 2: Planta con sensores (45 segundos)
```
Pestaña: Traducción Simple
✅ Activar "Incluir datos de sensores"
Entrada: "Mi planta de tomate tiene las hojas enrolladas hacia arriba"
CSV: data/sensores_ejemplo.csv
Resultado: Traducción + análisis de humedad crítica + recomendación de riego
```

### Ejemplo 3: Modo Frankenstein (45 segundos)
```
Pestaña: Modo Frankenstein
Fuente 1: "Una abeja realizando una danza en forma de 8"
Fuente 2: "Un cactus con arrugas en su superficie"
Resultado: Traducción integrada única + ver traducciones individuales
```

---

## 📊 Decisiones Técnicas

### 1. Arquitectura del Agente

**Decisión:** Usar LangChain con tool calling directo en lugar de LangGraph completo.

**Razón:** Para un MVP, el tool calling directo es más simple y suficiente. Las herramientas son determinísticas (búsqueda en JSON y análisis de CSV), no requieren flujos complejos con estados.

**Alternativa considerada:** LangGraph con nodos y edges, descartada por complejidad excesiva para este alcance.

### 2. Modo Demo sin API key

**Decisión:** Implementar respuestas simuladas cuando no hay API key configurada.

**Razón:** Permite demostrar el flujo completo sin requerir credenciales. Esencial para evaluadores que quieran probar sin configurar cuentas.

**Implementación:** `FrankensteinAgent` detecta `provider="demo"` y genera respuestas template manteniendo la estructura de datos.

### 3. Base de conocimiento en JSON estático

**Decisión:** Usar `data/patrones.json` en lugar de base de datos.

**Razón:** 
- MVP con 15 patrones no justifica BD
- JSON es versionable con git
- Cero dependencias de infraestructura
- Fácil de auditar y curar

**Escalabilidad futura:** Migrar a SQLite o PostgreSQL cuando >100 patrones.

### 4. Soporte dual OpenAI + Mistral

**Decisión:** Implementar ambos proveedores con configuración por `.env`.

**Razón:**
- Mistral es más económico para pruebas
- OpenAI (GPT-4o-mini) ofrece mejor calidad
- Flexibilidad para el usuario según presupuesto

### 5. Disclaimer obligatorio

**Decisión:** Incluir disclaimer en cada respuesta, no como popup descartable.

**Razón:** 
- Transparencia ética sobre limitaciones
- Evita malentendidos sobre capacidades reales
- Requisito explícito del brief del proyecto

---

## 🚧 Limitaciones y Trabajo Futuro

### Limitaciones Actuales

1. **Científicas:**
   - No representa traducción literal (imposible científicamente)
   - Base de conocimiento limitada a 15 patrones
   - Confianza calculada heurísticamente, no validada empíricamente

2. **Técnicas:**
   - Sin persistencia de datos (historial se pierde al cerrar sesión)
   - Análisis de sensores limitado a CSV con formato específico
   - Sin soporte para audio/video real (solo descripciones textuales)

3. **Funcionales:**
   - Modo Frankenstein limitado a 4 fuentes
   - Sin API REST para integraciones
   - UI solo en español

### Trabajo Futuro

- [ ] Expandir base de conocimiento a 50+ patrones
- [ ] Integración con sensores IoT en tiempo real
- [ ] Análisis de audio con ML (espectrogramas de cantos)
- [ ] Sistema de votación comunitaria para calidad de traducciones
- [ ] API REST para desarrolladores
- [ ] Soporte multiidioma (inglés, francés)
- [ ] Dashboard de analítica para biólogos

---

## 🤝 Contribuciones

Este es un proyecto educativo. Contribuciones bienvenidas en:

- 🔬 Nuevos patrones científicamente respaldados
- 🐛 Corrección de bugs
- 📚 Mejoras en documentación
- 🎨 Mejoras en UI/UX

---

## 📄 Licencia

MIT License - Ver archivo LICENSE para detalles.

---

## ⚠️ Consideraciones Éticas

### Transparencia

Este sistema es **experimental y educativo**. No reemplaza:
- Consultas veterinarias para animales
- Asesoría agronómica para plantas
- Investigación científica formal

### Limitaciones Filosóficas

La experiencia subjetiva de otros seres vivos (qualia) permanece fundamentalmente inaccesible. Nuestras "traducciones" son **interpretaciones humanas** basadas en patrones de comportamiento observables, no acceso directo a sus estados mentales.

### Uso Responsable

- ✅ Educación sobre comunicación interespecífica
- ✅ Divulgación científica accesible
- ✅ Prototipado de interfaces humano-naturaleza
- ❌ NO para diagnósticos médicos/veterinarios
- ❌ NO como evidencia en investigación formal sin validación

---

## 📞 Contacto y Soporte

**Desarrollado por:** Equipo Frankenstein Lingua  
**Versión:** 1.0.0 MVP  
**Fecha:** 2024  

Para preguntas, bugs o sugerencias, abre un issue en GitHub.

---

## 🙏 Agradecimientos

Base de conocimiento curada a partir de:
- Von Frisch (1967) - Comunicación en abejas
- Coren (2004) - Etología canina
- Bradshaw (2013) - Comportamiento felino
- Taiz & Zeiger (2010) - Fisiología vegetal
- Stamets (2000) - Cultivo de hongos

Y muchas otras fuentes referenciadas en `data/patrones.json`.

---

**¡Que tu viaje traduciendo el lenguaje de la naturaleza sea tan fascinante como el del Dr. Frankenstein cosiendo vida!** ⚡🧬🌍
