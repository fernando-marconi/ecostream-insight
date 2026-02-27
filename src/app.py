import os
import pandas as pd
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv

# Configuracoes Iniciais
st.set_page_config(page_title="EcoStream Insight", layout="wide")
load_dotenv()

# Caminho do banco de dados
PATH_DATA = "data/historico_ar.csv"

# Cidades monitoradas
CIDADES_PROJETO = [
    "sao-paulo", "rio-de-janeiro", "curitiba", "manaus", 
    "beijing", "delhi", "new-york", "mexico-city", 
    "oslo", "reykjavik"
]

st.title("EcoStream Insight: Dashboard Global de Qualidade do Ar")

# Verificacao de Dados
if os.path.exists(PATH_DATA):
    df = pd.read_csv(PATH_DATA)
    df['data_hora'] = pd.to_datetime(df['data_hora'])
    
    # --- Ranking Geral ---
    st.subheader("Ranking Atual de Poluicao")
    # Pega o ultimo registro de cada cidade
    df_ranking = df.sort_values('data_hora').groupby('cidade').last().reset_index()
    
    fig_ranking = px.bar(
        df_ranking.sort_values('aqi', ascending=False),
        x='aqi', y='cidade', orientation='h',
        color='aqi', color_continuous_scale='Reds',
        labels={'aqi': 'Indice AQI', 'cidade': 'Cidade'},
        title="Nivel de AQI por Localidade (Maior = Mais Poluido)"
    )
    st.plotly_chart(fig_ranking, use_container_width=True)

    st.divider()

    # --- Analise Detalhada ---
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Filtros")
        cidade_sel = st.selectbox("Escolha uma cidade para historico", CIDADES_PROJETO)
    
    with col2:
        df_cidade = df[df['cidade'] == cidade_sel]
        if not df_cidade.empty:
            fig_hist = px.line(
                df_cidade, x='data_hora', y='aqi', 
                markers=True, title=f"Evolucao Temporal: {cidade_sel.title()}"
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info(f"Aguardando dados para {cidade_sel}.")
else:
    st.warning("Arquivo de dados nao encontrado.")
    st.info("O robo de coleta automatica ainda nao gerou o arquivo CSV.")