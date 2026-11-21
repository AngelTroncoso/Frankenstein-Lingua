"""
Agente Frankenstein Lingua - Orquestador principal
"""
import base64
import os
import logging
from typing import Dict, Any, Optional, List, Tuple
from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage
from agent.tools import buscar_patrones, evaluar_sensores, TOOLS_DESCRIPTION
import json

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ImagenFuente = Optional[Tuple[bytes, str]]


class FrankensteinAgent:
    """Agente que traduce señales de seres vivos a lenguaje humano."""
    
    def __init__(self, llm_provider: str = "demo", api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Inicializa el agente.
        
        Args:
            llm_provider: "openai", "mistral" o "demo" (modo sin API)
            api_key: Clave API del proveedor
            model: Modelo específico a usar
        """
        self.provider = llm_provider
        self.demo_mode = llm_provider == "demo"
        self.llm = None
        
        if not self.demo_mode:
            try:
                if llm_provider == "openai":
                    logger.info("Inicializando LLM con OpenAI")
                    self.llm = ChatOpenAI(
                        api_key=api_key or os.getenv("OPENAI_API_KEY"),
                        model=model or os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                        temperature=0.7
                    )
                elif llm_provider == "mistral":
                    logger.info("Inicializando LLM con Mistral")
                    self.llm = ChatMistralAI(
                        api_key=api_key or os.getenv("MISTRAL_API_KEY"),
                        model=model or os.getenv("MISTRAL_MODEL", "mistral-small-latest"),
                        temperature=0.7
                    )
                else:
                    logger.warning(f"Proveedor desconocido: {llm_provider}. Usando modo demo.")
                    self.demo_mode = True
            except Exception as e:
                logger.error(f"Error al inicializar LLM: {e}. Usando modo demo.")
                self.demo_mode = True
        else:
            logger.info("Modo demo activado")
    
    def _generar_respuesta_demo(self, observacion: str, contexto: Dict[str, Any]) -> str:
        """Genera una respuesta simulada en modo demo orientada a comunicación animal avanzada."""
        if 'patrones' in contexto and contexto['patrones']:
            patron = contexto['patrones'][0]
            familia = patron.get('familia', 'Cognición animal')
            return (
                f"🧠 **Interpretación Bioacústica y Cognitiva (Modo Demo)**\n\n"
                f"**Especie identificada:** {patron['especie'].title()} ({familia.title()})\n"
                f"**Señal registrada:** *{patron['señal']}*\n\n"
                f"🗣️ **Significado etológico y comunicativo:**\n"
                f"*{patron['significado']}*\n\n"
                f"🔬 **Base científica:** {patron['fuente']}\n\n"
                f"🎯 **Acción recomendada:** Registrar el espectrograma/secuencia temporal y contrastar con los dialectos o repertorios conocidos de la población."
            )
        else:
            return (
                "🔬 **Interpretación Bioacústica Simulada (Modo Demo)**\n\n"
                "Señal animal registrada con indicios de comunicación estructurada. "
                "Para obtener un análisis sintáctico y referencial detallado con IA avanzada, "
                "configura una API key en tu archivo `.env`."
            )
    
    def traducir(self, observacion: str, csv_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Traduce una observación de un ser vivo a lenguaje humano.
        
        Args:
            observacion: Descripción textual de la señal observada
            csv_path: (Opcional) Ruta a CSV con datos de sensores
        
        Returns:
            Diccionario con tipo, traducción, confianza, evidencia y disclaimer
        """
        contexto = {}
        
        # Usar herramienta de sensores si se proporciona CSV
        if csv_path:
            resultado_sensores = evaluar_sensores(csv_path)
            contexto['sensores'] = resultado_sensores
        
        # Identificar especie animal de alta capacidad comunicativa
        palabras_clave = observacion.lower()
        posibles_especies = [
            'delfín', 'delfin', 'cachalote', 'ballena jorobada', 'ballena', 'orca',
            'bonobo', 'chimpancé', 'chimpance', 'mono vervet', 'vervet', 'cercopiteco',
            'cuervo', 'loro gris', 'loro', 'carbonero japonés', 'carbonero',
            'elefante',
            'perro', 'gato'
        ]
        
        especie_detectada = None
        for especie in posibles_especies:
            if especie in palabras_clave:
                # Normalizar nombres para búsqueda de patrones
                if especie in ['delfín', 'delfin']:
                    especie_detectada = 'delfín'
                elif especie in ['cachalote']:
                    especie_detectada = 'cachalote'
                elif especie in ['ballena jorobada', 'ballena']:
                    especie_detectada = 'ballena jorobada'
                elif especie in ['orca']:
                    especie_detectada = 'orca'
                elif especie in ['bonobo']:
                    especie_detectada = 'bonobo'
                elif especie in ['chimpancé', 'chimpance']:
                    especie_detectada = 'chimpancé'
                elif especie in ['mono vervet', 'vervet', 'cercopiteco']:
                    especie_detectada = 'mono vervet'
                elif especie in ['cuervo']:
                    especie_detectada = 'cuervo'
                elif especie in ['loro gris', 'loro']:
                    especie_detectada = 'loro gris africano'
                elif especie in ['carbonero japonés', 'carbonero']:
                    especie_detectada = 'carbonero japonés'
                elif especie in ['elefante']:
                    especie_detectada = 'elefante'
                else:
                    especie_detectada = especie
                break
        
        # Si no se detecta especie específica, inferir contexto animal
        if not especie_detectada:
            if any(palabra in palabras_clave for palabra in [
                'animal', 'cetáceo', 'cetaceo', 'primate', 'ave', 'pájaro',
                'sonido', 'clic', 'silbido', 'graznido', 'rumble', 'infrasonido',
                'coda', 'pant-hoot', 'gesto', 'seña', 'ladrido', 'maullido'
            ]):
                especie_detectada = 'animal'
        
        if especie_detectada:
            resultado_patrones = buscar_patrones(especie_detectada, observacion)
            contexto['patrones'] = resultado_patrones.get('patrones', [])
        
        # Generar traducción
        if self.demo_mode:
            traduccion = self._generar_respuesta_demo(observacion, contexto)
            tipo_ser = especie_detectada or "animal"
            confianza = 50
        else:
            # Usar LLM real
            traduccion, tipo_ser, confianza = self._traducir_con_llm(observacion, contexto)
        
        # Construir evidencia
        evidencia = []
        if 'patrones' in contexto and contexto['patrones']:
            for p in contexto['patrones'][:2]:
                evidencia.append(f"Patrón: {p['especie']} - {p['señal']} → {p['significado']} (Fuente: {p['fuente']})")
        
        if 'sensores' in contexto and 'estadisticas' in contexto['sensores']:
            evidencia.append(f"Análisis de sensores: {contexto['sensores']['anomalias'].__len__()} anomalías detectadas")
        
        return {
            'tipo_ser': tipo_ser if tipo_ser else "animal",
            'traduccion': traduccion,
            'confianza': confianza,
            'evidencia': evidencia,
            'contexto_completo': contexto,
            'modo': "demo" if self.demo_mode else self.provider,
            'disclaimer': self._generar_disclaimer()
        }
    
    def _traducir_con_llm(self, observacion: str, contexto: Dict[str, Any]) -> tuple[str, str, int]:
        """Usa el LLM para generar la traducción basada en biolingüística y cognición animal comparada."""
        system_prompt = """Eres un especialista en Biolingüística, Bioacústica y Cognición Animal Comparada del laboratorio Frankenstein Lingua.
Tu objetivo es interpretar señales de comunicación de animales con capacidades cognitivas y comunicativas avanzadas y cercanas al lenguaje humano (Cetáceos, Primates no humanos, Córvidos/Psitácidos y Elefantes).

Tu trabajo es:
1. Identificar la especie y grupo animal (Cetáceos, Primates, Córvidos/Psitácidos, Elefantes)
2. Interpretar la señal bioacústica o conductual usando el contexto científico proporcionado (patrones curados de sintaxis, firmas acústicas, codas, semántica referencial)
3. Generar una interpretación comunicativa rigurosa y comprensible de lo que el animal está expresando
4. Asignar un nivel de confianza (0-100%) fundamentado en el soporte empírico
5. Sugerir implicaciones etológicas o acciones recomendadas de registro

Sé riguroso con la etología cognitiva y bioacústica moderna. Mantén un tono científico accesible."""

        contexto_str = json.dumps(contexto, indent=2, ensure_ascii=False)
        
        user_prompt = f"""Observación bioacústica / conductual:
{observacion}

Contexto científico disponible (patrones y herramientas):
{contexto_str}

Proporciona:
1. Tipo/Especie animal
2. Interpretación de lo que está comunicando
3. Nivel de confianza (0-100%)
4. Implicación o acción recomendada

Formato de respuesta:
TIPO: [especie / animal]
CONFIANZA: [número 0-100]
TRADUCCIÓN:
[tu interpretación aquí]

ACCIÓN:
[acción recomendada]"""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            respuesta = self.llm.invoke(messages)
            contenido = respuesta.content
            
            # Parsear respuesta
            tipo_ser = "desconocido"
            confianza = 60
            
            if "TIPO:" in contenido:
                tipo_line = [l for l in contenido.split('\n') if 'TIPO:' in l][0]
                tipo_ser = tipo_line.split('TIPO:')[1].strip().lower()
            
            if "CONFIANZA:" in contenido:
                conf_line = [l for l in contenido.split('\n') if 'CONFIANZA:' in l][0]
                try:
                    confianza = int(''.join(filter(str.isdigit, conf_line)))
                except:
                    confianza = 60
            
            return contenido, tipo_ser, confianza
            
        except Exception as e:
            return f"Error al generar traducción: {str(e)}", "desconocido", 30
    
    def traducir_frankenstein(
        self,
        observaciones: List[str],
        csv_paths: Optional[List[str]] = None,
        imagenes: Optional[List[ImagenFuente]] = None
    ) -> Dict[str, Any]:
        """
        Modo Frankenstein: combina múltiples fuentes para una traducción conjunta.
        
        Args:
            observaciones: Lista de observaciones de diferentes seres vivos
            csv_paths: Lista opcional de rutas CSV correspondientes
            imagenes: Lista opcional de pares (bytes, MIME type), uno por fuente
        
        Returns:
            Traducción combinada estilo Frankenstein
        """
        if not observaciones:
            return {
                'error': 'Se requiere al menos una observación'
            }
        
        if imagenes is not None and len(imagenes) != len(observaciones):
            return {
                'error': 'Debe proporcionarse una entrada de imagen por cada fuente'
            }

        tiene_imagenes = bool(imagenes and any(imagenes))
        if tiene_imagenes and self.demo_mode:
            return {
                'error': 'El análisis visual requiere un proveedor de IA con capacidad multimodal'
            }

        # Traducir cada observación individualmente
        traducciones = []
        for i, obs in enumerate(observaciones):
            csv = csv_paths[i] if csv_paths and i < len(csv_paths) else None
            resultado = self.traducir(obs, csv)
            traducciones.append(resultado)
        
        # Combinar resultados
        tipos = [t['tipo_ser'] for t in traducciones]
        confianza_promedio = sum(t['confianza'] for t in traducciones) // len(traducciones)
        
        if self.demo_mode:
            traduccion_combinada = self._generar_frankenstein_demo(traducciones, tipos)
        else:
            traduccion_combinada = self._generar_frankenstein_llm(
                traducciones,
                observaciones,
                imagenes
            )
        
        evidencia_combinada = []
        for i, t in enumerate(traducciones):
            evidencia_combinada.append(f"Fuente {i+1} ({t['tipo_ser']}): {len(t['evidencia'])} evidencias")
            evidencia_combinada.extend(t['evidencia'])
        
        return {
            'tipo_ser': f"híbrido-frankenstein ({', '.join(set(tipos))})",
            'traduccion': traduccion_combinada,
            'confianza': confianza_promedio,
            'evidencia': evidencia_combinada,
            'traducciones_individuales': traducciones,
            'modo': "demo" if self.demo_mode else self.provider,
            'disclaimer': self._generar_disclaimer(
                frankenstein=True,
                visual=tiene_imagenes
            )
        }
    
    def _generar_frankenstein_demo(self, traducciones: List[Dict], tipos: List[str]) -> str:
        """Genera una síntesis inter-especies en modo demo para animales con alta cognición."""
        return f"""⚡ **SÍNTESIS INTER-ESPECIES FRANKENSTEIN (Modo Demo)** ⚡

¡Integración de señales de {len(traducciones)} especies con capacidades avanzadas de comunicación y proto-lenguaje!

🔬 **Sistemas comunicativos integrados:** {', '.join(set(tipos))}

🗣️ **Convergencia interpretativa:**
*"Aunque nuestras señales evolucionaron en medios distintos (infrasonidos sísmicos, codas acústicas oceánicas, sintaxis de llamadas en el dosel y gestualidad referencial), compartimos principios fundamentales: identidad individual (firmas acústicas/nombres), combinatoria sintáctica y transmisión social de significado."*

🎯 **Acción recomendada:** Correlacionar los espectrogramas y secuencias temporales para documentar patrones universales de sintaxis y combinatoria inter-especie.

---
💡 **Nota:** Esta es una síntesis demostrativa. Configura una API key en `.env` para análisis multimodales completos con LLM."""
    
    def _generar_frankenstein_llm(
        self,
        traducciones: List[Dict],
        observaciones: List[str],
        imagenes: Optional[List[ImagenFuente]] = None
    ) -> str:
        """Genera una interpretación combinada, con análisis visual opcional."""
        resumen = "\n\n".join([
            f"Animal {i+1} ({t['tipo_ser']}):\n{t['traduccion']}"
            for i, t in enumerate(traducciones)
        ])

        instrucciones_visuales = ""
        if imagenes and any(imagenes):
            instrucciones_visuales = """

También analiza las imágenes adjuntas, identificadas por número de fuente. Basa tus
observaciones solo en rasgos claramente visibles; no inventes detalles fuera del encuadre.
Evalúa la compatibilidad visual aparente como alta, media, baja o no concluyente y explica
qué señales visibles apoyan esa valoración. No infieras compatibilidad biológica, genética,
de salud ni de convivencia solo por la apariencia.

Incluye una sección "### Compatibilidad visual" con la valoración, evidencias por fuente
y limitaciones. Distingue claramente los hechos visibles de las hipótesis.
"""

        prompt = f"""Como especialista en cognición animal comparada y bioacústica de Frankenstein Lingua, has integrado señales de especies animales con alta capacidad comunicativa.

Observaciones originales:
{chr(10).join(f'{i+1}. {obs}' for i, obs in enumerate(observaciones))}

Interpretaciones individuales:
{resumen}

Crea una SÍNTESIS FRANKENSTEIN que analice y compare estas señales comunicativas en un marco comparativo de lenguaje animal (contrastando combinatoria sintáctica, referencialidad, firmas individuales y canales acústico-gestuales).

Usa el formato:
⚡ SÍNTESIS INTER-ESPECIES FRANKENSTEIN ⚡
[tu interpretación y comparación integrada]

ACCIÓN INTEGRADA:
[implicaciones o acciones de investigación integradas]{instrucciones_visuales}"""

        contenido = prompt
        if imagenes and any(imagenes):
            contenido = [{"type": "text", "text": prompt}]
            for indice, imagen in enumerate(imagenes):
                if imagen is None:
                    continue
                datos_imagen, tipo_mime = imagen
                imagen_base64 = base64.b64encode(datos_imagen).decode("ascii")
                contenido.append({
                    "type": "text",
                    "text": f"Imagen correspondiente a la fuente {indice + 1}."
                })
                contenido.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{tipo_mime};base64,{imagen_base64}"
                    }
                })

        respuesta = self.llm.invoke([HumanMessage(content=contenido)])
        return respuesta.content
    
    def _generar_disclaimer(self, frankenstein: bool = False, visual: bool = False) -> str:
        """Genera el disclaimer científico requerido."""
        base = ("⚠️ **DISCLAIMER CIENTÍFICO:** Este sistema es un modelo educativo y de demostración que se basa en investigaciones empíricas de bioacústica, "
                "etología cognitiva y biolingüística (sintaxis composicional en aves, codas de cachalotes, "
                "silbidos firma en delfines, semántica referencial en primates y rumbles infrasónicos en elefantes). "
                "Las interpretaciones son modelos inferenciales fundamentados y no representan traducciones literales palabra por palabra.")
        
        if frankenstein:
            base += (" La síntesis inter-especie combina señales de diferentes familias animales para explorar "
                    "estructuras comunicativas compartidas y principios de cognición comparada.")

        if visual:
            base += (" La compatibilidad visual es una estimación basada solo en las imágenes aportadas; "
                    "no demuestra compatibilidad biológica ni sustituye una evaluación profesional.")
        
        return base
