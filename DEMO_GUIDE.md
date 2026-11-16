# 🎬 Guion de Demo - Frankenstein Lingua

**Duración:** 2 minutos  
**Objetivo:** Demostrar las tres funcionalidades principales del sistema

---

## 🎯 Preparación (antes de la demo)

1. Ejecutar `streamlit run app.py`
2. Verificar que la app cargó correctamente
3. Tener abierto el archivo `data/sensores_ejemplo.csv` en el explorador de archivos
4. Cerrar pestañas innecesarias del navegador para enfocarse en la demo

---

## 📋 Script de Demo

### Introducción (10 segundos)

> "Hola, soy [tu nombre] y les voy a mostrar **Frankenstein Lingua**, un agente de IA que traduce señales de comunicación de animales, plantas y hongos a lenguaje humano. Es un proyecto educativo que combina ciencia real con IA. Vamos a ver tres ejemplos rápidos."

---

### Ejemplo 1: Animal - Perro (30 segundos)

**Acción:**
1. Click en pestaña **"🔬 Traducción Simple"**
2. En el área de texto, escribir o pegar:
   ```
   Mi perro está ladrando de forma aguda y repetida mientras mira hacia la puerta y mueve la cola
   ```
3. Click en **"🌍 Traducir"**

**Narración mientras procesa:**
> "En el primer ejemplo, describo el comportamiento de mi perro. El sistema busca en su base de conocimiento patrones de comunicación canina..."

**Al mostrar resultado:**
> "Aquí vemos la traducción: dice que el perro busca atención o alerta sobre algo. El nivel de confianza es del 85%, y abajo podemos ver la evidencia científica que usó, incluyendo estudios de etología. Y aquí abajo, muy importante, está el **disclaimer** recordando que esto es una interpretación educativa, no una traducción literal."

**Puntos clave a mencionar:**
- ✅ Confianza del 85%
- ✅ Evidencia científica (Coren, 2004)
- ✅ Disclaimer visible

---

### Ejemplo 2: Planta con Sensores (45 segundos)

**Acción:**
1. Mismo tab **"🔬 Traducción Simple"**
2. Escribir:
   ```
   Mi planta de tomate tiene las hojas enrolladas hacia arriba
   ```
3. ✅ Activar checkbox **"📊 Incluir datos de sensores"**
4. Click en **"Browse files"** y seleccionar `data/sensores_ejemplo.csv`
5. Click en **"🌍 Traducir"**

**Narración mientras procesa:**
> "Ahora una planta. Describo que las hojas están enrolladas, y además subo un CSV con datos reales de sensores: humedad del suelo, luz y temperatura de las últimas horas. El agente va a analizar ambas fuentes..."

**Al mostrar resultado:**
> "Fascinante. La traducción dice que la planta necesita agua urgentemente. Miren el análisis: la humedad del suelo cayó del 65% al 35%, y el sistema detectó una **tendencia descendente crítica**. La acción recomendada es riego inmediato. Si expandimos la evidencia científica, vemos referencias sobre estrés hídrico en plantas."

**Puntos clave a mencionar:**
- ✅ Integración de texto + datos CSV
- ✅ Detección de anomalías (humedad crítica)
- ✅ Acción práctica (regar)

---

### Ejemplo 3: Modo Frankenstein (45 segundos)

**Acción:**
1. Click en pestaña **"⚡ Modo Frankenstein"**
2. Verificar que dice **"¿Cuántas fuentes quieres combinar?"** = 2
3. En **Observación 1** escribir:
   ```
   Una abeja está realizando una danza en forma de 8
   ```
4. En **Observación 2** escribir:
   ```
   Un cactus presenta arrugas en su superficie
   ```
5. Click en **"⚡ ¡Coser Traducciones!"**

**Narración mientras procesa:**
> "Y ahora la función más divertida: el **Modo Frankenstein**. Voy a combinar dos seres vivos completamente diferentes: una abeja danzando y un cactus arrugado. El sistema va a 'coser' estas señales como el Dr. Frankenstein cosía partes del cuerpo..."

