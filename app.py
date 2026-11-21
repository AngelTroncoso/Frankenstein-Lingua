"""
Frankenstein Lingua - Interfaz Streamlit
Agente de decodificación bioacústica y comunicación inter-especies
"""
import streamlit as st
import streamlit.components.v1 as components
import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv
from agent.frankenstein_agent import FrankensteinAgent
from agent.bioacoustics import (
    calcular_metricas_biolinguisticas,
    generar_datos_espectrograma,
    generar_sintetizador_audio_html,
    obtener_perfil_especie
)
import pandas as pd
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}
HERO_IMAGE_PATH = Path(__file__).parent / "assets" / "ecosistema.svg"

# Configuración de la página
st.set_page_config(
    page_title="Frankenstein Lingua · Bioacoustic AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


def inyectar_estilos_futuristas():
    """Inyecta CSS con estética Bio-Cybernetic Lab y Glassmorphism."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', -apple-system, sans-serif;
    }

    /* Fondo espacial profundo con gradientes bioluminiscentes */
    .stApp {
        background: radial-gradient(circle at 12% 18%, rgba(0, 242, 254, 0.06) 0%, transparent 40%),
                    radial-gradient(circle at 88% 82%, rgba(79, 172, 254, 0.06) 0%, transparent 45%),
                    #080c16;
        color: #e2e8f0;
    }

    /* Tarjetas Glassmorphic */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(14, 22, 40, 0.65) !important;
        border: 1px solid rgba(0, 242, 254, 0.22) !important;
        backdrop-filter: blur(14px) !important;
        border-radius: 14px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45) !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }

    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: rgba(0, 242, 254, 0.5) !important;
        box-shadow: 0 10px 36px rgba(0, 242, 254, 0.15) !important;
    }

    /* Botones primarios neón */
    .stButton > button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
        color: #040914 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.55rem 1.6rem !important;
        box-shadow: 0 4px 18px rgba(0, 242, 254, 0.35) !important;
        transition: all 0.25s ease !important;
        letter-spacing: 0.5px;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 28px rgba(0, 242, 254, 0.6) !important;
        color: #000000 !important;
    }

    /* Tabs futuristas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(10, 18, 34, 0.75);
        padding: 6px 10px;
        border-radius: 12px;
        border: 1px solid rgba(0, 242, 254, 0.18);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 600;
        padding: 8px 16px;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 242, 254, 0.22), rgba(79, 172, 254, 0.25)) !important;
        color: #00f2fe !important;
        border-bottom: 2px solid #00f2fe !important;
    }

    /* Inputs y textareas */
    .stTextArea textarea, .stTextInput input, .stSelectbox [data-baseweb="select"] {
        background-color: rgba(9, 15, 28, 0.85) !important;
        border: 1px solid rgba(0, 242, 254, 0.25) !important;
        color: #f1f5f9 !important;
        border-radius: 10px !important;
    }

    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #00f2fe !important;
        box-shadow: 0 0 12px rgba(0, 242, 254, 0.35) !important;
    }

    /* Métricas destacadas con brillo */
    div[data-testid="stMetricValue"] {
        color: #00f2fe !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700 !important;
        text-shadow: 0 0 14px rgba(0, 242, 254, 0.45);
    }

    /* Badges de familias */
    .bio-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        background: rgba(0, 242, 254, 0.12);
        color: #00f2fe;
        border: 1px solid rgba(0, 242, 254, 0.35);
        margin-right: 6px;
    }
    </style>
    """, unsafe_allow_html=True)


def inicializar_sesion():
    """Inicializa variables de sesión."""
    if 'historial' not in st.session_state:
        st.session_state.historial = []
    if 'agente' not in st.session_state:
        provider = os.getenv('LLM_PROVIDER', 'demo')
        api_key = None
        model = None
        
        if provider == 'openai':
            api_key = os.getenv('OPENAI_API_KEY')
            model = os.getenv('OPENAI_MODEL')
        elif provider == 'mistral':
            api_key = os.getenv('MISTRAL_API_KEY')
            model = os.getenv('MISTRAL_MODEL')
        
        if not api_key and provider != 'demo':
            provider = 'demo'
        
        st.session_state.agente = FrankensteinAgent(
            llm_provider=provider,
            api_key=api_key,
            model=model
        )
        st.session_state.provider = provider


