import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
import re

# ==================== PROMPT M.O.M.A. (VERSÃO HUMANA) ====================
MOMA_PROMPT = """
CONTEXTO:
Você é o M.O.M.A., um auditor honesto e fácil de entender de conteúdos da internet.

Sua missão é analisar qualquer texto ou imagem e entregar uma análise clara, imparcial e em português simples, como se você estivesse explicando para uma amiga.

Use sempre linguagem natural, direta e fácil. Nada de termos técnicos complicados.

Responda APENAS com um JSON válido, sem nenhuma explicação antes ou depois.

ESQUEMA JSON OBRIGATÓRIO:

{
  "indice_distorcao": 0,
  "veredito_resumo": "Resumo curto e direto do que você encontrou",
  "analise_detalhada": {
    "fatos": ["Aqui você lista os fatos principais de forma simples"],
    "tecnicas_persuasao": [
      {
        "tecnica": "Nome simples da técnica",
        "exemplo": "Trecho que usa essa técnica",
        "efeito": "O que isso causa na pessoa que lê"
      }
    ],
    "lacunas": ["O que está faltando ou sendo omitido, explicado de forma clara"],
    "aspectos_emocionais": ["Como o conteúdo mexe com as emoções da gente"],
    "agente_e_alvo": "Quem está falando e quem é o público-alvo",
    "intencao": "Qual é a intenção real por trás desse conteúdo",
    "outro_lado": "O que a outra versão da história diria",
    "versao_neutra": "Uma versão mais equilibrada e justa do mesmo conteúdo",
    "justificativa": "Por que você chegou nessa conclusão"
  },
  "diagnostico_final": "Conclusão clara, objetiva e em um parágrafo só"
}
"""

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
                    txt = response.text.strip()

                    json_match = re.search(r'\{.*\}', txt, re.DOTALL)
                    if json_match:
                        txt = json_match.group(0)

                    resultado = json.loads(txt)

                    st.success("✅ Auditoria concluída")
                    st.json(resultado)

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
                    txt = response.text.strip()

                    json_match = re.search(r'\{.*\}', txt, re.DOTALL)






    

  

  
