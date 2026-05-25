import streamlit as st
import google.generativeai as genai
from PIL import Image
import re

# ==================== PROMPT FORTE ====================
MOMA_PROMPT = """
Você é o M.O.M.A., auditor honesto e fácil de entender.

Responda **EXCLUSIVAMENTE** com um JSON válido, sem nenhuma palavra antes ou depois, sem ```json.

Use exatamente este formato:

{
  "indice_distorcao": 0,
  "veredito_resumo": "resumo curto",
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
  "diagnostico_final": "conclusão clara"
}
"""

# ==================== VALIDAÇÃO SIMPLIFICADA ====================
def extrair_json(texto):
    texto = re.sub(r'^```(?:json)?\s*|\s*```$', '', texto, flags=re.MULTILINE | re.IGNORECASE)
    match = re.search(r'\{[\s\S]*\}', texto)
    if match:
        try:
            return eval(match.group(0))  # modo leve
        except:
            return None
    return None

# ==================== EXIBIÇÃO BONITA ====================
def exibir_analise(dados):
    st.success("✅ Auditoria concluída!")
    st.markdown(f"**📋 Resumo:** {dados.get('veredito_resumo', 'Sem resumo')}")
    st.divider()
    st.markdown("**✅ Fatos principais**")
    for f in dados.get('analise_detalhada', {}).get('fatos', []):
        st.markdown(f"• {f}")
    # (o resto da exibição continua bonito, mas simplificado)

    st.divider()
    if st.button("📋 Copiar relatório completo"):
        st.code(str(dados), language=None)

# ==================== CONFIGURAÇÃO ====================
st.set_page_config(page_title="M.O.M.A.", page_icon="🧠", layout="centered")

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        "gemini-3.5-flash",
        system_instruction=MOMA_PROMPT
    )
except Exception as e:
    st.error(f"Erro de configuração: {e}")
    st.stop()

# Interface (igual antes)
st.image("logo.PNG", width=300)
st.title("🧠 M.O.M.A.")
st.caption("Análise clara e honesta")

opcao = st.radio("Tipo de entrada:", ["Texto", "Imagem (print)"], horizontal=True)

if opcao == "Texto":
    # ... (código de texto igual)
    pass  # vou deixar só a parte da imagem pra não ficar gigante

else:
    arquivo = st.file_uploader("Envie um print ou imagem:", type=["png", "jpg", "jpeg", "webp"])
    if st.button("🧠 Auditar Imagem", type="primary"):
        if arquivo:
            with st.spinner("Analisando..."):
                try:
                    img = Image.open(arquivo)
                    st.image(img, caption="Imagem enviada", use_column_width=True)

                    prompt = "Faça uma auditoria completa desta imagem. Responda APENAS com o JSON exato do protocolo M.O.M.A., sem nenhuma explicação extra."

                    response = model.generate_content([prompt, img])
                    dados = extrair_json(response.text)

                    if dados:
                        exibir_analise(dados)
                    else:
                        st.error("O Gemini não devolveu JSON. Resposta bruta:")
                        st.write(response.text)
                except Exception as e:
                    st.error(f"Erro: {e}")
        else:
            st.warning("Envie uma imagem.")

if st.button("🔄 Limpar tudo"):
    y