def mostrar_header():
    """Muestra el encabezado con estética futurista de laboratorio."""
    modo = st.session_state.get('provider', 'demo')
    with st.container(border=True):
        columna_titulo, columna_imagen = st.columns([1.5, 1])
        with columna_titulo:
            st.markdown('<span class="bio-badge">UNIVERSAL BIOACOUSTIC AGENT</span><span class="bio-badge">COGNICIÓN COMPARADA</span>', unsafe_allow_html=True)
            st.title("⚡ Frankenstein Lingua")
            st.write(
                "Decodificación bioacústica y síntesis comunicativa entre las especies más cercanas "
                "al lenguaje: **Cetáceos, Primates no humanos, Córvidos/Psitácidos y Elefantes**."
            )
            if modo == 'demo':
                st.warning(
                    "Modo Demo Científico · Síntesis y análisis bioacústico con datos curados.",
                    icon=":material/science:"
                )
            else:
                st.success(f"Motor IA Conectado: {modo.upper()}", icon=":material/check_circle:")
        with columna_imagen:
            st.image(
                str(HERO_IMAGE_PATH),
                caption="Protocolos de comunicación animal avanzada",
                width=340
            )


def mostrar_resultado(resultado: dict, titulo: str = "Traducción"):
    """Muestra el resultado con consola bioacústica, espectrograma y métricas."""
    confianza = resultado['confianza']
    especie_identificada = resultado['tipo_ser']

    with st.container(border=True):
        st.subheader(titulo)
        columna_tipo, columna_confianza = st.columns([3, 1])
        with columna_tipo:
            st.caption("Especie / Familia identificada")
            st.markdown(f"### {especie_identificada.title()}")
        with columna_confianza:
            st.metric("Confianza científica", f"{confianza}%")
        st.progress(confianza / 100)
        st.markdown(resultado['traduccion'])

        # Consola Bioacústica interactiva (Audio Synthesizer con Web Audio API)
        st.caption("CONSOLA BIOACÚSTICA NEURAL")
        components.html(generar_sintetizador_audio_html(especie_identificada), height=135)

        # Espectrograma interactivo y métricas cuantitativas
        with st.expander("📊 Ver Espectrograma Dinámico y Métricas Cuantitativas", expanded=True):
            metricas = calcular_metricas_biolinguisticas(resultado['traduccion'], especie_identificada)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Entropía de Shannon", metricas['entropia_shannon'])
            c2.metric("Frecuencia Pico", metricas['frecuencia_pico'])
            c3.metric("Complejidad Sintáctica", f"{metricas['indice_sintaxis']}%")
            c4.metric("Canal de Transmisión", metricas['rango_frecuencia'])

            df_spec = generar_datos_espectrograma(especie_identificada)
            st.caption("Envolvente espectro-temporal de la señal:")
            st.line_chart(
                df_spec.set_index('Tiempo (s)')[['Frecuencia (kHz)', 'Intensidad (dB/Potencia)']],
                height=220
            )

    if resultado.get('evidencia'):
        with st.expander("Consultar evidencia científica", icon=":material/science:"):
            for ev in resultado['evidencia']:
                st.markdown(f"- {ev}")

    st.warning(resultado['disclaimer'], icon=":material/info:")

    st.session_state.historial.append({
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'tipo': resultado['tipo_ser'],
        'confianza': resultado['confianza'],
        'traduccion': resultado['traduccion']
    })


def tab_simple():
    """Interfaz para traducción bioacústica simple."""
    st.header("Traducción e Interpretación Bioacústica", icon=":material/biotech:")
    st.write(
        "Describe una señal comunicativa observada en animales con alta capacidad cognitiva "
        "(silbidos firma, codas rítmicas, pant-hoots sintácticos, alarmas semánticas o infrasonidos)."
    )

    with st.container(border=True):
        with st.form("traduccion_simple"):
            observacion = st.text_area(
                "Señal o conducta observada",
                placeholder="Ejemplo: Un cachalote emite una serie de clics rítmicos en patrón 1+1+3 con modulación coordinada de tempo ante miembros de su clan matrilíneo.",
                height=120
            )
            archivo_csv = st.file_uploader(
                "Datos bioacústicos o telemetría (CSV opcional)",
                type=['csv'],
                help="Añade un CSV con datos de frecuencia o tiempo para complementar el análisis."
            )
            traducir = st.form_submit_button(
                "⚡ Decodificar Señal Bioacústica",
                type="primary",
                width="stretch"
            )

    if traducir:
        if not observacion.strip():
            st.error("Describe una observación antes de continuar.")
            return

        if archivo_csv:
            with tempfile.TemporaryDirectory(prefix="frankenstein_sensores_") as directorio:
                csv_path = Path(directorio) / "sensores.csv"
                csv_path.write_bytes(archivo_csv.getvalue())
                with st.spinner("Analizando la señal bioacústica y telemetría..."):
                    resultado = st.session_state.agente.traducir(observacion, str(csv_path))
        else:
            with st.spinner("Analizando la señal con modelos bioacústicos..."):
                resultado = st.session_state.agente.traducir(observacion)

        if 'error' in resultado:
            st.error(f"Error: {resultado['error']}")
        else:
            mostrar_resultado(resultado)


