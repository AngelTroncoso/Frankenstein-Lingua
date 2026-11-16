# 🚀 Pasos Exactos para Desplegar Frankenstein Lingua

Este documento contiene los pasos precisos para levantar la aplicación localmente y desplegarla en Streamlit Community Cloud.

---

## ✅ Verificación Previa - Lo que YA está hecho

- [x] Código completo implementado
- [x] Base de conocimiento con 15 patrones curados
- [x] 11 tests ejecutados exitosamente
- [x] Modo demo funcional sin API key
- [x] Soporte para OpenAI y Mistral
- [x] Documentación completa

---

## 📍 OPCIÓN 1: Ejecución Local (5 minutos)

### Paso 1: Verificar Python
```bash
python --version
# Debe ser Python 3.11 o superior
```

### Paso 2: Clonar/Navegar al proyecto
```bash
cd c:\Users\angel\OneDrive\Escritorio\KIROWEN
```

### Paso 3: Crear entorno virtual
```bash
python -m venv venv

# Activar (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# O activar (Windows CMD)
venv\Scripts\activate.bat
```

### Paso 4: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 5: (Opcional) Configurar API key
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env en tu editor favorito
# Descomentar y configurar:
# LLM_PROVIDER=openai
# OPENAI_API_KEY=tu-clave-aqui
```

**Nota:** Si NO configuras API key, funciona en modo demo con respuestas simuladas.

### Paso 6: Ejecutar la aplicación
```bash
streamlit run app.py
```

La app se abrirá automáticamente en `http://localhost:8501`

### Paso 7: Verificar funcionamiento
1. Ve a la pestaña "🎬 Guion Demo"
2. Presiona "Probar Ejemplo 1"
3. Deberías ver una traducción simulada (o real si configuraste API key)

---

## 🌐 OPCIÓN 2: Despliegue en Streamlit Cloud (10 minutos)

### Requisitos Previos
- Cuenta de GitHub (gratuita)
- Cuenta de Streamlit (gratuita, se crea con GitHub)

### Paso 1: Subir código a GitHub

#### 1.1 Inicializar repositorio local
```bash
cd c:\Users\angel\OneDrive\Escritorio\KIROWEN
git init
git add .
git commit -m "Initial commit - Frankenstein Lingua MVP"
```

#### 1.2 Crear repositorio en GitHub
1. Ve a https://github.com/new
2. Nombre: `frankenstein-lingua`
3. Visibilidad: Público o Privado (ambos funcionan)
4. **NO inicialices con README/license** (ya lo tienes local)
5. Click "Create repository"

#### 1.3 Conectar y subir
```bash
git remote add origin https://github.com/TU-USUARIO/frankenstein-lingua.git
git branch -M main
git push -u origin main
```

### Paso 2: Desplegar en Streamlit Cloud

#### 2.1 Ir a Streamlit Cloud
1. Abre https://share.streamlit.io
2. Click "Sign in with GitHub"
3. Autoriza Streamlit

#### 2.2 Crear nueva app
1. Click "New app" (botón azul)
2. **Repository:** Selecciona `TU-USUARIO/frankenstein-lingua`
3. **Branch:** `main`
4. **Main file path:** `app.py`
5. **App URL (opcional):** `frankenstein-lingua` (o el nombre que prefieras)

#### 2.3 (Opcional) Configurar Secrets para API
Si quieres usar IA real en producción:

1. Antes de hacer click en "Deploy", expande **"Advanced settings"**
2. En la sección **"Secrets"**, pega esto:

```toml
LLM_PROVIDER = "openai"
OPENAI_API_KEY = "sk-proj-tu-clave-real-aqui"
OPENAI_MODEL = "gpt-4o-mini"
```

O para Mistral:
```toml
LLM_PROVIDER = "mistral"
MISTRAL_API_KEY = "tu-clave-mistral-aqui"
MISTRAL_MODEL = "mistral-small-latest"
```

