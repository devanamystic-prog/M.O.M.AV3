import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
import re

# ==================== PROMPT M.O.M.A. ====================
MOMA_PROMPT = """
CONTEXTO:
Você é o M.O.M.A. (Media Objectivity & Manipulation Auditor), motor de análise forense de narrativas.
Sua função é auditar qualquer texto ou imagem através de um protocolo rígido de 10 camadas lógicas, com neutralidade absoluta e rigor máximo.

Responda APENAS com um JSON válido, sem nenhuma explicação adicional antes ou depois.

ESQUEMA JSON OBRIGATÓRIO:
{
  "indice_distorcao": 0,
  "veredito_resumo": "String curta e objetiva",
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
st.caption("Protocolo Forense de 10 Camadas")

opcao = st.radio("Tipo de entrada:", ["Texto", "Imagem (print)"], horizontal=True)

# ==================== ANÁLISE DE TEXTO ====================
if opcao == "Texto":
    entrada = st.text_area("Cole o texto para auditoria:", height=300)
    if st.button("🧠 Auditar Texto", type="primary"):
        if entrada.strip():
            with st.spinner("Executando protocolo forense completo..."):
                try:
                    response = model.generate_content(entrada)
                    txt = response.text.strip()

                    # Parser robusto
                    json_match = re.search(r'\{.*\}', txt, re.DOTALL)
                    if json_match:
                        txt = json_match.group(0)
                    
                    resultado = json.loads(txt)
                    st.success("✅ Auditoria concluída com sucesso")
                    st.json(resultado)
                    
                    # Botão copiar
                    st.code(txt, language="json")
                    st.caption("Copie o JSON acima se quiser salvar")

                except Exception as e:
                    st.error(f"Erro ao processar resposta: {e}")
                    st.text_area("Resposta bruta do Gemini (para debug):", txt, height=200)
        else:
            st.warning("Insira um texto para iniciar a auditoria.")

# ==================== ANÁLISE DE IMAGEM ====================
else:
    arquivo = st.file_uploader("Envie um print ou imagem:", type=["png", "jpg", "jpeg", "webp"])
    if st.button("🧠 Auditar Imagem", type="primary"):
        if arquivo:
            with st.spinner("Analisando imagem com protocolo visual completo..."):
                try:
                    img = Image.open(arquivo)
                    st.image(img, caption="Imagem enviada", use_column_width=True)

                    # Prompt reforçado para imagem
                    prompt_imagem = "Faça uma auditoria forense completa desta imagem seguindo rigorosamente o protocolo M.O.M.A. de 10 camadas."

                    response = model.generate_content([prompt_imagem, img])
                    txt = response.text.strip()

                    # Mesmo parser robusto
                    json_match = re.search(r'\{.*\}', txt, re.DOTALL)
                    if json_match:
                        txt = json_match.group(0)

                    resultado = json.loads(txt)
                    st.success("✅ Auditoria visual concluída")
                    st.json(resultado)
                    st.code(txt, language="json")

                except Exception as e:
                    st.error(f"Erro na análise da imagem: {e}")
                    if 'txt' in locals():
                        st.text_area("Resposta bruta:", txt, height=300)
        else:
            st.warning("Envie uma imagem para iniciar a auditoria.")

# Botão limpar
if st.button("🔄 Limpar tudo"):
    st.rerun()






    

  

  
