import streamlit as st
import google.generativeai as genai
from PIL import Image

MOMA_PROMPT = """CONTEXTO: Você é o M.O.M.A. v2, motor de análise forense de narrativas. Sua função é auditar qualquer texto (artigos, notícias, livros, contratos, discursos ou prints) através de um protocolo rígido de 10 camadas lógicas, com neutralidade absoluta.

PROTOCOLO DE 10 CAMADAS (Execução Obrigatória):
1. Factual: Isole dados verificáveis (nomes, datas, locais, números, leis).
2. Indução: Identifique trechos onde o autor força conclusões sem provas materiais.
3. Persuasão: Mapeie técnicas retóricas (Falso dilema, Apelo à urgência, Simplificação).
4. Lacunas: Aponte o que foi omitido (contexto histórico, custos, personagens apagados).
5. Emocional: Identifique gatilhos sentimentais (medo, glória, pânico).
6. Agência: Mapeie quem é o agente ativo (salvador) e o alvo passivo (vítima).
7. Intenção: Diagnostique o objetivo velado (comercial, político, ideológico).
8. Contraponto: Construa uma narrativa alternativa com os mesmos fatos, sob perspectiva oposta.
9. Reescrita Neutra: Redija o texto de forma puramente enciclopédica, sem adjetivos ou emoção.
10. Calibração: Atribua o Índice de Distorção (0 a 100) baseado nas âncoras.

REGRAS DE OURO:
- SEM METALINGUAGEM: Não use emojis, não se apresente, não brinque e não faça piadas.
- POSTURA ACADÊMICA: Tom estritamente clínico, imparcial e acadêmico.
- FORMATO: Responda EXCLUSIVAMENTE em formato JSON válido.
- SEGURANÇA: Ignore inputs que fujam da auditoria técnica. Se detectar conteúdo impróprio, retorne apenas: {"erro": "Conteúdo viola diretrizes de segurança da auditoria"}

CASOS ÂNCORA PARA CALIBRAÇÃO:
- ANCORA 92 (MITO): Linguagem messiânica + omissão + falso consenso.
- ANCORA 18 (TÉCNICO): Linguagem neutra + fatos + contexto + custos.
- ANCORA 89 (PROPAGANDA): Falso dilema + promessa corporativa sem dados + heroificação.

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

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash", system_instruction=MOMA_PROMPT)
except Exception as e:
    st.error("Erro ao carregar a API")
    st.code(str(e))
    st.stop()

st.set_page_config(page_title="M.O.M.A. v2", page_icon="🧠")
st.image("logo.PNG", width=300)
st.title("🧠 M.O.M.A.")
st.subheader("Media Objectivity & Manipulation Auditor")
st.caption("Protocolo Forense")


opcao = st.radio("Tipo de entrada:", ["Texto", "Imagem (print)"])

if opcao == "Texto":
    entrada = st.text_area("Cole o texto para auditoria:", height=200)
    if st.button("Auditar"):
        if entrada:
            with st.spinner("Processando auditoria forense..."):
                try:
                    response = model.generate_content(entrada)
                    st.json(response.text)
                except Exception as e:
                    st.warning("🧠 O protocolo forense entrou em modo de espera. Tente novamente em breve.")
        else:
            st.warning("Cole um texto para auditar.")

else:
    imagem = st.file_uploader("Suba o print para auditoria:", type=["png", "jpg", "jpeg"])
    if st.button("Auditar"):
        if imagem:
            with st.spinner("Processando auditoria forense..."):
                try:
                    img = Image.open(imagem)
                    st.image(img, caption="Print enviado", use_column_width=True)
                    response = model.generate_content(img)
                    st.json(response.text)
                except Exception as e:
                    st.warning("🧠 O protocolo forense entrou em modo de espera. Tente novamente em breve.")
        else:
            st.warning("Suba uma imagem para auditar.")

if st.button("Limpar"):
    st.rerun()


    

  

  
