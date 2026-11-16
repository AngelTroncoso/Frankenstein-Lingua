"""
Frankenstein Lingua - Interfaz Streamlit
Agente de traducción de comunicación entre especies
"""
import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
from agent.frankenstein_agent import FrankensteinAgent
import json
import pandas as pd
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="Frankenstein Lingua",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-style: italic;
        margin-bottom: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .traduccion-box {
        background-color: #f0f7f0;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #2E7D32;
        margin: 1rem 0;
    }
    .disclaimer-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


def inicializar_sesion():
    """Inicializa variables de sesión."""
    if 'historial' not in st.session_state:
        st.session_state.historial = []
    if 'agente' not in st.session_state:
        # Detectar configuración
        provider = os.getenv('LLM_PROVIDER', 'demo')
        api_key = None
        model = None
        
        if provider == 'openai':
            api_key = os.getenv('OPENAI_API_KEY')
            model = os.getenv('OPENAI_MODEL')
        elif provider == 'mistral':
            api_key = os.getenv('MISTRAL_API_KEY')
            model = os.getenv('MISTRAL_MODEL')
        
        # Si no hay API key, forzar modo demo
        if not api_key and provider != 'demo':
            provider = 'demo'
        
        st.session_state.agente = FrankensteinAgent(
            llm_provider=provider,
            api_key=api_key,
            model=model
        )
        st.session_state.provider = provider


def mostrar_header():
    """Muestra el encabezado de la aplicación."""
    st.markdown('<h1 class="main-header">⚡ Frankenstein Lingua</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Agente de traducción universal entre especies</p>', unsafe_allow_html=True)
    
    # Mostrar modo de operación
    modo = st.session_state.get('provider', 'demo')
    if modo == 'demo':
        st.warning("🧪 **Modo Demo Activo** - Las traducciones son simuladas. Configura una API key en `.env` para usar IA real.", icon="⚠️")
    else:
        st.success(f"✅ Conectado a {modo.upper()}", icon="🤖")


