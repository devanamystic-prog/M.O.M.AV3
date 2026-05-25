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

# ==================== EXIBIÇÃO BONITA + BOTÃO COPIAR ====================
def exibir_analise(resultado: MomaResponse):
    st.success("✅ Auditoria concluída com sucesso!")
    
    st.markdown('<h3 style="color:#4CAF50;">📋 Resumo</h3>', unsafe_allow_html=True)
    st.markdown(f"**{resultado.veredito_resumo}**")
    st.divider()
    
    st.markdown('<h3 style="color:#2196F3;">✅ Fatos principais</h3>', unsafe_allow_html=True)
    for fato in resultado.analise_detalhada.fatos:
        st.markdown(f"• {fato}")
    st.divider()
    
    st.markdown('<h3 style="color:#9C27B0;">🎯 Técnicas de persuasão</h3>', unsafe_allow_html=True)
    for tec in resultado.analise_detalhada.tecnicas_persuasao:
        st.markdown(f"**{tec.tecnica}**")
        st.markdown(f"Exemplo: {tec.exemplo}")
        st.markdown(f"Efeito: {tec.efeito}")
        st.divider()
    
    st.markdown('<h3 style="color:#FF9800;">⚠️ O que está faltando</h3>', unsafe_allow_html=True)
    for lacuna in resultado.analise_detalhada.lacunas:
        st.markdown(f"• {lacuna}")
    st.divider()
    
    st.markdown('<h3 style="color:#E91E63;">❤️ Aspectos emocionais</h3>', unsafe_allow_html=True)
    for emo in resultado.analise_detalhada.aspectos_emocionais:
        st.markdown(f"• {emo}")
    st.divider()
    
    st.markdown('<h3 style="color:#00BCD4;">👤 Quem fala e intenção</h3>', unsafe_allow_html=True)
    st.markdown(f"**Agente e alvo:** {resultado.analise_detalhada.agente_e_alvo}")
    st.markdown(f"**Intenção real:** {resultado.analise_detalhada.intencao}")
    st.markdown(f"**Outro lado:** {resultado.analise_detalhada.outro_lado}")
    st.divider()
    
    st.markdown('<h3 style="color:#2E7D32;">📝 Versão mais equilibrada</h3>', unsafe_allow_html=True)
    st.markdown(resultado.analise_detalhada.versao_neutra)
    st.divider()
    
    st.markdown('<h3 style="color:#FF5722;">🔍 Minha justificativa</h3>', unsafe_allow_html=True)
    st.markdown(resultado.analise_detalhada.justificativa)
    
    st.markdown('<h3 style="color:#4CAF50;">🏁 Diagnóstico final</h3>', unsafe_allow_html=True)
    st.markdown(f"**{resultado.diagnostico_final}**")

    # Botão de copiar
    st.divider()
    if st.button("📋 Copiar relatório completo", type="primary", use_container_width=True):
        texto_copia = f"""🧠 M.O.M.A. - Análise Completa

📋 Resumo:
{resultado.veredito_resumo}

✅ Fatos principais:
""" + "\n• ".join(resultado.analise_detalhada.fatos) + f"""

🎯 Técnicas de persuasão:
""" + "\n".join([f"• {t.tecnica}\n  Exemplo: {t.exemplo}\n  Efeito: {t.efeito}" for t in resultado.analise_detalhada.tecnicas_persuasao]) + f"""

⚠️ O que está faltando:
""" + "\n• ".join(resultado.analise_detalhada.lacunas) + f"""

❤️ Aspectos emocionais:
""" + "\n• ".join(resultado.analise_detalhada.aspectos_emocionais) + f"""

👤 Agente e alvo: {resultado.analise_detalhada.agente_e_alvo}
Intenção real: {resultado.analise_detalhada.intencao}
Outro lado: {resultado.analise_detalhada.outro_lado}

📝 Versão equilibrada:
{resultado.analise_detalhada.versao_neutra}

🔍 Justificativa:
{resultado.analise_detalhada.justificativa}

🏁 Diagnóstico final:
{resultado.diagnostico_final}
"""
        st.code(texto_copia, language=None)
        st.success("✅ Relatório copiado! Toque longo no texto acima e copie.")

# ==================== CONFIGURAÇÃO DO APP ====================
st.set_page_config(page_title="M.O.M.A.", page_icon="🧠", layout="centered")

try:
    api_key =






    

  

  
