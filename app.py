
import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuração do Protocolo MOMA
MOMA_PROMPT = """Analise este conteúdo como M.O.M.A. v2, motor forense. 
Use 10 camadas lógicas (Factual, Indução, Persuasão, Lacunas, Emocional, Agência, Intenção, Contraponto, Reescrita Neutra, Calibração).
Responda EXCLUSIVAMENTE em JSON:
{
  "indice_distorcao": 0,
  "veredito_resumo": "...",
  "protocolo_10_camadas": {},
  "diagnostico_final": "..."
}"""

# Inicialização da API
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    # Mudança aqui: usando o nome 'latest' que ajuda em versões instáveis
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
except Exception as e:
    st.error("Erro na API")
    st.stop()

st.set_page_config(page_title="M.O.M.A. v2", page_icon="🧠")
st.title("🧠 M.O.M.A. v2")
st.caption("Protocolo Forense de Análise de Narrativas")

opcao = st.radio("Tipo de entrada:", ["Texto", "Imagem"])

if opcao == "Texto":
    entrada = st.text_area("Cole o texto para auditoria:", height=200)
    if st.button("Auditar Texto"):
        if entrada:
            with st.spinner("Analisando..."):
                try:
                    response = model.generate_content([MOMA_PROMPT, entrada])
                    txt = response.text.replace("```json", "").replace("```", "").strip()
                    st.json(txt)
                except Exception as e:
                    st.error(f"Erro: {e}")
        else:
            st.warning("Cole um texto.")

else:
    arquivo = st.file_uploader("Suba a imagem/print:", type=["png", "jpg", "jpeg"])
    if st.button("Auditar Imagem"):
        if arquivo:
            with st.spinner("Analisando imagem..."):
                try:
                    img = Image.open(arquivo)
                    st.image(img, caption="Imagem carregada", width=300)
                    response = model.generate_content([MOMA_PROMPT, img])
                    txt = response.text.replace("```json", "").replace("```", "").strip()
                    st.json(txt)
                except Exception as e:
                    st.error(f"Erro na análise: {e}")
        else:
            st.warning("Suba uma imagem primeiro.")

if st.button("Limpar"):
    st.rerun()



    

  

  
