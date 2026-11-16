# ⚡ Quickstart - Frankenstein Lingua

**Para los impacientes: 3 comandos y estás corriendo.**

---

## 🚀 Inicio Rápido (2 minutos)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar la app
streamlit run app.py

# 3. ¡Listo! Se abre automáticamente en tu navegador
```

La app funciona en **modo demo** sin configuración adicional.

---

## 🎬 Primeros Pasos en la UI

1. **Ve a la pestaña "🎬 Guion Demo"**
2. **Presiona "Probar Ejemplo 1"** → Traducción de perro
3. **Presiona "Probar Ejemplo 2"** → Planta con sensores
4. **Presiona "Probar Ejemplo 3"** → Modo Frankenstein

**¡Ya viste todas las funcionalidades principales!**

---

## 🔑 (Opcional) Activar IA Real

Si quieres traducciones con GPT-4 en lugar de respuestas demo:

```bash
# 1. Copiar template
cp .env.example .env

# 2. Editar .env y agregar:
# LLM_PROVIDER=openai
# OPENAI_API_KEY=tu-clave-aqui

# 3. Reiniciar la app
streamlit run app.py
```

---

## ✅ Verificar que Todo Funciona

```bash
# Ejecutar tests
pytest

# Deberías ver: 11 passed
```

---

## 📚 ¿Quieres Más?

- **README completo:** [README.md](README.md)
- **Guion de demo 2 min:** [DEMO_GUIDE.md](DEMO_GUIDE.md)
- **Despliegue en cloud:** [DEPLOYMENT_STEPS.md](DEPLOYMENT_STEPS.md)
- **Resumen ejecutivo:** [RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md)

---

**¡Eso es todo! Ya tienes Frankenstein Lingua funcionando.** ⚡🧬
