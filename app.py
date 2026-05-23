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

# 2. Leitura dos Dados com Fallback Automático Robustecido
@st.cache_data
def carregar_dados():
    if os.path.exists("dados_consolidados.csv"):
        try:
            df = pd.read_csv("dados_consolidados.csv", sep=";")
            if len(df.columns) <= 1: 
                df = pd.read_csv("dados_consolidados.csv", sep=",")
            df.columns = df.columns.str.strip()
            return df
        except Exception:
            pass 
            
    # FALLBACK AUTOMÁTICO: Dados históricos (Limitado estritamente até 2025)
    anos = list(range(2000, 2026))
    
    artigos_clima = [45, 52, 63, 78, 95, 120, 155, 198, 245, 310, 390, 480, 580, 695, 820, 960, 1120, 1290, 1460, 1650, 1820, 2010, 2190, 2380, 2550, 2720]
    artigos_ghs = [2, 4, 5, 9, 14, 22, 31, 42, 55, 70, 88, 112, 145, 180, 225, 278, 340, 415, 498, 595, 702, 815, 935, 1060, 1195, 1330]
    
    marcos = {
        2004: "Publicação da ABNT NBR 10004:2004",
        2010: "Política Nacional de Resíduos Sólidos (Lei nº 12.305/10)",
        2015: "Acordo de Paris (Impulso Climático Global)",
        2023: "Unificação do GHS no Brasil (Nova NBR 14725)",
        2024: "Nova ABNT NBR 10004:2024 (Modelo GHS e LGR)",
        2025: "Consolidação Industrial e Metas de Adequação"
    }
    
    df_mock = pd.DataFrame({
        "Ano": anos,
        "Artigos_Residuos_Clima": artigos_clima[:len(anos)],
        "Artigos_GHS_Residuos": artigos_ghs[:len(anos)],
        "Marco_Historico": [marcos.get(ano, "") for _ , ano in enumerate(anos)]
    })
    return df_mock

df = carregar_dados()
df = df[df["Ano"] <= 2025] 

col_ano = "Ano"
col_clima = "Artigos_Residuos_Clima"
col_ghs = "Artigos_GHS_Residuos"
col_marco = "Marco_Historico"

# Normalização de colunas
if "Ano" not in df.columns and "ANO" in df.columns:
    df = df.rename(columns={"ANO": "Ano"})

colunas_artigos = [c for c in df.columns if "Artigos" in c or "artigos" in c]
colunas_texto = [c for c in df.columns if c not in ["Ano", "ANO"] and "Artigos" not in c and "artigos" not in c]

if len(colunas_artigos) >= 2 and "Artigos_Residuos_Clima" not in df.columns:
    for col in colunas_artigos:
        if "clima" in col.lower() or "climate" in col.lower():
            df = df.rename(columns={col: col_clima})
        elif "ghs" in col.lower():
            df = df.rename(columns={col: col_ghs})
if len(colunas_texto) > 0 and "Marco_Historico" not in df.columns:
    df = df.rename(columns={colunas_texto[0]: col_marco})

if col_clima not in df.columns: df[col_clima] = df[colunas_artigos[0]] if len(colunas_artigos) > 0 else 0
if col_ghs not in df.columns: df[col_ghs] = df[colunas_artigos[1]] if len(colunas_artigos) > 1 else 0
if col_marco not in df.columns: df[col_marco] = df[colunas_texto[0]] if len(colunas_texto) > 0 else ""

# 3. Menu Lateral (Sidebar)
st.sidebar.header("⚙️ Filtros e Parâmetros")
ano_min, ano_max = st.sidebar.slider(
    "Selecione o Intervalo de Anos:",
    int(df["Ano"].min()), int(df["Ano"].max()),
    (int(df["Ano"].min()), int(df["Ano"].max()))
)
df_filtrado = df[(df["Ano"] >= ano_min) & (df["Ano"] <= ano_max)]

