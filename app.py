"""
Frankenstein Lingua - Interfaz Streamlit
Agente de traducción de comunicación entre especies
"""
import streamlit as st
import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv
from agent.frankenstein_agent import FrankensteinAgent
import pandas as pd
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}
HERO_IMAGE_PATH = Path(__file__).parent / "assets" / "ecosistema.svg"

# Configuración de la página
st.set_page_config(
    page_title="Frankenstein Lingua",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    modo = st.session_state.get('provider', 'demo')
    with st.container(border=True):
        columna_titulo, columna_imagen = st.columns([1.5, 1])
        with columna_titulo:
            st.caption("LABORATORIO INTERESPECIE · CIENCIA + IA")
            st.title("Frankenstein Lingua")
            st.write("Un puente visual entre las señales de la naturaleza y la curiosidad humana.")
            if modo == 'demo':
                st.warning(
                    "Modo Demo · Las interpretaciones son simuladas.",
                    icon=":material/science:"
                )
            else:
                st.success(f"{modo.upper()}", icon=":material/check_circle:")
        with columna_imagen:
            st.image(
                str(HERO_IMAGE_PATH),
                caption="Señales conectadas entre especies",
                width=360
            )


def mostrar_resultado(resultado: dict, titulo: str = "Traducción"):
    """Muestra el resultado de una traducción."""
    confianza = resultado['confianza']
    with st.container(border=True):
        st.subheader(titulo)
        columna_tipo, columna_confianza = st.columns([3, 1])
        with columna_tipo:
            st.caption("Ser vivo identificado")
            st.write(resultado['tipo_ser'].title())
        with columna_confianza:
            st.metric("Confianza estimada", f"{confianza}%")
        st.progress(confianza / 100)
        st.markdown(resultado['traduccion'])

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
    """Interfaz para traducción simple."""
    st.header("Traducción simple", icon=":material/biotech:")
    st.write("Describe una señal observada. Puedes añadir lecturas de sensores para complementar el análisis de una planta.")

    with st.container(border=True):
        with st.form("traduccion_simple"):
            observacion = st.text_area(
                "¿Qué observaste?",
                placeholder="Ejemplo: Mi perro ladra de forma aguda y repetida mientras mira hacia la puerta.",
                height=130
            )
            archivo_csv = st.file_uploader(
                "Lecturas de sensores (opcional)",
                type=['csv'],
                help="Añade un CSV con datos ambientales para complementar la interpretación."
            )
            traducir = st.form_submit_button(
                "Generar interpretación",
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
                with st.spinner("Analizando la observación y los datos..."):
                    resultado = st.session_state.agente.traducir(observacion, str(csv_path))
        else:
            with st.spinner("Analizando la observación..."):
                resultado = st.session_state.agente.traducir(observacion)

        if 'error' in resultado:
            st.error(f"Error: {resultado['error']}")
        else:
            mostrar_resultado(resultado)


def tab_frankenstein():
    """Interfaz para modo Frankenstein (combinación)."""
    st.header("Modo Frankenstein", icon=":material/hub:")
    st.write("Combina señales de distintas fuentes en una interpretación integrada.")
    st.caption(
        "Opcional: añade una foto por fuente para comparar rasgos visibles. "
        "El análisis requiere un modelo multimodal; las imágenes se envían al proveedor "
        "configurado y no se guardan en la aplicación."
    )

    num_fuentes = st.number_input(
        "Fuentes a combinar",
        min_value=2,
        max_value=4,
        value=2,
        help="Elige entre dos y cuatro observaciones."
    )

    observaciones = []
    archivos_csv = []
    archivos_imagen = []

    for i in range(int(num_fuentes)):
        with st.container(border=True):
            st.subheader(f"Fuente {i + 1}")
            obs = st.text_area(
                "Describe la señal observada",
                placeholder="Ejemplo: Un cactus presenta arrugas en su superficie.",
                height=100,
                key=f"obs_{i}"
            )
            observaciones.append(obs)
            columna_sensores, columna_imagen = st.columns(2)
            with columna_sensores:
                archivo_csv = st.file_uploader(
                    "Lecturas de sensores (opcional)",
                    type=['csv'],
                    key=f"csv_file_{i}"
                )
                archivos_csv.append(archivo_csv)
            with columna_imagen:
                archivo_imagen = st.file_uploader(
                    "Imagen de esta fuente (opcional)",
                    type=['jpg', 'jpeg', 'png'],
                    help="JPG o PNG; máximo 10 MB por imagen.",
                    key=f"image_file_{i}"
                )
                archivos_imagen.append(archivo_imagen)
                if archivo_imagen:
                    st.image(
                        archivo_imagen,
                        caption=f"Vista previa · Fuente {i + 1}",
                        width=220
                    )

    combinar = st.button(
        "Combinar interpretaciones",
        type="primary",
        width="stretch"
    )
    if combinar:
        if not all(observacion.strip() for observacion in observaciones):
            st.error("Completa la observación de cada fuente antes de continuar.")
            return

        if any(archivos_imagen) and st.session_state.agente.demo_mode:
            st.error(
                "El modo Demo no puede analizar imágenes. Configura un proveedor de IA "
                "y un modelo con capacidad visual para usar esta función."
            )
            return

        imagenes = []
        for indice, archivo_imagen in enumerate(archivos_imagen):
            if not archivo_imagen:
                imagenes.append(None)
                continue

            datos_imagen = archivo_imagen.getvalue()
            if len(datos_imagen) > MAX_IMAGE_SIZE_BYTES:
                st.error(f"La imagen de la fuente {indice + 1} supera el límite de 10 MB.")
                return
            if archivo_imagen.type not in ALLOWED_IMAGE_TYPES:
                st.error(f"El formato de la imagen de la fuente {indice + 1} no es compatible.")
                return

            imagenes.append((datos_imagen, archivo_imagen.type))

        with tempfile.TemporaryDirectory(prefix="frankenstein_fuentes_") as directorio:
            csv_paths = []
            for i, archivo in enumerate(archivos_csv):
                if archivo:
                    csv_path = Path(directorio) / f"sensores_{i + 1}.csv"
                    csv_path.write_bytes(archivo.getvalue())
                    csv_paths.append(str(csv_path))
                else:
                    csv_paths.append(None)

            with st.spinner("Integrando las señales de cada fuente..."):
                resultado = st.session_state.agente.traducir_frankenstein(
                    observaciones,
                    csv_paths,
                    imagenes
                )

        if 'error' in resultado:
            st.error(f"Error: {resultado['error']}")
        else:
            titulo = (
                "Interpretación integrada y compatibilidad visual"
                if any(imagenes)
                else "Interpretación integrada"
            )
            mostrar_resultado(resultado, titulo)
            traducciones = resultado.get('traducciones_individuales', [])
            if traducciones:
                with st.expander("Ver interpretaciones por fuente", icon=":material/search:"):
                    for i, traduccion in enumerate(traducciones):
                        st.markdown(f"**Fuente {i + 1} · {traduccion['tipo_ser']}**")
                        st.markdown(traduccion['traduccion'])


def tab_ejemplos():
    """Guion de demo con ejemplos listos."""
    st.header("Ejemplos guiados", icon=":material/play_circle:")
    st.write("Explora tres escenarios de muestra para conocer las distintas funciones.")

    columna_animal, columna_planta, columna_integrada = st.columns(3)

    with columna_animal:
        with st.container(border=True):
            st.subheader("Señal animal")
            st.caption("Interpretación de una conducta observada.")
            if st.button("Probar ejemplo", key="ej1", width="stretch"):
                observacion = "Mi perro está ladrando de forma aguda y repetida mientras mira hacia la puerta y mueve la cola"
                with st.spinner("Analizando la observación..."):
                    resultado = st.session_state.agente.traducir(observacion)
                if 'error' in resultado:
                    st.error(f"Error: {resultado['error']}")
                else:
                    mostrar_resultado(resultado)

    with columna_planta:
        with st.container(border=True):
            st.subheader("Planta y sensores")
            st.caption("Usa el CSV de muestra incluido en el proyecto.")
            if st.button("Probar ejemplo", key="ej2", width="stretch"):
                observacion = "Mi planta de tomate tiene las hojas enrolladas hacia arriba"
                csv_ejemplo = Path("data") / "sensores_ejemplo.csv"
                if csv_ejemplo.exists():
                    with st.spinner("Analizando la observación y los sensores..."):
                        resultado = st.session_state.agente.traducir(
                            observacion,
                            str(csv_ejemplo)
                        )
                    if 'error' in resultado:
                        st.error(f"Error: {resultado['error']}")
                    else:
                        mostrar_resultado(resultado)
                else:
                    st.error("No se encontró data/sensores_ejemplo.csv.")

    with columna_integrada:
        with st.container(border=True):
            st.subheader("Modo Frankenstein")
            st.caption("Integra señales de especies diferentes.")
            if st.button("Probar ejemplo", key="ej3", width="stretch"):
                observaciones = [
                    "Una abeja está realizando una danza en forma de 8",
                    "Un cactus presenta arrugas en su superficie"
                ]
                with st.spinner("Integrando las señales..."):
                    resultado = st.session_state.agente.traducir_frankenstein(observaciones)
                if 'error' in resultado:
                    st.error(f"Error: {resultado['error']}")
                else:
                    mostrar_resultado(resultado, "Interpretación integrada")


def tab_historial():
    """Muestra el historial de traducciones."""
    st.header("Historial de traducciones", icon=":material/history:")

    if not st.session_state.historial:
        st.info("Las interpretaciones que generes durante esta sesión aparecerán aquí.")
        return

    df_historial = pd.DataFrame(st.session_state.historial).rename(columns={
        "timestamp": "Fecha y hora",
        "tipo": "Ser vivo",
        "confianza": "Confianza (%)",
        "traduccion": "Interpretación"
    })
    with st.container(border=True):
        st.dataframe(df_historial, width="stretch", hide_index=True)
        st.download_button(
            label="Descargar historial CSV",
            data=df_historial.to_csv(index=False),
            file_name=f"frankenstein_lingua_historial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            icon=":material/download:"
        )


def sidebar():
    """Barra lateral con información y configuración."""
    with st.sidebar:
        st.markdown("### Laboratorio")
        st.caption("Frankenstein Lingua · exploración interespecie")

        st.subheader("Base de conocimiento")
        try:
            from agent.tools import cargar_patrones
            num_patrones = len(cargar_patrones())
            st.caption(f"{num_patrones} patrones científicos disponibles")
        except Exception as error:
            st.warning(f"No se pudo cargar la base de patrones: {error}")

        st.subheader("Configuración")
        modo_actual = st.session_state.get('provider', 'demo')
        st.markdown(f"**Proveedor:** {modo_actual.upper()}")

        if modo_actual == 'demo':
            st.caption("Configura una API key en `.env` para habilitar un proveedor de IA.")

        with st.expander("Acerca de este proyecto"):
            st.write(
                "Herramienta educativa y creativa. Sus interpretaciones no son "
                "traducciones literales ni sustituyen el asesoramiento profesional."
            )
        st.caption("Versión 1.0.0 MVP")


def main():
    """Función principal de la aplicación."""
    inicializar_sesion()
    
    mostrar_header()
    sidebar()
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs([
        ":material/biotech: Traducción simple",
        ":material/hub: Modo Frankenstein",
        ":material/play_circle: Ejemplos",
        ":material/history: Historial"
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
