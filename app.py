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
        if len(df.columns) <= 1: 
            df = pd.read_csv("dados_consolidados.csv", sep=",")
    except Exception:
        df = pd.read_csv("dados_consolidados.csv")
    
    # Limpa espaços invisíveis nos nomes das colunas
    df.columns = df.columns.str.strip()
    return df

df = carregar_dados()

# 3. Organização do Layout em Duas Abas Interativas
aba_graficos, aba_lixiviacao = st.tabs(["📈 Linha do Tempo & Artigos", "⚠️ O Paradoxo da Lixiviação (Risco Ocupacional)"])

with aba_graficos:
    st.subheader("Evolução das Publicações Acadêmicas (Google Acadêmico)")
    
    # Identificar dinamicamente as colunas que contêm os dados dos artigos
    colunas_artigos = [c for c in df.columns if "Artigos" in c or "artigos" in c]
    
    if len(colunas_artigos) > 0:
        fig = px.line(
            df, 
            x="Ano", 
            y=colunas_artigos,
            labels={"value": "Quantidade de Artigos", "variable": "Foco da Pesquisa", "Ano": "Ano"},
            title="Tendência de Artigos Científicos por Ano",
            markers=True
        )
        
        for trace in fig.data:
            trace.name = trace.name.replace("_", " ")
            
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Nenhuma coluna de artigos encontrada. Verifique se os nomes das colunas começam com 'Artigos'.")
    
    st.markdown("---")
    st.subheader("🔍 Linha do Tempo e Contexto dos Marcos Regulatórios")
    
    # SOLUÇÃO BLINDADA: Identifica as colunas de texto por exclusão para nunca mais dar erro de índice
    colunas_texto = [c for c in df.columns if c not in ["Ano", "ANO"] and "Artigos" not in c and "artigos" not in c]
    
    if len(colunas_texto) > 0:
        # A primeira coluna de texto será considerada o Marco Histórico
        col_marco = colunas_texto[0]
        
        # Filtra a tabela para pegar apenas as linhas que têm algum texto explicativo escrito
        df_marcos = df[df[col_marco].notna() & (df[col_marco].astype(str).str.strip() != "")]
        
        if not df_marcos.empty:
            st.write("Selecione um ano para entender o contexto histórico da época:")
            ano_selecionado = st.selectbox("Escolha o ano do Marco Histórico:", sorted(df_marcos["Ano"].unique()))
            
            linha = df_marcos[df_marcos["Ano"] == ano_selecionado].iloc[0]
            
            # Se houver uma segunda coluna de texto (ex: Categoria), usamos ela, senão mostramos apenas o Marco
            if len(colunas_texto) > 1:
                col_cat = colunas_texto[1]
                st.info(f"**[{str(linha[col_cat]).upper()}] Em {ano_selecionado}:** {linha[col_marco]}")
            else:
                st.info(f"**Em {ano_selecionado}:** {linha[col_marco]}")
        else:
            st.info("ℹ️ Nenhum texto de marco histórico detetado nas linhas da planilha.")
    else:
        st.warning("⚠️ Não foi encontrada nenhuma coluna de texto para os marcos históricos na planilha.")

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
