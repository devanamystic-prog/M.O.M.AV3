import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuração do Protocolo MOMA
MOMA_PROMPT = "Analise este conteúdo como M.O.M.A. v2, motor forense. Use 10 camadas lógicas e responda apenas em JSON."

# Inicialização da API
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    # Usando o nome mais simples do modelo
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error("Erro na API")
    st.stop()

st.set_page_config(page_title="M.O.M.A. v2", page_icon="🧠")
st.title("🧠 M.O.M.A. v2")

opcao = st.radio("Tipo:", ["Texto", "Imagem"])

if opcao == "Texto":
    entrada = st.text_area("Texto para auditoria:")
    if st.button("Auditar Texto"):
        if entrada:
            with st.spinner("Analisando..."):
                try:
                    response = model.generate_content([MOMA_PROMPT, entrada])
                    st.json(response.text.replace("```json", "").replace("```", "").strip())
                except Exception as e:
                    st.error(f"Erro: {e}")

else:
    arquivo = st.file_uploader("Suba a imagem:", type=["png", "jpg", "jpeg"])
    if st.button("Auditar Imagem"):
        if arquivo:
            with st.spinner("Analisando..."):
                try:
                    img = Image.open(arquivo)
                    st.image(img, width=300)
                    response = model.generate_content([MOMA_PROMPT, img])
                    st.json(response.text.replace("```json", "").replace("```", "").strip())
                except Exception as e:
                    st.error(f"Erro na análise: {e}")

if st.button("Limpar"):
    st.rerun()



    

  

  