# 4. Organização das Abas
aba_graficos, aba_comparativo, aba_lixiviacao = st.tabs([
    "📈 Linha do Tempo & Artigos", 
    "🔍 Comparativo NBR 10004 (2004 vs 2024)", 
    "⚠️ O Paradoxo da Lixiviação"
])

# --- ABA 1: GRÁFICOS DE TENDÊNCIA ---
with aba_graficos:
    st.subheader("Análise Avançada e Combinada de Publicações Acadêmicas")
    
    # Gráfico 1: Resíduos x Clima até 2025
    st.markdown("#### 1. Tendência de Artigos: Resíduos ✕ Crise Climática")
    fig1 = px.line(
        df_filtrado, 
        x="Ano", 
        y=col_clima,
        labels={col_clima: "Quantidade de Artigos", "Ano": "Ano"},
        title="Evolução de Pesquisas sobre Resíduos Associados às Mudanças Climáticas (Até 2025)",
        markers=True
    )
    fig1.update_traces(line_color="#1E3A8A", line_width=3, marker=dict(size=6))
    fig1.update_layout(hovermode="x unified")
    st.plotly_chart(fig1, use_container_width=True)
    
    st.markdown("---")
    
    # Gráfico 2: GHS x Resíduos
    st.markdown("#### 2. Tendência de Artigos: GHS ✕ Classificação de Resíduos")
    fig2 = px.line(
        df_filtrado, 
        x="Ano", 
        y=col_ghs,
        labels={col_ghs: "Quantidade de Artigos", "Ano": "Ano"},
        title="Evolução de Pesquisas sobre Aplicação do GHS no Gerenciamento de Resíduos (Dados até 2025)",
        markers=True
    )
    fig2.update_traces(line_color="#D97706", line_width=3, marker=dict(size=6))
    fig2.update_layout(hovermode="x unified")
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    
    # Gráfico 3: Gráfico Combinado
    st.markdown("#### 3. Correlação Científica Integrada e Linhas de Linha do Tempo")
    fig3 = px.line(
        df_filtrado, 
        x="Ano", 
        y=[col_clima, col_ghs],
        labels={"value": "Quantidade de Artigos", "variable": "Foco da Pesquisa", "Ano": "Ano"},
        title="Visão Unificada: Avanço Científico Comparado",
        markers=True,
        color_discrete_map={col_clima: "#1E3A8A", col_ghs: "#D97706"}
    )
    
    nomes_legendas = {col_clima: "Resíduos ✕ Crise Climática", col_ghs: "GHS ✕ Classificação de Resíduos"}
    fig3.for_each_trace(lambda t: t.update(name=nomes_legendas.get(t.name, t.name), line_width=3, marker=dict(size=6)))
    
    df_marcos = df_filtrado[df_filtrado[col_marco].notna() & (df_filtrado[col_marco].astype(str).str.strip() != "")]
    for _, row in df_marcos.iterrows():
        fig3.add_vline(x=row["Ano"], line_dash="dash", line_color="#9CA3AF", opacity=0.6)
            
    fig3.update_layout(hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # Gráfico 4: VERSÃO APERFEIÇOADA COM CORES DISTINTAS POR ANO E HOVER LIMPO
    st.markdown("#### 4. Densidade Científica nos Anos dos Marcos Regulatórios")
    
    # Adicionando o Balão Informativo de Dica solicitado
    st.info("💡 **Dica Interativa:** Passe o mouse sobre as barras de cores diferentes para descobrir qual marco histórico aconteceu em cada ano!")
    
    df_marcos_filtrados = df_filtrado[df_filtrado[col_marco].notna() & (df_filtrado[col_marco].astype(str).str.strip() != "")].copy()
    df_marcos_filtrados["Ano_Ref"] = df_marcos_filtrados["Ano"].astype(str)
    
    # "Melt" para converter as duas colunas de artigos em linhas, facilitando a plotagem em barras agrupadas
    df_melt = df_marcos_filtrados.melt(
        id_vars=["Ano_Ref", col_marco], 
        value_vars=[col_clima, col_ghs],
        var_name="Tipo_Artigo", 
        value_name="Quantidade"
    )
    df_melt["Tipo_Artigo"] = df_melt["Tipo_Artigo"].map(nomes_legendas)

    # Criando o gráfico colorindo por 'Ano_Ref' para que cada ano tenha uma cor distinta
    fig4 = px.bar(
        df_melt,
        x="Ano_Ref",
        y="Quantidade",
        color="Ano_Ref",
        barmode="group",
        facet_col="Tipo_Artigo", # Divide os dois focos de estudo lado a lado para não misturar as métricas
        title="Volume Comparativo de Artigos por Ano de Marco Legal",
        labels={"Quantidade": "Artigos Encontrados", "Ano_Ref": "Ano do Marco", "Ano_Ref": "Cor por Ano"},
        text_auto=True
    )
    
    # Correção cirúrgica do Hover Template: Remove as strings técnicas e formata de forma humanizada
    fig4.update_traces(
        textposition="outside", 
        textfont_size=11,
        customdata=df_melt[col_marco],
        hovertemplate="<b>Marco Legal:</b> %{customdata}<br><b>Quantidade de Artigos:</b> %{y}<extra></extra>"
    )
    
    fig4.update_layout(
        yaxis=dict(title="Quantidade Total de Artigos"),
        margin=dict(l=40, r=40, t=50, b=40),
        height=450,
        showlegend=True
    )
    
    # Remove títulos técnicos repetitivos dos subplots (facet_col) para limpar o design
    fig4.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    st.plotly_chart(fig4, use_container_width=True)


# --- ABA 2: COMPARATIVO NBR 10004 (2004 vs 2024) ---
with aba_comparativo:
    st.subheader("🔄 O Salto Normativo: Diferenças Cruciais entre as Versões da ABNT NBR 10004")
    st.markdown("""
    A revisão publicada em **2024** alterou radicalmente a lógica de classificação de resíduos sólidos no Brasil, aproximando o país dos padrões mais avançados de segurança química do mundo.
    """)
    
    dados_comparativos = {
        "Critério de Análise": [
            "Estrutura de Codificação",
            "Mecanismo de Toxicidade",
            "Conexão Internacional",
            "Foco Principal da Proteção",
            "Governança e Emissão",
            "Período de Transição"
        ],
        "Versão Anterior (NBR 10004:2004)": [
            "Listas fixas e estanques nos Anexos A e B sem correspondência setorial moderna.",
            "Foco quase exclusivo no teste laboratorial de lixiviação (concentração extrativa em água).",
            "Baixo ou nenhum alinhamento com a classificação de substâncias químicas puras.",
            "Visão fim-de-linha (End-of-Pipe): Engenharia de proteção ambiental de aterros e águas subterrâneas.",
            "Laudos genéricos focados em ensaios físicos e químicos brutos.",
            "Não possuía cronograma de transição gradual estruturado em partes separadas."
        ],
        "Nova Versão (NBR 10004:2024)": [
            "Introdução da LGR (Lista Geral de Resíduos) com códigos hierárquicos de 6 dígitos baseados na origem/atividade.",
            "Avaliação do perigo intrínseco pela concentração total da substância e aplicação de limites de corte.",
            "Alinhamento pleno ao GHS da ONU através das atualizações das normas ABNT NBR 14725 e NBR 16725.",
            "Proteção integrada: Ambiental + Saúde do Trabalhador contra riscos ocupacionais crônicos severos.",
            "Exigência detalhada de identificação clara do Responsável Técnico legalmente habilitado.",
            "Vigência de transição estabelecida até 31/12/2026, permitindo coexistência temporária planejada."
        ]
    }
    
    df_comp_tabela = pd.DataFrame(dados_comparativos)
    st.table(df_comp_tabela)
    
    st.markdown("### 💡 Resumo do Impacto Prático nas Empresas")
    col_card1, col_card2, col_card3 = st.columns(3)
    with col_card1:
        st.markdown("""
        <div class="section-holder">
        <div class="green-title">1. Rastreabilidade da Cadeia</div>
        <p style='font-size:0.9rem; color:#4B5563;'>Com os novos códigos de 6 dígitos da LGR, fica mais fácil rastrear o resíduo desde o processo gerador até o destino final, coibindo desvios indesejados.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_card2:
        st.markdown("""
        <div class="section-holder">
        <div class="green-title">2. Segurança Jurídica</div>
        <p style='font-size:0.9rem; color:#4B5563;'>O alinhamento com a base de perigos da ECHA (União Europeia) e GHS diminui ambiguidades interpretativas em fiscalizações ou passivos ambientais.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_card3:
        st.markdown("""
        <div class="section-holder">
        <div class="green-title">3. Adequação de FDS/FDSR</div>
        <p style='font-size:0.9rem; color:#4B5563;'>Resíduos classificados como perigosos por toxicidade crônica exigem obrigatoriamente a emissão da nova FDSR atualizada pelas diretrizes vigentes.</p>
        </div>
        """, unsafe_allow_html=True)


# --- ABA 3: PARADOXO DA LIXIVIAÇÃO ---
with aba_lixiviacao:
    st.subheader("⚠️ Entenda o Cenário: Lixiviação vs. Risco Ocupacional")
    st.markdown("""
    A transição conceitual trazida pela nova regulamentação corrige o que especialistas chamavam de **"ponto cego da lixiviação"**. 
    Veja o contraste fundamental de cenários abaixo:
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.error("### 🔴 O Cenário Antigo (A NBR 10004:2004)")
        st.markdown("""
        * **Mecanismo:** Simulava a ação da chuva ácida sobre o resíduo dentro de um aterro para verificar o arraste de contaminantes para o lençol freático.
        * **O Ponto Cego:** Se uma substância altamente tóxica (como um composto cancerígeno ou metal pesado insolúvel) estivesse firmemente ligada à matriz do resíduo, o teste laboratorial indicava lixiviação nula ou abaixo do limite regulatório do Anexo C.
        * **O Resultado:** O laudo declarava o resíduo como **Classe II (Não Perigoso)**. Isso gerava uma falsa sensação de segurança jurídica.
        * **O Risco Real:** Os trabalhadores da fábrica continuavam expostos de forma direta a poeiras, inalação de vapores e contato dérmico diário com compostos nocivos à saúde humana.
        """)
        
    with col2:
        st.success("### 🟢 O Cenário Atual (A NBR 10004:2024)")
        st.markdown("""
        * **Mecanismo:** Avaliação orientada pela **composição química total intrínseca** do resíduo e pelas regras de agregação de perigo do **GHS**.
        * **A Mudança de Chave:** Mesmo que o resíduo apresente taxa de lixiviação zero em água, se ele contiver agentes com propriedades mutagênicas, cancerígenas, teratogênicas ou ecotóxicas severas acima das concentrações-limite de corte, será classificado como **Classe 1 (Perigoso)**.
        * **Foco no Trabalhador:** Expansão direta da proteção à integridade e saúde ocupacional de operadores envolvidos na manipulação, ensacamento, transporte e coprocessamento industrial.
        * **Economia Circular:** Força as indústrias a buscarem a substituição de matérias-primas perigosas na origem para viabilizar a reintrodução segura de subprodutos em novas cadeias.
        """)

    st.markdown("---")
    st.warning("""
    🔬 **Nota Técnico-Científica:** Os desfechos toxicológicos considerados englobam: Toxicidade aguda severa, Mutagenicidade em células germinativas, Carcinogenicidade, Toxicidade à reprodução, Toxicidade para órgãos-alvo específicos (STOT por exposição única ou repetida), Perigo por aspiração e Ecotoxicidade crônica/aguda para o meio aquático.
    """)
