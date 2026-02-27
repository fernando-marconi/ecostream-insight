import os
import pandas as pd
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv

# Configuração da Página
st.set_page_config(page_title="EcoStream Insight", layout="wide")

# Carregamento de chaves
load_dotenv()

st.title("EcoStream Insight: Dashboard Global de Qualidade do Ar")

# Caminho do banco de dados
PATH_DATA = "data/historico_ar.csv"

# Lista de cidades que definimos no projeto
CIDADES_PROJETO = [
    "sao-paulo", "rio-de-janeiro", "curitiba", "manaus", 
    "beijing", "delhi", "new-york", "mexico-city", 
    "oslo", "reykjavik"
]

if os.path.exists(PATH_DATA):
    df = pd.read_csv(PATH_DATA)
    
    # Conversão de data para garantir ordenação correta
    df['data_hora'] = pd.to_datetime(df['data_hora'])
    
    # --- SEÇÃO 1: Ranking Geral ---
    st.subheader("Ranking Atual de Poluição")
    # Obtemos o último registro de cada cidade para comparar o agora
    df_ranking = df.sort_values('data_hora').groupby('cidade').last().reset_index()
    
    fig_ranking = px.bar(
        df_ranking.sort_values('aqi', ascending=False),
        x='aqi', y='cidade', orientation='h',
        color='aqi', color_continuous_scale='Reds',
        labels={'aqi': 'Índice AQI', 'cidade': 'Cidade'},
        title="Nível de AQI por Localidade (Maior = Mais Poluído)"
    )
    st.plotly_chart(fig_ranking, use_container_width=True)

    st.divider()

    # --- SEÇÃO 2: Análise Detalhada ---
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Filtros")
        cidade_sel = st.selectbox("Escolha uma cidade para histórico", CIDADES_PROJETO)
    
    with col2:
        df_cidade = df[df['cidade'] == cidade_sel]
        if not df_cidade.empty:
            fig_hist = px.line(
                df_cidade, x='data_hora', y='aqi', 
                markers=True, title=f"Evolução Temporal: {cidade_sel.title()}"
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info(f"Ainda não há dados históricos para {cidade_sel}.")

else:
    st.warning("Arquivo de dados não encontrado.")
    st.info("O robô de coleta automática ainda não gerou o primeiro arquivo CSV em 'data/historico_ar.csv'.")