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

# 2. Leitura dos Dados com detecção automática de separador (; ou ,)
@st.cache_data
def carregar_dados():
    try:
        # Tenta ler primeiro com ponto e vírgula (padrão do Excel em português)
        df = pd.read_csv("dados_consolidados.csv", sep=";")
        if len(df.columns) <= 1: # Se der errado, tenta o padrão de vírgula
            df = pd.read_csv("dados_consolidados.csv", sep=",")
    except Exception:
        df = pd.read_csv("dados_consolidados.csv")
    
    # Remove espaços invisíveis que possam existir nos nomes das colunas
    df.columns = df.columns.str.strip()
    return df

df = carregar_dados()

# 3. Organização do Layout em Duas Abas Interativas
aba_graficos, aba_lixiviacao = st.tabs(["📈 Linha do Tempo & Artigos", "⚠️ O Paradoxo da Lixiviação (Risco Ocupacional)"])

with aba_graficos:
    st.subheader("Evolução das Publicações Acadêmicas (Google Acadêmico)")
    
    # Identificar dinamicamente as colunas de artigos para evitar erros de digitação
    colunas_artigos = [c for c in df.columns if "Artigos" in c]
    
    if len(colunas_artigos) > 0:
        # Criando o gráfico interativo de linhas usando o Plotly
        fig = px.line(
            df, 
            x="Ano", 
            y=colunas_artigos,
            labels={"value": "Quantidade de Artigos", "variable": "Foco da Pesquisa", "Ano": "Ano"},
            title="Tendência de Artigos Científicos por Ano",
            markers=True
        )
        
        # Ajusta as legendas de forma amigável
        for trace in fig.data:
            nome_limpo = trace.name.replace("_", " ")
            trace.name = nome_limpo
            
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Nenhuma coluna de artigos encontrada. Verifique se o nome das colunas na sua planilha começa com a palavra 'Artigos'.")
    
    st.markdown("---")
    st.subheader("🔍 Linha do Tempo e Contexto dos Marcos Regulatórios")
    
    # Garante que vai achar a coluna do Marco histórico independente de maiúscula/minúscula
    col_marco = [c for c in df.columns if "Marco" in c or "marco" in c][0]
    col_cat = [c for c in df.columns if "Cat" in c or "cat" in c][0]
    
    df_marcos = df[df[col_marco].notna() & (df[col_marco] != "")]
    
    if not df_marcos.empty:
        st.write("Selecione um ano para entender o contexto histórico da época:")
        ano_selecionado = st.selectbox("Escolha o ano do Marco Histórico:", sorted(df_marcos["Ano"].unique()))
        
        linha = df_marcos[df_marcos["Ano"] == ano_selecionado].iloc[0]
        st.info(f"**[{str(linha[col_cat]).upper()}] Em {ano_selecionado}:** {linha[col_marco]}")
    else:
        st.info("Nenhum texto de marco histórico detectado para exibição.")

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
        - Mesmo que um resíduo passe no teste de lixiviação (não solte nada na água), ele pode ser enquadrado como **Classe 1 (Perigoso)** se tiver substâncias cancerígenas, mutagênicos ou de toxicidade crônica severa.
        - **Foco no Trabalhador:** Proteção direta contra o risco ocupacional por contato ou inalação de poeiras.
        """)