def tab_router_interespecies():
    """Módulo innovador: Router de Comunicación Directa Animal A ↔ Animal B."""
    st.header("🔀 Router Inter-Especies (Animal A ↔ Animal B)", icon=":material/swap_calls:")
    st.write(
        "**Transposición neural y bioacústica directa:** toma el mensaje de una especie emisora, "
        "extrae sus invariantes semánticos universales y lo transpone al canal bioacústico y sintaxis de la especie receptora."
    )

    especies_disponibles = [
        "Cachalote (Codas rítmicas submarinas)",
        "Delfín (Silbidos firma ultrasónicos)",
        "Chimpancé (Pant-hoots y tamborileo sísmico)",
        "Bonobo (Peep-calls y lexigramas deícticos)",
        "Elefante (Rumbles infrasónicos terrestres)",
        "Cuervo (Señalamiento y llamadas moduladas)",
        "Loro Gris Africano (Categorización conceptual)",
        "Carbonero Japonés (Sintaxis composicional ABC-D)"
    ]

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.subheader("1. Especie Emisora (Origen)")
            sel_origen = st.selectbox("Selecciona emisor", especies_disponibles, index=0)
            esp_origen = sel_origen.split()[0].lower()

            presets = {
                "cachalote": "Coda rítmica 1+1+3 advirtiendo presencia de orcas depredadoras y llamando a agrupación del clan",
                "delfín": "Silbido firma individual ascendente coordinando maniobra de cerco a cardumen",
                "chimpancé": "Secuencia ordenada de pant-hoots dobles alertando sobre frutos en árbol alto",
                "bonobo": "Vocalización peep modulada solicitando cooperación con gesto deíctico manual",
                "elefante": "Rumble de infrasonido nominal alertando sobre enjambre de abejas",
                "cuervo": "Graznido de reclutamiento con señalamiento con el pico hacia objeto desconocido",
                "loro": "Llamada referencial distinguiendo objeto grande de color rojo",
                "carbonero": "Combinación sintáctica de notas alerta-reclutamiento ABC-D"
            }
            preset_default = presets.get(esp_origen, "Llamada de alerta y coordinación grupal")

            senal_input = st.text_area(
                "Señal emitida en su sistema nativo",
                value=preset_default,
                height=100
            )

    with col2:
        with st.container(border=True):
            st.subheader("2. Especie Receptora (Destino)")
            sel_destino = st.selectbox("Selecciona receptor", especies_disponibles, index=1)
            esp_destino = sel_destino.split()[0].lower()

            st.caption("Canal físico del receptor:")
            perf_dest = obtener_perfil_especie(esp_destino)
            st.info(f"📡 {perf_dest['canal']} (Frecuencia: {perf_dest['rango_frecuencia_hz'][0]} - {perf_dest['rango_frecuencia_hz'][1]} Hz)")

    if st.button("⚡ Transpolar Protocolo Comunicativo (A ➔ B)", type="primary", width="stretch"):
        with st.spinner(f"Transpolando señal de {esp_origen.title()} a {esp_destino.title()}..."):
            res_router = st.session_state.agente.traducir_interespecies(
                especie_origen=esp_origen,
                senal_origen=senal_input,
                especie_destino=esp_destino
            )

        with st.container(border=True):
            st.subheader("⚡ Señal Transpuesta y Adaptada")
            m1, m2 = st.columns([3, 1])
            with m1:
                st.markdown(f"**Mensaje adaptado al sistema de {res_router['especie_destino']}:**")
                st.markdown(f"> *\"{res_router['senal_transpuesta']}\"*")
            with m2:
                st.metric("Inteligibilidad Teórica", f"{res_router['inteligibilidad_estimada']}%")

            st.markdown(f"**Mecanismo de transducción:** {res_router['mecanismo_biologico']}")

            # Invariantes semánticos
            with st.expander("🔬 Invariantes Semánticos Universales Extraídos", expanded=True):
                inv = res_router['invariante_semantico']
                ic1, ic2, ic3 = st.columns(3)
                ic1.markdown(f"**Intención:**\n{inv['intencion']}")
                ic2.markdown(f"**Valencia Afectiva:**\n{inv['valencia']}")
                ic3.markdown(f"**Nivel de Urgencia:**\n{inv['urgencia']}")

            # Consola bioacústica del receptor
            st.caption(f"Audio bioacústico transpolar en canal de {res_router['especie_destino']}:")
            components.html(generar_sintetizador_audio_html(esp_destino), height=135)


