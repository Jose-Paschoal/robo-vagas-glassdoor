import streamlit as st
import pandas as pd
import plotly.express as px

# Configurações iniciais
st.set_page_config(page_title="Painel de Vagas de Dados", layout="wide")

# Título do App
st.title("📊 Painel de Vagas de Dados")

# Carrega os dados
df_original = pd.read_csv("vagas_glassdoor_tratado.csv")  # dados completos
df = df_original.copy()  # será filtrado conforme seleções

# FILTROS LATERAIS
st.sidebar.header("🔎 Filtros")

# Remoto
remoto = st.sidebar.checkbox("Mostrar apenas vagas remotas")
if remoto:
    df = df[df['remoto'] == 1]

# Estado
estados_disponiveis = sorted(df['estado'].dropna().unique())
estado_selecionado = st.sidebar.multiselect("Estado", estados_disponiveis)
if estado_selecionado:
    df = df[df['estado'].isin(estado_selecionado)]

# Região
regioes_disponiveis = sorted(df['regiao'].dropna().unique())
regiao_selecionada = st.sidebar.multiselect("Região", regioes_disponiveis)
if regiao_selecionada:
    df = df[df['regiao'].isin(regiao_selecionada)]

# Faixa salarial
faixas_salarial = sorted(df['faixa_salarial'].dropna().unique())
faixa_salario = st.sidebar.multiselect("Faixa salarial", faixas_salarial)
if faixa_salario:
    df = df[df['faixa_salarial'].isin(faixa_salario)]

# Faixa de publicação
faixa_publicacao = sorted(df['faixa_dias'].dropna().unique())
publicacao_selecionada = st.sidebar.multiselect("Publicado há (dias)", faixa_publicacao)
if publicacao_selecionada:
    df = df[df['faixa_dias'].isin(publicacao_selecionada)]

# MOSTRA RESULTADOS
st.markdown(f"### 📌 Total de vagas encontradas: {df.shape[0]}")
st.dataframe(df)

# GRÁFICO 1 – Vagas por Estado (visão geral, independente dos filtros)
# ➤ Usamos o df_original aqui para manter todos os estados visíveis
estado_contagem = df_original['estado'].value_counts().reset_index()
estado_contagem.columns = ['estado', 'quantidade']

fig1 = px.bar(estado_contagem,
              x='estado', y='quantidade',
              title="Distribuição de Vagas por Estado (Visão Geral)",
              labels={'quantidade': 'Número de Vagas', 'estado': 'Estado'})

st.plotly_chart(fig1, use_container_width=True)

# GRÁFICO 2 – Vagas por Região (filtrado)
fig2 = px.pie(df, names="regiao", title="Distribuição por Região")
st.plotly_chart(fig2, use_container_width=True)

# GRÁFICO 3 – Faixa Salarial (filtrado)
salario_contagem = df['faixa_salarial'].value_counts().reset_index()
salario_contagem.columns = ['faixa_salarial', 'count']

fig3 = px.bar(salario_contagem,
              x='faixa_salarial', y='count',
              title='Distribuição por Faixa Salarial')
st.plotly_chart(fig3, use_container_width=True)

# BOTÃO PARA DOWNLOAD
st.markdown("### 📥 Download dos dados filtrados")
st.download_button(
    label="Baixar como CSV",
    data=df.to_csv(index=False, encoding='utf-8-sig'),
    file_name='vagas_filtradas.csv',
    mime='text/csv'
)
