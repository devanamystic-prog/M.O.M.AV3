import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# =========================
# PROMPT DO M.O.M.A.
# =========================

MOMA_PROMPT = """
CONTEXTO:
Você é o M.O.M.A., motor de análise forense de narrativas.

Sua função é auditar qualquer texto ou imagem através de um protocolo rígido de 10 camadas lógicas, com neutralidade absoluta.

ESQUEMA JSON OBRIGATÓRIO:

{
  "indice_distorcao": 0,
  "veredito_resumo": "String curta",
  "protocolo_10_camadas": {
    "c1_fatos": ["..."],
    "c2_inducao": [
      {
        "trecho_exato": "...",
        "analise": "..."
      }
    ],
    "c3_persuasao": [
      {
        "tecnica": "...",
        "trecho": "...",
        "efeito": "..."
      }
    ],
    "c4_lacunas": ["..."],
    "c5_emocional": ["..."],
    "c6_agencia": {
      "agente_ativo": "...",
      "alvo_passivo": "..."
    },
    "c7_intencao": "...",
    "c8_outro_lado": "...",
    "c9_reescrita_neutra": "...",
    "c10_calibracao_justificativa": "..."
  },
  "diagnostico_final": "Conclusão forense detalhada."
}
"""

# =========================
# CONFIGURAÇÃO DA API
# =========================

try:

    api_key = st.secrets["GOOGLE_API_KEY"]

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        system_instruction=MOMA_PROMPT
    )

except Exception:

    st.warning(
        "🧠 O núcleo analítico não conseguiu despertar."
    )

    st.stop()

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================

st.set_page_config(
    page_title="M.O.M.A.",
    page_icon="🧠",
    layout="centered"
)

# =========================
# TOPO
# =========================

st.image("logo.PNG", width=300)

st.title("🧠 M.O.M.A.")

st.markdown("""
# Media Objectivity & Manipulation Auditor

### Protocolo Forense
""")

# =========================
# TIPO DE ENTRADA
# =========================

opcao = st.radio(
    "Tipo de entrada:",
    [
        "Texto",
        "Imagem (print)"
    ]
)

# =========================
# TEXTO
# =========================

if opcao == "Texto":

    entrada = st.text_area(
        "Cole o texto para auditoria:",
        height=250
    )

    if st.button("🧠 Auditar Texto"):

        if entrada:

            with st.spinner("🧠 Executando protocolo forense..."):

                try:

                    response = model.generate_content(entrada)

                    txt = (
                        response.text
                        .replace("```json", "")
                        .replace("```", "")
                        .strip()
                    )

                    st.success("✅ Auditoria concluída")

                    st.json(json.loads(txt))

                except Exception:

                    st.warning(
                        "🧠 O protocolo entrou em repouso.\n\n"
                        "Os núcleos analíticos estão se reorganizando.\n"
                        "Tente novamente mais tarde."
                    )

        else:

            st.warning(
                "📄 Insira um texto para iniciar a auditoria."
            )

# =========================
# IMAGEM
# =========================

else:

    arquivo = st.file_uploader(
        "Envie um print:",
        type=["png", "jpg", "jpeg"]
    )

    if st.button("🧠 Auditar Imagem"):

        if arquivo:

            with st.spinner("🧠 Executando protocolo visual..."):

                try:

                    img = Image.open(arquivo)

                    st.image(
                        img,
                        caption="Print enviado",
                        width=300
                    )

                    response = model.generate_content([
                        "Faça uma auditoria forense completa desta imagem.",
                        img
                    ])

                    txt = (
                        response.text
                        .replace("```json", "")
                        .replace("```", "")
                        .strip()
                    )

                    st.success("✅ Auditoria concluída")

                    st.json(json.loads(txt))

                except Exception:

                    st.warning(
                        "🧠 O protocolo visual entrou em repouso.\n\n"
                        "Os núcleos analíticos estão se reorganizando.\n"
                        "Tente novamente mais tarde."
                    )

        else:

            st.warning(
                "🖼️ Envie uma imagem para iniciar a auditoria."
            )

# =========================
# LIMPAR
# =========================

if st.button("🔄 Limpar"):

    st.rerun()




    

  

  