def tab_frankenstein():
    """Interfaz para modo Frankenstein (combinación multi-especies)."""
    st.header("Modo Frankenstein (Fusión Multi-Especies)", icon=":material/hub:")
    st.write(
        "Combina señales bioacústicas de diferentes especies para explorar la convergencia "
        "y encontrar principios universales de comunicación animal."
    )

    num_fuentes = st.number_input(
        "Especies a combinar",
        min_value=2,
        max_value=4,
        value=2,
        help="Elige entre dos y cuatro fuentes."
    )

    observaciones = []
    archivos_csv = []
    archivos_imagen = []

    for i in range(int(num_fuentes)):
        with st.container(border=True):
            st.subheader(f"Especie / Fuente {i + 1}")
            obs = st.text_area(
                "Describe la señal bioacústica o conductual",
                placeholder="Ejemplo: Un delfín mular reproduce su silbido firma individual mientras interactúa.",
                height=90,
                key=f"obs_{i}"
            )
            observaciones.append(obs)
            columna_sensores, columna_imagen = st.columns(2)
            with columna_sensores:
                archivo_csv = st.file_uploader(
                    "Telemetría / CSV (opcional)",
                    type=['csv'],
                    key=f"csv_file_{i}"
                )
                archivos_csv.append(archivo_csv)
            with columna_imagen:
                archivo_imagen = st.file_uploader(
                    "Foto o espectrograma (opcional)",
                    type=['jpg', 'jpeg', 'png'],
                    key=f"image_file_{i}"
                )
                archivos_imagen.append(archivo_imagen)

    combinar = st.button("⚡ Coser Señales Multi-Especie", type="primary", width="stretch")
    if combinar:
        if not all(observacion.strip() for observacion in observaciones):
            st.error("Completa la observación de cada fuente antes de continuar.")
            return

        imagenes = []
        for archivo in archivos_imagen:
            if archivo:
                imagenes.append((archivo.getvalue(), archivo.type))
            else:
                imagenes.append(None)

        with tempfile.TemporaryDirectory(prefix="frankenstein_fuentes_") as directorio:
            csv_paths = []
            for i, archivo in enumerate(archivos_csv):
                if archivo:
                    csv_path = Path(directorio) / f"sensores_{i + 1}.csv"
                    csv_path.write_bytes(archivo.getvalue())
                    csv_paths.append(str(csv_path))
                else:
                    csv_paths.append(None)

            with st.spinner("Sintetizando la comunicación de cada especie..."):
                resultado = st.session_state.agente.traducir_frankenstein(
                    observaciones,
                    csv_paths,
                    imagenes
                )

        if 'error' in resultado:
            st.error(f"Error: {resultado['error']}")
        else:
            mostrar_resultado(resultado, "Síntesis Multi-Especies Frankenstein")


