import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuração do M.O.M.A.
MOMA_PROMPT = """CONTEXTO: Você é o M.O.M.A. v2, motor de análise forense de narrativas. Sua função é auditar qualquer texto ou imagem através de um protocolo rígido de 10 camadas lógicas, com neutralidade absoluta.
ESQUEMA JSON OBRIGATÓRIO:
{
  "indice_distorcao": 0,
  "veredito_resumo": "String curta",
  "protocolo_10_camadas": {
    "c1_fatos": ["..."],
    "c2_inducao": [{"trecho_exato": "...", "analise": "..."}],
    "c3_persuasao": [{"tecnica": "...", "trecho": "...", "efeito": "..."}],
    "c4_lacunas": ["..."],
    "c5_emocional": ["..."],
    "c6_agencia": {"agente_ativo": "...", "alvo_passivo": "..."},
    "c7_intencao": "...",
    "c8_outro_lado": "...",
    "c9_reescrita_neutra": "...",
    "c10_calibracao_justificativa": "..."
  },
  "diagnostico_final": "Conclusão forense detalhada."
}"""

# 2. Inicialização da API
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    # Usando o 1.5-flash para não dar erro de cota
    model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=MOMA_PROMPT)
except Exception as e:
    st.error("Erro na API")
    st.stop()

# 3. Interface do Usuário
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
                    response = model.generate_content(entrada)
                    txt = response.text.replace("```json", "").replace("```", "").strip()
                    st.json(txt)
                except Exception as e:
                    st.error(f"Erro: {e}")
        else:
            st.warning("Cole um texto primeiro.")

else:
    arquivo = st.file_uploader("Suba a imagem/print:", type=["png", "jpg", "jpeg"])
    if st.button("Auditar Imagem"):
        if arquivo:
            with st.spinner("Analisando imagem..."):
                try:
                    img = Image.open(arquivo)
                    st.image(img, caption="Imagem carregada", width=300)
                    response = model.generate_content(["Analise esta imagem conforme o protocolo MOMA", img])
                    txt = response.text.replace("```json", "").replace("```", "").strip()
                    st.json(txt)
                except Exception as e:
                    st.error(f"Erro na imagem: {e}")
        else:
            st.warning("Suba uma imagem primeiro.")

if st.button("Limpar"):
    st.rerun()




    

  

  
