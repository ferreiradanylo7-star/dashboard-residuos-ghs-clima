import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração Inicial da Página
st.set_page_config(
    page_title="Resíduos, Clima e GHS", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

st.title("📊 Análise Evolutiva: Gestão de Resíduos, GHS e Mudanças Climáticas")
st.markdown("""
Este painel interativo correlaciona o crescimento da produção científica mundial com os principais marcos regulatórios, 
evidenciando a transição da engenharia sanitária tradicional para a era da Economia Circular e avaliação de riscos toxicológicos.
""")

# 2. Leitura dos Dados do Repositório
@st.cache_data
def carregar_dados():
    # Carrega o CSV que você subiu no repositório
    df = pd.read_csv("dados_consolidados.csv")
    return df

df = carregar_dados()

# 3. Organização do Layout em Duas Abas Interativas
aba_graficos, aba_lixiviacao = st.tabs(["📈 Linha do Tempo & Artigos", "⚠️ O Paradoxo da Lixiviação (Risco Ocupacional)"])

with aba_graficos:
    st.subheader("Evolução das Publicações Acadêmicas (Google Acadêmico)")
    
    # Criando o gráfico interativo de linhas usando o Plotly
    fig = px.line(
        df, 
        x="Ano", 
        y=["Artigos_Clima_Residuos", "Artigos_GHS_Residuos"],
        labels={"value": "Quantidade de Artigos", "variable": "Foco da Pesquisa", "Ano": "Ano"},
        title="Tendência de Artigos Científicos por Ano",
        markers=True
    )
    
    # Customizando as legendas para ficarem bonitas em português
    novos_nomes = {"Artigos_Clima_Residuos": "Crise Climática + Resíduos", "Artigos_GHS_Residuos": "GHS + Resíduos"}
    fig.for_each_trace(lambda t: t.update(name = novos_nomes[t.name]))
    
    # Plotando o gráfico na tela
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🔍 Linha do Tempo e Contexto dos Marcos Regulatórios")
    st.write("Mova a barra ou selecione um ano para entender o contexto histórico da época:")
    
    # Caixa de seleção baseada nos anos da sua planilha que possuem marcos escritos
    df_marcos = df[df["Marco_Historico"].notna()]
    ano_selecionado = st.selectbox("Escolha o ano do Marco Histórico:", df_marcos["Ano"].unique())
    
    # Buscando a linha correspondente ao ano selecionado
    linha = df_marcos[df_marcos["Ano"] == ano_selecionado].iloc[0]
    
    # Exibindo o marco histórico de forma destacada
    st.info(f"**[{linha['Categoria'].upper()}] Em {ano_selecionado}:** {linha['Marco_Historico']}")

with aba_lixiviacao:
    st.subheader("Fique Atento: Lixiviação vs. Risco Ocupacional na ABNT NBR 10004:2024")
    st.markdown("""
    A transição do Brasil para o modelo europeu e para o **GHS** resolveu um grande ponto cego que existia na norma de 2004. 
    Veja o contraste abaixo:
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.error("### 🔴 O Cenário Antigo (A NBR 10004:2004)")
        st.write("""
        - O foco principal era puramente ambiental e de engenharia de aterros (proteção de águas subterrâneas).
        - Se o poluente não se desprendesse do resíduo no ensaio laboratorial de lixiviação, o laudo declarava o material como **Não Perigoso**.
        - **O Perigo:** Criava uma falsa sensação de segurança jurídica e ignorava os riscos à saúde de quem manipulava o resíduo na fábrica.
        """)
    with col2:
        st.success("### 🟢 O Cenário Atual (A NBR 10004:2024)")
        st.write("""
        - Alinhamento total com a composição química real e a **Economia Circular**.
        - Mesmo que um resíduo passe no teste de lixiviação (não solte nada na água), ele pode ser enquadrado como **Classe 1 (Perigoso)** se tiver substâncias cancerígenas, mutagênicas ou de toxicidade crônica severa.
        - **Foco no Trabalhador:** Proteção direta contra o risco ocupacional por contato ou inalação de poeiras.
        """)