def mostrar_resultado(resultado: dict, titulo: str = "Traducción"):
    """Muestra el resultado de una traducción."""
    st.markdown(f"### {titulo}")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"**Tipo de ser vivo:** {resultado['tipo_ser'].title()}")
    
    with col2:
        # Medidor de confianza con color
        confianza = resultado['confianza']
        color = "#4CAF50" if confianza >= 70 else "#FFC107" if confianza >= 40 else "#F44336"
        st.markdown(f"**Confianza:** <span style='color:{color};font-weight:bold'>{confianza}%</span>", unsafe_allow_html=True)
    
    # Traducción
    st.markdown('<div class="traduccion-box">', unsafe_allow_html=True)
    st.markdown(resultado['traduccion'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Evidencia
    if resultado.get('evidencia'):
        with st.expander("📚 Ver evidencia científica"):
            for ev in resultado['evidencia']:
                st.markdown(f"- {ev}")
    
    # Disclaimer
    st.markdown('<div class="disclaimer-box">', unsafe_allow_html=True)
    st.markdown(resultado['disclaimer'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Agregar al historial
    st.session_state.historial.append({
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'tipo': resultado['tipo_ser'],
        'confianza': resultado['confianza'],
        'traduccion': resultado['traduccion']
    })


def tab_simple():
    """Interfaz para traducción simple."""
    st.header("🔬 Traducción Simple")
    st.write("Describe la observación de un ser vivo y obtén su traducción.")
    
    observacion = st.text_area(
        "Describe lo que observaste:",
        placeholder="Ejemplo: Mi perro está ladrando de forma aguda y repetida mientras mira hacia la puerta",
        height=100
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        usar_csv = st.checkbox("📊 Incluir datos de sensores (para plantas)")
    
    csv_path = None
    if usar_csv:
        with col2:
            archivo_csv = st.file_uploader("Sube tu CSV de sensores", type=['csv'])
            if archivo_csv:
                # Guardar temporalmente
                csv_path = f"temp_sensores_{datetime.now().timestamp()}.csv"
                with open(csv_path, 'wb') as f:
                    f.write(archivo_csv.getbuffer())
    
    if st.button("🌍 Traducir", type="primary", use_container_width=True):
        if not observacion:
            st.error("Por favor, describe una observación.")
            return
        
        with st.spinner("🧬 Cosiendo fragmentos de conocimiento..."):
            resultado = st.session_state.agente.traducir(observacion, csv_path)
            
            if 'error' in resultado:
                st.error(f"Error: {resultado['error']}")
            else:
                mostrar_resultado(resultado)
        
        # Limpiar archivo temporal
        if csv_path and os.path.exists(csv_path):
            os.remove(csv_path)


def tab_frankenstein():
    """Interfaz para modo Frankenstein (combinación)."""
    st.header("⚡ Modo Frankenstein")
    st.write("Combina señales de diferentes seres vivos para una traducción integrada.")
    
    num_fuentes = st.number_input("¿Cuántas fuentes quieres combinar?", min_value=2, max_value=4, value=2)
    
    observaciones = []
    csv_paths = []
    
    for i in range(int(num_fuentes)):
        st.markdown(f"#### Fuente {i+1}")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            obs = st.text_area(
                f"Observación {i+1}:",
                placeholder=f"Ejemplo: Un cactus con arrugas en su superficie",
                height=80,
                key=f"obs_{i}"
            )
            observaciones.append(obs)
        
        with col2:
            usar_csv_i = st.checkbox(f"CSV #{i+1}", key=f"csv_check_{i}")
            if usar_csv_i:
                archivo = st.file_uploader(f"CSV #{i+1}", type=['csv'], key=f"csv_file_{i}")
                if archivo:
                    csv_path_i = f"temp_frankenstein_{i}_{datetime.now().timestamp()}.csv"
                    with open(csv_path_i, 'wb') as f:
                        f.write(archivo.getbuffer())
                    csv_paths.append(csv_path_i)
                else:
                    csv_paths.append(None)
            else:
                csv_paths.append(None)
    
    if st.button("⚡ ¡Coser Traducciones!", type="primary", use_container_width=True):
        if not all(observaciones):
            st.error("Por favor, completa todas las observaciones.")
            return
        
        with st.spinner("⚡ Cosiendo las partes del monstruo..."):
            resultado = st.session_state.agente.traducir_frankenstein(observaciones, csv_paths)
            
            if 'error' in resultado:
                st.error(f"Error: {resultado['error']}")
            else:
                mostrar_resultado(resultado, "🧟 Traducción Frankenstein")
                
                # Mostrar traducciones individuales
                with st.expander("🔍 Ver traducciones individuales"):
                    for i, trad in enumerate(resultado.get('traducciones_individuales', [])):
                        st.markdown(f"**Fuente {i+1} ({trad['tipo_ser']})**")
                        st.markdown(trad['traduccion'][:200] + "...")
                        st.markdown("---")
        
        # Limpiar archivos temporales
        for csv_p in csv_paths:
            if csv_p and os.path.exists(csv_p):
                os.remove(csv_p)


def tab_ejemplos():
    """Guion de demo con ejemplos listos."""
    st.header("🎬 Guion de Demo")
    st.write("Ejemplos listos para probar el sistema en 2 minutos.")
    
    st.markdown("### Ejemplo 1: Animal (Perro) 🐕")
    if st.button("Probar Ejemplo 1", key="ej1"):
        obs = "Mi perro está ladrando de forma aguda y repetida mientras mira hacia la puerta y mueve la cola"
        with st.spinner("Traduciendo..."):
            resultado = st.session_state.agente.traducir(obs)
            mostrar_resultado(resultado)
    
    st.markdown("---")
    
    st.markdown("### Ejemplo 2: Planta con Sensores 🌱")
    st.write("Usa el archivo `data/sensores_ejemplo.csv` incluido en el proyecto.")
    if st.button("Probar Ejemplo 2", key="ej2"):
        obs = "Mi planta de tomate tiene las hojas enrolladas hacia arriba"
        csv_ejemplo = "data/sensores_ejemplo.csv"
        if os.path.exists(csv_ejemplo):
            with st.spinner("Traduciendo..."):
                resultado = st.session_state.agente.traducir(obs, csv_ejemplo)
                mostrar_resultado(resultado)
        else:
            st.error("Archivo de ejemplo no encontrado. Asegúrate de que data/sensores_ejemplo.csv existe.")
    
    st.markdown("---")
    
    st.markdown("### Ejemplo 3: Modo Frankenstein ⚡")
    if st.button("Probar Ejemplo 3", key="ej3"):
        obs1 = "Una abeja está realizando una danza en forma de 8"
        obs2 = "Un cactus presenta arrugas en su superficie"
        with st.spinner("Cosiendo traducciones..."):
            resultado = st.session_state.agente.traducir_frankenstein([obs1, obs2])
            mostrar_resultado(resultado, "⚡ Traducción Frankenstein")


def tab_historial():
    """Muestra el historial de traducciones."""
    st.header("📜 Historial de Traducciones")
    
    if not st.session_state.historial:
        st.info("Aún no hay traducciones en esta sesión.")
        return
    
    # Mostrar historial
    df_historial = pd.DataFrame(st.session_state.historial)
    st.dataframe(df_historial, use_container_width=True)
    
    # Opción de exportar
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("📥 Exportar a CSV"):
            csv = df_historial.to_csv(index=False)
            st.download_button(
                label="Descargar CSV",
                data=csv,
                file_name=f"frankenstein_lingua_historial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )


def sidebar():
    """Barra lateral con información y configuración."""
    with st.sidebar:
        st.image("https://em-content.zobj.net/thumbs/240/google/350/brain_1f9e0.png", width=100)
        
        st.markdown("### ⚡ Frankenstein Lingua")
        st.markdown("**Versión:** 1.0.0 MVP")
        
        st.markdown("---")
        
        st.markdown("### 🎯 Cómo usar")
        st.markdown("""
        1. **Traducción Simple:** Describe una señal de un ser vivo
        2. **Modo Frankenstein:** Combina múltiples fuentes
        3. **Ejemplos Demo:** Prueba los casos predefinidos
        """)
        
        st.markdown("---")
        
        st.markdown("### 🔬 Base de Conocimiento")
        st.info(f"📚 {len(st.session_state.agente._FrankensteinAgent__class__.__dict__.get('cargar_patrones', lambda: {'patrones': []})())} patrones cargados")
        
        st.markdown("---")
        
        st.markdown("### ⚙️ Configuración")
        modo_actual = st.session_state.get('provider', 'demo')
        st.markdown(f"**Modo:** {modo_actual.upper()}")
        
        if modo_actual == 'demo':
            st.warning("Configura `.env` para usar IA real")
        
        st.markdown("---")
        
        st.markdown("### ℹ️ Acerca de")
        st.markdown("""
        Sistema experimental que interpreta señales de comunicación de animales, 
        plantas y hongos usando IA y conocimiento científico curado.
        
        **Disclaimer:** Este es un proyecto educativo y creativo. 
        No representa traducciones literales científicamente validadas.
        """)


def main():
    """Función principal de la aplicación."""
    inicializar_sesion()
    
    mostrar_header()
    sidebar()
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔬 Traducción Simple",
        "⚡ Modo Frankenstein",
        "🎬 Guion Demo",
        "📜 Historial"
    ])
    
    with tab1:
        tab_simple()
    
    with tab2:
        tab_frankenstein()
    
    with tab3:
        tab_ejemplos()
    
    with tab4:
        tab_historial()


if __name__ == "__main__":
    main()
