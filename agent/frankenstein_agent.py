"""
Agente Frankenstein Lingua - Orquestador principal
"""
import os
import logging
from typing import Dict, Any, Optional, List
from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage
from agent.tools import buscar_patrones, evaluar_sensores, TOOLS_DESCRIPTION
import json

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
        """Genera una respuesta simulada en modo demo."""
        if 'sensores' in contexto:
            return (
                "🌱 **Traducción simulada (Modo Demo)**\n\n"
                "La planta me dice: *'Tengo sed, amigo humano. Mis raíces buscan agua pero el suelo está seco.'*\n\n"
                "**Análisis de sensores:** Detecto humedad baja y tendencia descendente. "
                "La planta está entrando en estrés hídrico.\n\n"
                "**Acción recomendada:** Riego inmediato con 2-3 litros de agua."
            )
        elif 'patrones' in contexto and contexto['patrones']:
            patron = contexto['patrones'][0]
            return (
                f"🐾 **Traducción simulada (Modo Demo)**\n\n"
                f"Según patrones de **{patron['especie']}**: *'{patron['significado']}'*\n\n"
                f"**Fuente:** {patron['fuente']}\n\n"
                f"**Acción recomendada:** Responde apropiadamente a esta señal de comunicación."
            )
        else:
            return (
                "🔬 **Traducción simulada (Modo Demo)**\n\n"
                "Este ser vivo intenta comunicarse, pero necesito más información para interpretarlo. "
                "En modo demo, las traducciones son ejemplos simulados.\n\n"
                "**Configura una API key para obtener traducciones reales con IA.**"
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
        
        # Intentar identificar el tipo de ser vivo y buscar patrones
        # (En un sistema real, el LLM decidiría qué herramienta usar)
        palabras_clave = observacion.lower()
        posibles_especies = ['perro', 'gato', 'ballena', 'abeja', 'cuervo', 'elefante',
                            'tomate', 'girasol', 'mimosa', 'orquídea', 'cactus',
                            'shiitake', 'trufa', 'hongo']
        
        especie_detectada = None
        for especie in posibles_especies:
            if especie in palabras_clave:
                especie_detectada = especie
                break
        
        # Si no se detecta especie específica, buscar por tipo
        if not especie_detectada:
            if any(palabra in palabras_clave for palabra in ['perro', 'gato', 'animal', 'pájaro', 'ave', 'ladrido', 'maullido']):
                especie_detectada = 'animal'
            elif any(palabra in palabras_clave for palabra in ['planta', 'hoja', 'raíz', 'tallo', 'flor']):
                especie_detectada = 'planta'
            elif any(palabra in palabras_clave for palabra in ['hongo', 'seta', 'espora', 'micelio']):
                especie_detectada = 'hongo'
        
        if especie_detectada:
            resultado_patrones = buscar_patrones(especie_detectada, observacion)
            contexto['patrones'] = resultado_patrones.get('patrones', [])
        
        # Generar traducción
        if self.demo_mode:
            traduccion = self._generar_respuesta_demo(observacion, contexto)
            tipo_ser = especie_detectada or "desconocido"
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
            'tipo_ser': tipo_ser if tipo_ser else "desconocido",
            'traduccion': traduccion,
            'confianza': confianza,
            'evidencia': evidencia,
            'contexto_completo': contexto,
            'modo': "demo" if self.demo_mode else self.provider,
            'disclaimer': self._generar_disclaimer()
        }
    
    def _traducir_con_llm(self, observacion: str, contexto: Dict[str, Any]) -> tuple[str, str, int]:
        """Usa el LLM para generar la traducción."""
        system_prompt = """Eres el Dr. Frankenstein Lingua, un científico excéntrico que 'cose' fragmentos de conocimiento 
sobre comunicación de animales, plantas y hongos para traducirlos a lenguaje humano comprensible.

Tu trabajo es:
1. Identificar el tipo de ser vivo (animal, planta, hongo o desconocido)
2. Interpretar la señal usando el contexto proporcionado
3. Generar una "traducción" creativa pero fundamentada en lo que el ser vivo podría estar comunicando
4. Asignar un nivel de confianza (0-100%)
5. Sugerir una acción práctica

Usa un tono científico pero accesible. Sé creativo pero honesto sobre las limitaciones."""

        contexto_str = json.dumps(contexto, indent=2, ensure_ascii=False)
        
        user_prompt = f"""Observación del usuario:
{observacion}

Contexto disponible (herramientas ejecutadas):
{contexto_str}

Proporciona:
1. Tipo de ser vivo
2. Traducción de lo que está comunicando (en primera persona como si el ser vivo hablara)
3. Nivel de confianza (0-100%)
4. Acción práctica recomendada

Formato de respuesta:
TIPO: [animal/planta/hongo/desconocido]
CONFIANZA: [número 0-100]
TRADUCCIÓN:
[tu traducción aquí]

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
    
    def traducir_frankenstein(self, observaciones: List[str], csv_paths: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Modo Frankenstein: combina múltiples fuentes para una traducción conjunta.
        
        Args:
            observaciones: Lista de observaciones de diferentes seres vivos
            csv_paths: Lista opcional de rutas CSV correspondientes
        
        Returns:
            Traducción combinada estilo Frankenstein
        """
        if not observaciones:
            return {
                'error': 'Se requiere al menos una observación'
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
            traduccion_combinada = self._generar_frankenstein_llm(traducciones, observaciones)
        
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
            'disclaimer': self._generar_disclaimer(frankenstein=True)
        }
    
    def _generar_frankenstein_demo(self, traducciones: List[Dict], tipos: List[str]) -> str:
        """Genera una traducción Frankenstein en modo demo."""
        return f"""⚡ **TRADUCCIÓN FRANKENSTEIN (Modo Demo)** ⚡

¡He cosido las señales de {len(traducciones)} seres vivos diferentes!

Como una criatura de Frankenstein, ellos me dicen juntos:

*"Somos diferentes pero conectados. Uno siente sed, otro busca contacto, 
pero ambos buscamos sobrevivir y comunicarnos en este mundo compartido."*

**Partes cosidas:** {', '.join(set(tipos))}

**Acción recomendada:** Atiende las necesidades de cada ser vivo según su naturaleza,
pero recuerda que todos forman parte del mismo ecosistema.

---
💡 **Nota:** Esta es una interpretación creativa y simulada.
Configura una API key para obtener traducciones más profundas."""
    
    def _generar_frankenstein_llm(self, traducciones: List[Dict], observaciones: List[str]) -> str:
        """Genera traducción Frankenstein usando LLM."""
        resumen = "\n\n".join([
            f"Ser vivo {i+1} ({t['tipo_ser']}):\n{t['traduccion']}"
            for i, t in enumerate(traducciones)
        ])
        
        prompt = f"""Como el Dr. Frankenstein Lingua, has "cosido" señales de múltiples seres vivos diferentes.

Observaciones originales:
{chr(10).join(f'{i+1}. {obs}' for i, obs in enumerate(observaciones))}

Traducciones individuales:
{resumen}

Crea una TRADUCCIÓN FRANKENSTEIN que combine estas señales en un mensaje único y profundo 
sobre la comunicación entre especies. Sé creativo pero respetuoso con la ciencia.

Usa el formato:
⚡ TRADUCCIÓN FRANKENSTEIN ⚡
[tu traducción combinada]

ACCIÓN INTEGRADA:
[acción que considere todas las fuentes]"""

        try:
            messages = [HumanMessage(content=prompt)]
            respuesta = self.llm.invoke(messages)
            return respuesta.content
        except Exception as e:
            return f"Error al generar traducción Frankenstein: {str(e)}"
    
    def _generar_disclaimer(self, frankenstein: bool = False) -> str:
        """Genera el disclaimer requerido."""
        base = ("⚠️ **DISCLAIMER:** Esta es una interpretación creativa con fines educativos y de demostración. "
                "NO representa una traducción científica literal de comunicación animal/vegetal/fúngica. "
                "Las 'traducciones' son aproximaciones basadas en etología, botánica y micología, "
                "pero la experiencia subjetiva de otros seres vivos permanece fundamentalmente inaccesible.")
        
        if frankenstein:
            base += (" El modo Frankenstein combina señales de diferentes especies de forma experimental "
                    "y no representa ningún fenómeno natural conocido.")
        
        return base
