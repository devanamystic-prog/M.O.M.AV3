import streamlit as st
import google.generativeai as genai
from PIL import Image
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
Você é o M.O.M.A., auditor honesto e fácil de entender.

Responda **APENAS** com um JSON válido, sem nenhuma explicação, sem ```json, sem texto antes ou depois do JSON.

Use exatamente este formato:
{
  "indice_distorcao": 0,
  "veredito_resumo": "resumo curto e direto",
  "analise_detalhada": {
    "fatos": ["fato 1", "fato 2"],
    "tecnicas_persuasao": [{"tecnica": "...", "exemplo": "...", "efeito": "..."}],
    "lacunas": ["..."],
    "aspectos_emocionais": ["..."],
    "agente_e_alvo": "...",
    "intencao": "...",
    "outro_lado": "...",
    "versao_neutra": "...",
    "justificativa": "..."
  },
  "diagnostico_final": "conclusão clara em um parágrafo"
}
"""

# ==================== VALIDAÇÃO ====================
def validar_json_pydantic(texto_resposta: str) -> MomaResponse:
    texto = texto_resposta.strip()
    match = re.search(r'\{[\s\S]*\}', texto)
    if not match:
        raise ValueError("Não encontrei JSON na resposta.")
    json_str = match.group(0)
    json_str = re.sub(r'^```(?:json)?\s*|\s*```$', '', json_str, flags=re.MULTILINE | re.IGNORECASE)
    return MomaResponse.model_validate_json(json_str)

# ==================== EXIBIÇÃO BONITA + ÍNDICE ====================
def exibir_analise(resultado: MomaResponse):
    indice = max(0, min(100, resultado.indice_distorcao))
    
    if indice <= 30:
        cor = "🟢"
        nivel = "Baixa distorção"
    elif indice <= 70:
        cor = "🟡"
        nivel = "Distorção moderada"
    else:
        cor = "🔴"
        nivel = "Alta distorção"

    st.markdown(f"""
## 👁️ Índice Narrativo

# {cor} {indice}/100

### {nivel}
""")
    st.divider()

    st.success("✅ Auditoria concluída com sucesso!")
    
    st.markdown('<h3 style="color:#4CAF50;">📋 Resumo</h3>', unsafe_allow_html=True)
    st.markdown(f"**{resultado.veredito_resumo}**")
    st.divider()
    
    st.markdown('<h3 style="color:#2196F3;">✅ Fatos principais</h3>', unsafe_allow_html=True)
    for fato in resultado.analise_detalhada.fatos:
        st.markdown(f"• {fato}")
    st.divider()
    
    st.markdown('<h3 style="color:#9C