3. Click "Save"

#### 2.4 Desplegar
1. Click **"Deploy"**
2. Espera 2-5 minutos mientras se construye
3. La URL final será algo como: `https://frankenstein-lingua.streamlit.app`

### Paso 3: Verificar despliegue
1. Abre la URL de tu app
2. Verifica el mensaje en la parte superior:
   - **"🧪 Modo Demo Activo"** = Sin secrets configurados (OK para demo)
   - **"✅ Conectado a OPENAI/MISTRAL"** = Con API configurada
3. Prueba los ejemplos en "🎬 Guion Demo"

---

## 🔧 Troubleshooting

### Problema: "Module not found" al ejecutar local
**Solución:**
```bash
pip install --upgrade -r requirements.txt
```

### Problema: Tests fallan
**Solución:**
```bash
pytest tests/ -v
# Todos deberían pasar. Si no, verifica que instalaste las dependencias.
```

### Problema: En Streamlit Cloud dice "error loading app"
**Solución:**
1. Ve a Manage app → Logs
2. Busca el error específico
3. Común: verifica que `requirements.txt` está en el repositorio
4. Común: verifica que `app.py` está en la raíz (no en subcarpeta)

### Problema: API key no funciona en Streamlit Cloud
**Solución:**
1. Ve a tu app → ⚙️ Settings → Secrets
2. Verifica formato TOML (sin comillas extra, sin JSON)
3. Click "Save" y espera a que reinicie

### Problema: El modo Frankenstein no combina bien
**Solución:**
- En modo demo, las respuestas son templates simples
- Configura una API key real para traducciones complejas con IA

---

## 📊 Verificación de Funcionalidades

Checklist para confirmar que todo funciona:

- [ ] La app carga sin errores
- [ ] Se muestra el modo (Demo o proveedor configurado)
- [ ] **Tab "Traducción Simple":** Traduce un animal correctamente
- [ ] **Tab "Traducción Simple":** Sube CSV de sensores y detecta anomalías
- [ ] **Tab "Modo Frankenstein":** Combina 2 fuentes diferentes
- [ ] **Tab "Guion Demo":** Los 3 botones funcionan
- [ ] **Tab "Historial":** Muestra las traducciones previas
- [ ] Todas las respuestas incluyen disclaimer visible
- [ ] Se puede exportar historial a CSV

---

## 🎯 Siguientes Pasos Post-Despliegue

### Para Mejorar la App
1. Agregar más patrones a `data/patrones.json`
2. Configurar API key para traducciones más sofisticadas
3. Compartir URL con usuarios para feedback
4. Revisar métricas en Streamlit Cloud (Analytics)

### Para Desarrollo
1. Crear branch de desarrollo: `git checkout -b desarrollo`
2. Hacer cambios y probar local
3. Merge a main y push para actualizar producción automáticamente

### Para Expandir Funcionalidades
- Ver sección "Trabajo Futuro" en README.md
- Priorizar: API REST, más patrones, soporte de audio

---

## 📞 Recursos y Documentación

- **README completo:** `README.md`
- **Guion de demo:** `DEMO_GUIDE.md`
- **Tests:** `pytest tests/ -v`
- **Streamlit docs:** https://docs.streamlit.io
- **LangChain docs:** https://python.langchain.com/docs/

---

## ✅ Confirmación de Éxito

Tu despliegue está completo cuando puedes:

1. ✅ Abrir la URL pública de tu app
2. ✅ Ejecutar los 3 ejemplos del guion de demo
3. ✅ Ver traducciones con confianza y disclaimer
4. ✅ Exportar el historial a CSV

**¡Felicidades! Frankenstein Lingua está vivo.** ⚡🧬

---

**Tiempo total estimado:**
- Local: 5 minutos
- Streamlit Cloud: 10 minutos
- Total con ambos: 15 minutos

**Última actualización:** 2024
