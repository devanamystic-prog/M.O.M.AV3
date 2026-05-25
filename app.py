import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuração simples
MOMA_PROMPT = "Você é o M.O.M.A. v2. Analise este conteúdo com o protocolo forense de 10 camadas e responda em JSON."

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    # Usando o nome mais básico que existe
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Erro ao iniciar API")
    st.stop()

st.title("🧠 M.O.M.A. v2")

opcao = st.radio("Entrada:", ["Texto", "Imagem"])

if opcao == "Texto":
    entrada = st.text_area("Texto:")
    if st.button("Auditar Texto"):
        if entrada:
            try:
                # Forma mais simples de chamada
                response = model.generate_content(f"{MOMA_PROMPT}\n\nTexto: {entrada}")
                st.json(response.text.replace("```json", "").replace("```", "").strip())
            except Exception as e:
                st.error(f"Erro: {e}")

else:
    arquivo = st.file_uploader("Imagem:", type=["png", "jpg", "jpeg"])
    if st.button("Auditar Imagem"):
        if arquivo:
            try:
                img = Image.open(arquivo)
                st.image(img, width=300)
                # Chamada direta para imagem
                response = model.generate_content([MOMA_PROMPT, img])
                st.json(response.text.replace("```json", "").replace("```", "").strip())
            except Exception as e:
                st.error(f"Erro na análise: {e}")

if st.button("Limpar"):
    st.rerun()



    

  

  
