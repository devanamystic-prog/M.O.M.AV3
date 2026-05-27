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
    st.markdown(f"**Outro lado da história:** {resultado.analise_detalhada.outro_lado}")
    st.divider()
    
    st.markdown('<h3 style="color:#2E7D32;">📝 Versão mais equilibrada</h3>', unsafe_allow_html=True)
    st.markdown(resultado.analise_detalhada.versao_neutra)
    st.divider()
    
    st.markdown('<h3 style="color:#FF5722;">🔍 Justificativa</h3>', unsafe_allow_html=True)
    st.markdown(resultado.analise_detalhada.justificativa)
    
    st.markdown('<h3 style="color:#4CAF50;">🏁 Diagnóstico final</h3>', unsafe_allow_html=True)
    st.markdown(f"**{resultado.diagnostico_final}**")

# ==================== CONFIGURAÇÃO ====================
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 0.0,
        "top_p": 0.95,
        "response_mime_type": "application/json"
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",   # ← Mudança aqui (era o problema)
        system_instruction=MOMA_PROMPT,
        generation_config=generation_config
    )
except Exception as e:
    st.error(f"Erro ao configurar API: {e}")
    st.stop()

# ==================== INTERFACE ====================
st.image("logo.PNG", width=300)
st.title("🧠 M.O.M.A.")
st.markdown("*Media Objectivity & Manipulation Auditor*")
st.caption("Análise clara e honesta")

opcao = st.radio("Tipo de entrada:", ["Texto", "Imagem (impressão)"], horizontal=True)

if opcao == "Texto":
    entrada = st.text_area("Cole o texto para auditoria aqui:", height=300, placeholder="Cole aqui a matéria...")
    if st.button("🧠 Auditar Texto", type="primary"):
        if entrada.strip():
            with st.spinner("Analisando..."):
                try:
                    response = model.generate_content(entrada)
                    resultado = validar_json_pydantic(response.text)
                    exibir_analise(resultado)
                except Exception as e:
                    if "quota" in str(e).lower() or "limit" in str(e).lower() or "429" in str(e):
                        st.error("🎟️ Hoje o limite de análises de texto foi atingido.\nUse Imagem ou volte amanhã!")
                    else:
                        st.error(f"Erro ao processar: {e}")
        else:
            st.warning("Insira um texto para analisar.")

else:
    arquivo = st.file_uploader("Envie um print ou imagem:", type=["png", "jpg", "jpeg", "webp"])
    if st.button("🧠 Auditar Imagem", type="primary"):
        if arquivo:
            with st.spinner("Analisando imagem..."):
                try:
                    img = Image.open(arquivo)
                    st.image(img, caption="Imagem enviada", use_column_width=True)

                    prompt_imagem = "Faça uma auditoria completa desta imagem seguindo exatamente o formato JSON do protocolo M.O.M.A."

                    response = model.generate_content([prompt_imagem, img])
                    resultado = validar_json_pydantic(response.text)
                    exibir_analise(resultado)
                except Exception as e:
                    if "quota" in str(e).lower() or "limit" in str(e).lower() or "429" in str(e):
                        st.error("🎟️ Hoje o limite de imagens foi atingido.\nUse Texto ou volte amanhã!")
                    else:
                        st.error(f"Erro na análise da imagem: {e}")
        else:
            st.warning("Envie uma imagem para analisar.")

if st.button("🔄 Limpar tudo"):
    st.rerun()