**Al mostrar resultado:**
> "Increíble. El sistema generó una **traducción integrada** que conecta ambas señales: uno busca comunicar localización de recursos, el otro pide agua. La traducción dice algo como 'somos diferentes pero conectados en el mismo ecosistema'. Y si expandimos aquí abajo, puedo ver las traducciones individuales de cada uno."

**Puntos clave a mencionar:**
- ✅ Combinación creativa de 2+ especies
- ✅ Traducción integrada única
- ✅ Ver traducciones individuales

---

### Cierre y Historial (10 segundos)

**Acción:**
1. Click en pestaña **"📜 Historial"**
2. Mostrar la tabla con las 3 traducciones

**Narración:**
> "Todas las traducciones se guardan en el historial de la sesión y puedo exportarlas a CSV para análisis posterior. Este es el MVP completo: traducción simple, análisis de sensores y modo Frankenstein."

---

## 🎯 Mensajes Clave para Enfatizar

1. **Científicamente fundamentado:** Cada traducción usa patrones de etología, botánica y micología reales.
2. **Transparente:** Nivel de confianza visible + disclaimer obligatorio.
3. **Práctico:** No solo traduce, sugiere acciones concretas.
4. **Creativo:** El modo Frankenstein muestra posibilidades únicas de combinar conocimientos.
5. **Ético:** Aclara que NO es traducción literal, es interpretación educativa.

---

## 🔧 Troubleshooting Durante la Demo

### Si el modo es "Demo" (sin API key):
> "El sistema está en modo demo con respuestas simuladas. En producción, usaría GPT-4 u otro modelo para traducciones más sofisticadas basadas en el contexto completo."

### Si tarda mucho en procesar:
> "El agente está consultando el LLM y procesando múltiples herramientas en paralelo... [narrar qué está haciendo mientras espera]"

### Si hay un error:
> "Parece que hubo un problema técnico. En un caso real, el sistema tiene manejo de errores robusto. Déjenme mostrarles el siguiente ejemplo..."

---

## 📊 Variaciones Opcionales

### Demo Extendida (+30 segundos)
Agregar un cuarto ejemplo usando la pestaña **"🎬 Guion Demo"** con los botones de ejemplo predefinidos.

### Demo Técnica (+1 minuto)
- Mostrar `data/patrones.json` en editor
- Explicar arquitectura del agente
- Mostrar código de una herramienta (`agent/tools.py`)

### Demo para No-Técnicos
- Enfocarse más en los resultados que en la tecnología
- Usar analogías ("como Google Translate pero para animales")
- Mostrar más énfasis en el disclaimer ético

---

## ✅ Checklist Pre-Demo

- [ ] App ejecutándose en `localhost:8501`
- [ ] Navegador con pestañas limpias
- [ ] Archivo `sensores_ejemplo.csv` accesible
- [ ] Script de narración revisado
- [ ] Timer preparado (para practicar 2 minutos)
- [ ] Backup: capturas de pantalla de resultados esperados

---

## 🎓 Preguntas Frecuentes Post-Demo

**P: ¿Realmente puede entender lo que piensa un animal?**  
R: No. El sistema interpreta patrones de comportamiento basándose en ciencia, pero la experiencia subjetiva de otros seres vivos es inaccesible. Por eso incluimos el disclaimer en cada respuesta.

**P: ¿Funciona con cualquier animal/planta?**  
R: Actualmente tiene 15 patrones curados. Puede generalizar a especies similares, pero la precisión depende de qué tan cerca esté de los patrones conocidos. Es un MVP escalable.

**P: ¿Se puede usar en un veterinario/granja?**  
R: Este MVP es educativo. Para uso profesional, necesitaría validación científica rigurosa, más datos, y certificaciones apropiadas. Pero la arquitectura es sólida para extenderlo en esa dirección.

**P: ¿Por qué se llama Frankenstein?**  
R: Porque "cose" fragmentos de conocimiento de diferentes especies, como el Dr. Frankenstein cosía partes de cuerpos. Es una metáfora sobre crear algo nuevo a partir de piezas existentes.

---

**¡Buena suerte con tu demo!** ⚡🧬
