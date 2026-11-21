"""
Tests para el agente Frankenstein
"""
import pytest
from types import SimpleNamespace
from agent.frankenstein_agent import FrankensteinAgent


def test_agent_inicializacion_demo():
    """Verifica que el agente se inicialice correctamente en modo demo."""
    agente = FrankensteinAgent(llm_provider="demo")
    assert agente.demo_mode == True
    assert agente.provider == "demo"


def test_traducir_simple_demo():
    """Verifica traducción simple en modo demo."""
    agente = FrankensteinAgent(llm_provider="demo")
    resultado = agente.traducir("Un perro ladrando")
    
    assert 'tipo_ser' in resultado
    assert 'traduccion' in resultado
    assert 'confianza' in resultado
    assert 'evidencia' in resultado
    assert 'disclaimer' in resultado
    assert resultado['modo'] == 'demo'


def test_traducir_frankenstein_demo():
    """Verifica traducción Frankenstein en modo demo."""
    agente = FrankensteinAgent(llm_provider="demo")
    observaciones = [
        "Un perro ladrando",
        "Una planta con hojas caídas"
    ]
    resultado = agente.traducir_frankenstein(observaciones)
    
    assert 'tipo_ser' in resultado
    assert 'frankenstein' in resultado['tipo_ser'].lower() or 'híbrido' in resultado['tipo_ser']
    assert 'traduccion' in resultado
    assert 'traducciones_individuales' in resultado
    assert len(resultado['traducciones_individuales']) == 2


def test_analisis_visual_requiere_proveedor_multimodal():
    """El modo demo debe rechazar imágenes en vez de aparentar analizarlas."""
    agente = FrankensteinAgent(llm_provider="demo")
    resultado = agente.traducir_frankenstein(
        ["Un perro", "Un gato"],
        imagenes=[(b"imagen", "image/jpeg"), None]
    )

    assert 'error' in resultado
    assert "multimodal" in resultado['error']


def test_imagenes_se_envian_asociadas_a_su_fuente():
    """La fusión envía las imágenes al proveedor junto a sus fuentes."""
    class LLMFalso:
        def invoke(self, messages):
            self.messages = getattr(self, "messages", []) + messages
            contenido = messages[0].content
            if isinstance(contenido, list):
                return SimpleNamespace(content="### Compatibilidad visual\nApariencia complementaria.")
            return SimpleNamespace(
                content="TIPO: animal\nCONFIANZA: 75\nTRADUCCIÓN:\nSeñal interpretada."
            )

    agente = FrankensteinAgent(llm_provider="demo")
    agente.demo_mode = False
    agente.provider = "openai"
    agente.llm = LLMFalso()

    resultado = agente.traducir_frankenstein(
        ["Un perro", "Una planta"],
        imagenes=[(b"foto-perro", "image/jpeg"), (b"foto-planta", "image/png")]
    )

    contenido = agente.llm.messages[-1].content
    bloques_imagen = [bloque for bloque in contenido if bloque.get("type") == "image_url"]
    etiquetas_fuente = [
        bloque["text"] for bloque in contenido
        if bloque.get("type") == "text" and bloque["text"].startswith("Imagen correspondiente")
    ]

    assert "Compatibilidad visual" in resultado["traduccion"]
    assert len(bloques_imagen) == 2
    assert "data:image/jpeg;base64,Zm90by1wZXJybw==" == bloques_imagen[0]["image_url"]["url"]
    assert "data:image/png;base64,Zm90by1wbGFudGE=" == bloques_imagen[1]["image_url"]["url"]
    assert etiquetas_fuente == [
        "Imagen correspondiente a la fuente 1.",
        "Imagen correspondiente a la fuente 2."
    ]
    assert "no demuestra compatibilidad biológica" in resultado["disclaimer"]


def test_disclaimer_presente():
    """Verifica que todas las traducciones incluyan disclaimer."""
    agente = FrankensteinAgent(llm_provider="demo")
    resultado = agente.traducir("Un gato ronroneando")
    
    assert 'disclaimer' in resultado
    assert len(resultado['disclaimer']) > 50
    assert 'educativo' in resultado['disclaimer'].lower() or 'demostración' in resultado['disclaimer'].lower()


def test_confianza_rango_valido():
    """Verifica que el nivel de confianza esté en rango válido."""
    agente = FrankensteinAgent(llm_provider="demo")
    resultado = agente.traducir("Un elefante emitiendo infrasonidos")
    
    assert 'confianza' in resultado
    assert 0 <= resultado['confianza'] <= 100


def test_traducir_interespecies_demo():
    """Verifica la transposición inter-especies del router neural."""
    agente = FrankensteinAgent(llm_provider="demo")
    resultado = agente.traducir_interespecies(
        especie_origen="cachalote",
        senal_origen="coda rítmica 1+1+3 de alerta ante orcas",
        especie_destino="delfín"
    )
    
    assert 'especie_origen' in resultado
    assert 'especie_destino' in resultado
    assert 'invariante_semantico' in resultado
    assert 'senal_transpuesta' in resultado
    assert 'canal_receptor' in resultado
    assert 'metricas' in resultado
    assert resultado['inteligibilidad_estimada'] > 50


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
