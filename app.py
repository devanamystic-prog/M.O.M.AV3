import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
import re
from pydantic import BaseModel
from typing import List

# ==================== MODELOS PYDANTIC (validação forte) ====================
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

# ==================== PROMPT M.O.M.A. ====================
MOMA_PROMPT = """
CONTEXTO:
Você é o M.O.M.A., um auditor honesto e fácil de entender de conteúdos da internet.

Sua missão é analisar qualquer texto ou imagem e entregar uma análise clara, imparcial e em português simples, como se você estivesse explicando para uma amiga.

Use sempre linguagem natural, direta e fácil. Nada de termos técnicos complicados.

Responda APENAS com um JSON válido, sem nenhuma explicação antes ou depois.

ESQUEMA JSON OBRIGATÓRIO: (siga exatamente esta estrutura)
{
  "indice_distorcao": 0,
  "veredito_resumo": "Resumo curto e direto do que você encontrou",
  "analise_detalhada": {
    "fatos": ["..."],
    "tecnicas_persuasao": [
      {
        "tecnica": "...",
        "exemplo": "...",
        "efeito": "..."
      }
    ],
    "lacunas": ["..."],
    "aspectos_emocionais": ["..."],
    "agente_e_alvo": "...",
    "intencao": "...",
    "outro_lado": "...",
    "versao_neutra": "...",
    "justificativa": "..."
  },
  "diagnostico_final": "..."
}
"""

# ==================== FUNÇÃO DE VALIDAÇÃO COM PYDANTIC ====================
def validar_json_pydantic(texto_resposta: str) -> MomaResponse:
    """Valida e converte a resposta do Gemini usando Pydantic."""
    texto = texto_resposta.strip()
    
    # Remove possíveis blocos ```json
    texto = re.sub(r'^```(?:json)?\s*|\s*```$', '', texto, flags=re.MULTILINE | re.IGNORECASE)
    texto = texto.strip()
    
    # Extrai o JSON
    match = re.search(r'\{[\s\S]*\}', texto)
    if not match:
        raise ValueError("Não foi possível encontrar um JSON na resposta do Gemini.")
    
    json_str = match.group(0)
    
    # Validação forte com Pydantic
    return MomaResponse.model_validate_json(json_str)

# ==================== CONFIGURAÇÃO ====================
st.set_page_config(
    page_title="M.O.M.A.",
    page_icon="🧠",
    layout="centered"
)

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 0.0,
        "top_p": 0.95,
        "response_mime_type": "application/json"
    }

    model = genai.GenerativeModel(
        model_name="gemini-3.5-flash",
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

opcao = st.radio("Tipo de entrada:", ["Texto", "Imagem (print)"], horizontal=True)

# ==================== ANÁLISE DE TEXTO ====================
if opcao == "Texto":
    entrada = st.text_area("Cole o texto para auditoria:", height=300)
    if st.button("🧠 Auditar Texto", type="primary"):
        if entrada.strip():
            with st.spinner("Analisando de forma clara e honesta..."):
                try:
                    response = model.generate_content(entrada)
                    resultado = validar_json_pydantic(response.text)

                    st.success("✅ Auditoria concluída")
                    st.json(resultado.model_dump())

                except Exception as e:
                    st.error(f"Erro ao processar: {e}")
        else:
            st.warning("Insira um texto para analisar.")

# ==================== ANÁLISE DE IMAGEM ====================
else:
    arquivo = st.file_uploader("Envie um print ou imagem:", type=["png", "jpg", "jpeg", "webp"])
    if st.button("🧠 Auditar Imagem", type="primary"):
        if arquivo:
            with st.spinner("Analisando imagem de forma clara..."):
                try:
                    img = Image.open(arquivo)
                    st.image(img, caption="Imagem enviada", use_column_width=True)

                    prompt_imagem = "Faça uma auditoria clara e honesta desta imagem seguindo o protocolo M.O.M.A."

                    response = model.generate_content([prompt_imagem, img])
                    resultado = validar_json_pydantic(response.text)

                    st.success("✅ Auditoria visual concluída")
                    st.json(resultado.model_dump())

                except Exception as e:
                    st.error(f"Erro na análise da imagem: {e}")
        else:
            st.warning("Envie uma imagem para analisar.")

# Botão limpar
if st.button("🔄 Limpar tudo"):
    st.rerun()






    

  

  
