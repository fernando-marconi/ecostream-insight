import os
import pandas as pd
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv

# Configurações Iniciais
st.set_page_config(page_title="EcoStream Insight", layout="wide")
load_dotenv()

PATH_DATA = "data/historico_ar.csv"

st.title("EcoStream Insight: Qualidade do Ar em Tempo Real")
st.markdown("Dados coletados automaticamente via API WAQI e processados por GitHub Actions.")

# Verificação e Leitura de Dados
if os.path.exists(PATH_DATA):
    try:
        # Lendo o CSV gerado pelo robô
        df = pd.read_csv(PATH_DATA)
        df['data_hora'] = pd.to_datetime(df['data_hora'])
        
        # Metricas em Destaque
        ultimas_leituras = df.sort_values('data_hora').groupby('cidade').last().reset_index()
        cidade_mais_poluida = ultimas_leituras.loc[ultimas_leituras['aqi'].idxmax()]
        cidade_mais_limpa = ultimas_leituras.loc[ultimas_leituras['aqi'].idxmin()]

        m1, m2, m3 = st.columns(3)
        m1.metric("Cidades Monitoradas", len(ultimas_leituras['cidade'].unique()))
        m2.metric("Mais Poluída (AQI)", cidade_mais_poluida['cidade'].title(), int(cidade_mais_poluida['aqi']), delta_color="inverse")
        m3.metric("Mais Limpa (AQI)", cidade_mais_limpa['cidade'].title(), int(cidade_mais_limpa['aqi']))

        st.divider()

        # Visualizacao Grafica
        col_esq, col_dir = st.columns([2, 1])

        with col_esq:
            st.subheader("Comparativo Atual entre Cidades")
            fig_bar = px.bar(
                ultimas_leituras.sort_values('aqi', ascending=False),
                x='aqi', y='cidade', orientation='h',
                color='aqi', color_continuous_scale='RdYlGn_r',
                labels={'aqi': 'Índice AQI', 'cidade': 'Cidade'}
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_dir:
            st.subheader("Histórico por Cidade")
            cidade_foco = st.selectbox("Selecione para ver o histórico:", sorted(df['cidade'].unique()))
            df_foco = df[df['cidade'] == cidade_foco]
            fig_line = px.line(df_foco, x='data_hora', y='aqi', markers=True)
            st.plotly_chart(fig_line, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao processar o banco de dados: {e}")
else:
    st.info("Aguardando a próxima sincronização do robô para exibir os dados.")