# Changelog

Todos los cambios notables en este proyecto serán documentados aquí.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2024-11-16

### Agregado
- 10 nuevos patrones científicos a la base de conocimiento (25 patrones totales)
  - Delfín (clicks ultrasónicos)
  - Lobo (aullidos)
  - Hormiga (feromonas)
  - Venus atrapamoscas (trampa)
  - Eucalipto (compuestos volátiles)
  - Frijol (movimiento circadiano)
  - Penicillium (antibióticos)
  - Red micorrízica (wood wide web)
  - Luciérnaga (bioluminiscencia)
  - Murciélago (ecolocación)

- CSS mejorado con animaciones y efectos hover
- Archivo `config.py` para configuración centralizada
- Sistema de logging mejorado en el agente
- Este archivo CHANGELOG.md

### Mejorado
- Interfaz de usuario con gradientes y sombras
- Transiciones suaves en botones y cajas de traducción
- Manejo de errores con logging estructurado
- Colores dinámicos según nivel de confianza
- Documentación del sistema de umbrales

### Corregido
- Error en sidebar al cargar contador de patrones en Streamlit Cloud
- Manejo de excepciones al importar herramientas

## [1.0.0] - 2024-11-16

### Agregado
- Lanzamiento inicial del MVP
- Interfaz Streamlit con 4 pestañas funcionales
- Agente con LangChain y 2 herramientas
- Base de conocimiento con 15 patrones científicos
- Modo demo sin API keys
- Soporte para OpenAI y Mistral
- 11 tests unitarios (100% passing)
- Documentación completa (README, guías, demos)
- Modo Frankenstein para combinar múltiples fuentes
- Análisis de sensores CSV para plantas
- Historial de sesión con exportación a CSV
- Despliegue automatizado en Streamlit Community Cloud

### Características Principales
- Traducción de señales de animales, plantas y hongos
- Niveles de confianza (0-100%)
- Evidencia científica con fuentes
- Disclaimer ético obligatorio
- Sugerencias de acción práctica

---

## Tipos de Cambios

- **Agregado** para funcionalidades nuevas
- **Cambiado** para cambios en funcionalidades existentes
- **Obsoleto** para funcionalidades que serán removidas
- **Removido** para funcionalidades removidas
- **Corregido** para corrección de bugs
- **Seguridad** para vulnerabilidades corregidas