def tab_ejemplos():
    """Guion de demo con ejemplos listos para presentar."""
    st.header("Ejemplos Guiados de Demostración", icon=":material/play_circle:")
    st.write("Escenarios preconfigurados para una demo de 90 segundos frente a los jueces:")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.subheader("🐬 Cachalote (Project CETI)")
            st.caption("Codas rítmicas con combinatoria y alfabeto acústico.")
            if st.button("Probar Cachalote", key="ej1", width="stretch"):
                obs = "Un cachalote emite una coda rítmica de clics con patrón 1+1+3 y tempo coordinado ante miembros de su clan matrilíneo"
                with st.spinner("Decodificando coda bioacústica..."):
                    resultado = st.session_state.agente.traducir(obs)
                mostrar_resultado(resultado)

    with col2:
        with st.container(border=True):
            st.subheader("🦧 Chimpancé (Sintaxis)")
            st.caption("Secuencias ordenadas de pant-hoots y percusión.")
            if st.button("Probar Chimpancé", key="ej2", width="stretch"):
                obs = "Un chimpancé emite secuencias ordenadas de pant-hoots combinadas con tamborileo de raíces al avistar a miembros aliados"
                with st.spinner("Decodificando sintaxis vocal..."):
                    resultado = st.session_state.agente.traducir(obs)
                mostrar_resultado(resultado)

    with col3:
        with st.container(border=True):
            st.subheader("🐘 Elefante (Infrasonido)")
            st.caption("Rumble infrasónico con etiqueta nominal individual.")
            if st.button("Probar Elefante", key="ej3", width="stretch"):
                obs = "Un elefante africano emite un rumble de infrasonido de baja frecuencia con etiqueta nominal individual dirigida a su cría"
                with st.spinner("Decodificando infrasonido sísmico..."):
                    resultado = st.session_state.agente.traducir(obs)
                mostrar_resultado(resultado)


def tab_historial():
    """Muestra el registro de traducciones."""
    st.header("Historial de Análisis", icon=":material/history:")

    if not st.session_state.historial:
        st.info("Las interpretaciones que generes durante esta sesión aparecerán aquí.")
        return

    df_historial = pd.DataFrame(st.session_state.historial).rename(columns={
        "timestamp": "Fecha y hora",
        "tipo": "Especie / Ser",
        "confianza": "Confianza (%)",
        "traduccion": "Interpretación"
    })
    with st.container(border=True):
        st.dataframe(df_historial, width="stretch", hide_index=True)
        st.download_button(
            label="Descargar Historial Bioacústico CSV",
            data=df_historial.to_csv(index=False),
            file_name=f"frankenstein_bioacoustic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            icon=":material/download:"
        )


def sidebar():
    """Barra lateral con telemetría de la base de conocimiento y configuración."""
    with st.sidebar:
        st.markdown("### ⚡ Frankenstein Lingua")
        st.caption("Plataforma de Decodificación Bioacústica")

        st.subheader("Especies en Estudio")
        st.markdown(
            "- 🐬 **Cetáceos:** Delfines, Cachalotes, Orcas\n"
            "- 🦧 **Primates:** Bonobos, Chimpancés, Vervets\n"
            "- 🦅 **Aves:** Cuervos, Loro gris, Carbonero\n"
            "- 🐘 **Elefantes:** Infrasonidos nominales"
        )

        st.subheader("Base de Patrones")
        try:
            from agent.tools import cargar_patrones
            num_patrones = len(cargar_patrones())
            st.caption(f"✓ {num_patrones} patrones bioacústicos validados")
        except Exception as error:
            st.warning(f"Error: {error}")

        st.subheader("Motor de Inferencia")
        modo_actual = st.session_state.get('provider', 'demo')
        st.markdown(f"**Modo:** `{modo_actual.upper()}`")
        if modo_actual == 'demo':
            st.caption("Configura `OPENAI_API_KEY` o `MISTRAL_API_KEY` en `.env` para LLM en tiempo real.")

        with st.expander("Acerca del Proyecto"):
            st.write(
                "Inspirado en Project CETI e investigaciones de Nature sobre sintaxis animal, "
                "codas de cachalotes y etiquetas nominales en elefantes."
            )
        st.caption("Versión 2.0.0 Hackathon Edition")


def main():
    """Función principal de la aplicación."""
    inyectar_estilos_futuristas()
    inicializar_sesion()
    mostrar_header()
    sidebar()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        ":material/biotech: Traducción Bioacústica",
        ":material/swap_calls: Router Inter-Especies",
        ":material/hub: Modo Frankenstein",
        ":material/play_circle: Ejemplos Guiados",
        ":material/history: Historial"
    ])

    with tab1:
        tab_simple()

    with tab2:
        tab_router_interespecies()

    with tab3:
        tab_frankenstein()

    with tab4:
        tab_ejemplos()

    with tab5:
        tab_historial()


if __name__ == "__main__":
    main()
