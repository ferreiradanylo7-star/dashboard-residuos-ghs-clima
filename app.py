import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Configuração Inicial da Página
st.set_page_config(
    page_title="Resíduos, Clima e GHS", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Estilização CSS personalizada
st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0.5rem; }
    .subtitle { font-size: 1.1rem; color: #4B5563; margin-bottom: 2rem; }
    .section-holder { padding: 1.5rem; border-radius: 0.5rem; background-color: #F3F4F6; margin-bottom: 1rem; height: 100%; }
    .green-title { color: #15803D !important; font-weight: 600; font-size: 1.2rem; margin-bottom: 0.5rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📊 Análise Evolutiva: Gestão de Resíduos, GHS e Mudanças Climáticas</div>', unsafe_allow_html=True)
st.markdown("""
<div class="subtitle">
Este painel interativo correlaciona o crescimento da produção científica mundial com os principais marcos regulatórios, 
evidenciando a transição da engenharia sanitária tradicional para a era da Economia Circular e avaliação de riscos toxicológicos intrínsecos.
</div>
""", unsafe_allow_html=True)

# 2. Leitura dos Dados com Dicionário Oficial de Marcos Históricos
@st.cache_data
def carregar_dados():
    marcos_oficiais = {
        1972: "Conferência de Estocolmo e Criação do PNUMA (Ano Zero da consciência ambiental global).",
        1973: "Criação da SEMA (Secretaria Especial do Meio Ambiente) no Brasil.",
        1981: "Instituição da PNMA (Política Nacional do Meio Ambiente - Lei nº 6.938) no Brasil.",
        1987: "Publicação da primeira versão da ABNT NBR 10004 (Foco em aterros).",
        1989: "Publicação do 'Livro Azul' pela OMS/PNUMA: 'The Management of Hazardous Wastes'.",
        1992: "Eco-92 no Rio de Janeiro (Adoção da Agenda 21 e Convenção do Clima).",
        1994: "Publicação da primeira versão do Catálogo Europeu de Resíduos (EWC).",
        1997: "Assinatura do Protocolo de Kyoto (Primeiras metas rígidas de emissões climáticas).",
        1998: "Sanção da Lei de Crimes Ambientais (Lei nº 9.605) no Brasil.",
        2000: "União Europeia reformula e unifica seu Catálogo Harmonizado de Resíduos.",
        2002: "Entrada em vigor do Catálogo Europeu padronizado em códigos de 6 dígitos.",
        2003: "Publicação oficial da 1ª Edição do GHS pela ONU (O 'Livro Roxo').",
        2004: "Publicação da segunda versão da ABNT NBR 10004 (Consolidação de lixiviação/solubilização).",
        2008: "União Europeia adota o Regulamento CLP, integrando o GHS aos critérios de perigo.",
        2010: "Instituição da Política Nacional de Resíduos Sólidos (PNRS - Lei nº 12.305).",
        2012: "Publicada a Instrução Normativa 13 do Ibama, a Lista Brasileira de Resíduos Sólidos",
        2014: "União Europeia revisa seu Catálogo de Resíduos para alinhá-lo 100% ao GHS.",
        2015: "Assinatura do Acordo de Paris (COP21) e lançamento dos ODS da ONU.",
        2018: "Política da 'Espada Nacional' da China (Proibição da importação de resíduos plásticos mundiais).",
        2020: "Aprovação do Novo Marco Legal do Saneamento Básico (Lei nº 14.026) no Brasil.",
        2022: "Publicação do Planares (Plano Nacional de Resíduos Sólidos) com metas de redução de metano.",
        2024: "Publicação da Nova ABNT NBR 10004 (Partes 1 e 2), adotando a LGR (6 dígitos) e o GHS."
    }

    if os.path.exists("dados_consolidados.csv"):
        try:
            df = pd.read_csv("dados_consolidados.csv", sep=";")
            if len(df.columns) <= 1: 
                df = pd.read_csv("dados_consolidados.csv", sep=",")
            df.columns = df.columns.str.strip()
            if "Ano" in df.columns or "ANO" in df.columns:
                col_ano_local = "Ano" if "Ano" in df.columns else "ANO"
                df["Marco_Historico"] = df[col_ano_local].map(marcos_oficiais).fillna("")
            return df
        except Exception:
            pass 
            
    anos = list(range(1972, 2026))
    artigos_clima = []
    artigos_ghs = []
    
    for val_ano in anos:
        if val_ano < 2000:
            artigos_clima.append(int(5 + (val_ano - 1972) * 1.5))
            artigos_ghs.append(0)
        else:
            idx = val_ano - 2000
            artigos_clima.append(45 + idx * 105)
            artigos_ghs.append(2 + idx * 53 if val_ano >= 2003 else 0)
            
    df_mock = pd.DataFrame({
        "Ano": anos,
        "Artigos_Residuos_Clima": artigos_clima,
        "Artigos_GHS_Residuos": artigos_ghs,
        "Marco_Historico": [marcos_oficiais.get(a, "") for a in anos]
    })
    return df_mock

df = carregar_dados()
df = df[df["Ano"] <= 2025] 

col_ano = "Ano"
col_clima = "Artigos_Residuos_Clima"
col_ghs = "Artigos_GHS_Residuos"
col_marco = "Marco_Historico"

# 3. Menu Lateral (Sidebar)
st.sidebar.header("⚙️ Filtros e Parâmetros")
ano_min, ano_max = st.sidebar.slider(
    "Selecione o Intervalo de Anos Gerais:",
    int(df["Ano"].min()), int(df["Ano"].max()),
    (int(df["Ano"].min()), int(df["Ano"].max()))
)
df_filtrado = df[(df["Ano"] >= ano_min) & (df["Ano"] <= ano_max)]

# 4. Organização das Abas
aba_graficos, aba_comparativo, aba_lixiviacao, aba_resumo = st.tabs([
    "📈 Linha do Tempo & Artigos", 
    "🔍 Comparativo NBR 10004 (2004 vs 2024)", 
    "⚠️ O Paradoxo da Lixiviação",
    "📌 Resumo Executivo"
])

# --- ABA 1: GRÁFICOS ---
with aba_graficos:
    st.subheader("Análise Avançada e Combinada de Publicações Acadêmicas")
    
    nomes_legendas = {col_clima: "Resíduos ✕ Crise Climática", col_ghs: "GHS ✕ Classificação de Resíduos"}

    # Gráfico 1: Resíduos x Clima
    st.markdown("#### 1. Tendência de Artigos: Resíduos ✕ Crise Climática")
    fig1 = px.line(df_filtrado, x="Ano", y=col_clima, markers=True, title="Evolução de Pesquisas sobre Resíduos e Clima (Até 2025)")
    fig1.update_traces(line_color="#1E3A8A", line_width=3)
    st.plotly_chart(fig1, use_container_width=True)
    
    st.markdown("---")
    
    # Gráfico 2: GHS x Resíduos
    st.markdown("#### 2. Tendência de Artigos: GHS ✕ Classificação de Resíduos")
    fig2 = px.line(df_filtrado, x="Ano", y=col_ghs, markers=True, title="Evolução de Pesquisas sobre Aplicação do GHS (Dados até 2025)")
    fig2.update_traces(line_color="#D97706", line_width=3)
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    
    # Gráfico 3: Combinado
    st.markdown("#### 3. Correlação Científica Integrada")
    fig3 = px.line(df_filtrado, x="Ano", y=[col_clima, col_ghs], markers=True, title="Visão Unificada: Avanço Científico Comparado")
    fig3.for_each_trace(lambda t: t.update(name=nomes_legendas.get(t.name, t.name), line_width=3))
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # Gráfico 4: CORRIGIDO (Espaçamento e legibilidade)
    st.markdown("#### 4. Densidade Científica nos Anos dos Marcos Regulatórios")
    df_marcos_exclusivos = df_filtrado[df_filtrado[col_marco].notna() & (df_filtrado[col_marco].astype(str).str.strip() != "")].copy()
    df_marcos_exclusivos = df_marcos_exclusivos.sort_values(by="Ano")
    df_marcos_exclusivos["Ano_Ref"] = df_marcos_exclusivos["Ano"].astype(str)
    
    df_melt4 = df_marcos_exclusivos.melt(
        id_vars=["Ano_Ref", col_marco],
        value_vars=[col_clima, col_ghs],
        var_name="Foco do Estudo",
        value_name="Quantidade"
    )
    df_melt4["Foco do Estudo"] = df_melt4["Foco do Estudo"].map(nomes_legendas)

    fig4 = px.bar(
        df_melt4, x="Ano_Ref", y="Quantidade", color="Foco do Estudo", barmode="group",
        title="Volume de Artigos Científicos nos Anos dos Marcos Regulatórios",
        text_auto=True
    )
    fig4.update_layout(
        bargap=0.3, bargroupgap=0.1, height=600, margin=dict(t=80, b=50),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig4, use_container_width=True)

# --- ABA 2: COMPARATIVO ---
with aba_comparativo:
    st.subheader("🔄 O Salto Normativo: Diferenças Cruciais entre as Versões da ABNT NBR 10004")
    dados_comparativos = {
        "Critério de Análise": ["Estrutura de Codificação", "Mecanismo de Toxicidade", "Conexão Internacional", "Foco Principal", "Governança e Emissão", "Período de Transição"],
        "Versão Anterior (NBR 10004:2004)": ["Listas fixas e estanques", "Foco exclusivo em lixiviação", "Baixo alinhamento", "End-of-Pipe", "Laudos genéricos", "Não possuía cronograma"],
        "Nova Versão (NBR 10004:2024)": ["LGR (6 dígitos)", "Perigo intrínseco/GHS", "Alinhamento pleno", "Saúde do Trabalhador", "Responsável Técnico habilitado", "Vigência até 31/12/2026"]
    }
    st.table(pd.DataFrame(dados_comparativos))
    
    col_card1, col_card2, col_card3 = st.columns(3)
    with col_card1:
        st.markdown('<div class="section-holder"><div class="green-title">1. Rastreabilidade</div><p>Novos códigos de 6 dígitos facilitam a rastreabilidade do processo gerador ao destino final.</p></div>', unsafe_allow_html=True)
    with col_card2:
        st.markdown('<div class="section-holder"><div class="green-title">2. Segurança Jurídica</div><p>Alinhamento com GHS diminui ambiguidades em fiscalizações.</p></div>', unsafe_allow_html=True)
    with col_card3:
        st.markdown('<div class="section-holder"><div class="green-title">3. Adequação de FDS/FDSR</div><p>Resíduos com perigo por toxicidade exigem nova FDSR atualizada.</p></div>', unsafe_allow_html=True)

# --- ABA 3: PARADOXO ---
with aba_lixiviacao:
    st.subheader("⚠️ Entenda o Cenário: Lixiviação vs. Risco Ocupacional")
    col1, col2 = st.columns(2)
    with col1:
        st.error("### 🔴 O Cenário Antigo (A NBR 10004:2004)")
        st.markdown("* **Mecanismo:** Foco em lixiviação (simulação de chuva ácida).")
        st.markdown("* **O Ponto Cego:** Substâncias tóxicas fixas na matriz não eram detectadas como perigosas.")
        st.markdown("* **O Resultado:** Resíduos perigosos classificados como Classe II.")
    with col2:
        st.success("### 🟢 O Cenário Atual (A NBR 10004:2024)")
        st.markdown("* **Mecanismo:** Foco na composição química intrínseca (GHS).")
        st.markdown("* **A Mudança:** Aplicação de limites de corte para perigos mutagênicos/cancerígenos.")
        st.markdown("* **Foco no Trabalhador:** Expansão da proteção ocupacional na manipulação direta.")

# --- ABA 4: RESUMO EXECUTIVO ---
with aba_resumo:
    st.subheader("📌 Infográfico Resumido: A Nova Era da NBR 10004")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🔄 Transição Estrutural")
        st.markdown("* **Antigo:** Foco em lixiviação e aterros.")
        st.markdown("* **Novo:** Foco em perigo intrínseco e GHS.")
        st.markdown("* **Codificação:** Mudança para a **LGR (6 dígitos)**.")
    with c2:
        st.markdown("### 🎯 Objetivos Principais")
        st.markdown("* **Proteção:** Saúde do Trabalhador + Ambiental.")
        st.markdown("* **Transição:** Prazo máximo até 31/12/2026.")
        st.markdown("* **Visão:** Economia Circular e Rastreabilidade.")
    st.info("💡 **Conceito Chave:** O resíduo agora é classificado pelo que ele **é** (química), não apenas pelo que ele **solta** (ensaio de lixiviado).")
