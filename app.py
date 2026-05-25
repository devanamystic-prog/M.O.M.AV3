import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
import re
from pydantic import BaseModel
from typing import List

# ==================== MODELOS PYDANTIC ====================
class TecnicaPersuasao(BaseModel):
    tecnica: str
    exemplo: str
    efeito: str

class AnaliseDetalhada(BaseModel):
    fatos: List[str]
    tecnicas_persuasao: List[TecnicaPersuasao]
    lacunas: List[str]
    aspectos_emocionais: List[str]
    agente_e_alvo: str
    intencao: str
    outro_lado: str
    versao_neutra: str
    justificativa: str

class MomaResponse(BaseModel):
    indice_distorcao: int
    veredito_resumo: str
    analise_detalhada: AnaliseDetalhada
    diagnostico_final: str

# ==================== PROMPT ====================
MOMA_PROMPT = """
CONTEXTO:
Você é o M.O.M.A., um auditor honesto e fácil de entender de conteúdos da internet.

Sua missão é analisar qualquer texto ou imagem e entregar uma análise clara, imparcial e em português simples, como se você estivesse explicando para uma amiga.

Use sempre linguagem natural, direta e fácil. Nada de termos técnicos complicados.

Responda APENAS com um JSON válido, sem nenhuma explicação antes ou depois.
"""

# ==================== VALIDAÇÃO ====================
def validar_json_pydantic(texto_resposta: str) -> MomaResponse:
    texto = texto_resposta.strip()
    texto = re.sub(r'^```(?:json)?\s*|\s*```$', '', texto, flags=re.MULTILINE | re.IGNORECASE)
    texto = texto.strip()
    match = re.search(r'\{[\s\S]*\}', texto)
    if not match:
        raise ValueError("Não foi possível encontrar um JSON na resposta.")
    json_str = match.group(0)
    return MomaResponse.model_validate_json(json_str)

# ==================== EXIBIÇÃO COM ÍCONES, CORES E BOTÃO DE COPIAR ====================
def exibir_analise(resultado: MomaResponse):
    st.success("✅ Auditoria concluída com sucesso!")
    
    # Resumo
    st.markdown('<h3 style="color:#4CAF50;">📋 Resumo</h3>', unsafe_allow_html=True)
    st.markdown(f"**{resultado.veredito_resumo}**")
    st.divider()
    
    # Fatos
    st.markdown('<h3 style="color:#2196F3;">✅ Fatos principais</h3>', unsafe_allow_html=True)
    for fato in resultado.analise_detalhada.fatos:
        st.markdown(f"• {fato}")
    st.divider()
    
    # Técnicas
    st.markdown('<h3 style="color:#9C27B0;">🎯 Técnicas de persuasão</h3>', unsafe_allow_html=True)
    for tec in resultado.analise_detalhada.tecnicas_persuasao:
        st.markdown(f"**{tec.tecnica}**")
        st.markdown(f"Exemplo: {tec.exemplo}")
        st.markdown(f"Efeito: {tec.efeito}")
        st.divider()
    
    # Lacunas
    st.markdown('<h3 style="color:#FF9800;">⚠️ O que está faltando</h3>', unsafe_allow_html=True)
    for lacuna in resultado.analise_detalhada.lacunas:
        st.markdown(f"• {lacuna}")
    st.divider()
    
    # Emocional
    st.markdown('<h3 style="color:#E91E63;">❤️ Aspectos emocionais</h3>', unsafe_allow_html=True)
    for emo in resultado.analise_detalhada.aspectos_emocionais:
        st.markdown(f"• {emo}")
    st.divider()
    
    # Agente + Intenção + Outro lado
    st.markdown('<h3 style="color:#00BCD4;">👤 Quem fala e intenção</h






    

  

  
