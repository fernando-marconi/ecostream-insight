import os
import pandas as pd
import streamlit as st
import plotly.express as px

# Configuracao da Pagina
st.set_page_config(page_title="EcoStream Insight", layout="wide")

st.title("EcoStream Insight: Qualidade do Ar")
st.markdown("Monitoramento global automatizado via GitHub Actions.")

PATH_DATA = "data/historico_ar.csv"
PATH_PREPARADO = "data/dados_preparados.csv"

# Processamento Principal
if os.path.exists(PATH_DATA):
    try:
        df = pd.read_csv(PATH_DATA)
        df['aqi'] = pd.to_numeric(df['aqi'], errors='coerce')
        df = df.dropna(subset=['aqi'])
        
        if not df.empty:
            df['data_hora'] = pd.to_datetime(df['data_hora'])
            df = df.sort_values(by=['cidade', 'data_hora'])
            
            # Calculo de tendencia para o grafico principal
            df['tendencia_aqi'] = df.groupby('cidade')['aqi'].transform(
                lambda x: x.rolling(window=3, min_periods=1).mean()
            )

            # Situacao Atual
            st.subheader("Situacao Atual das Cidades")
            df_atual = df.sort_values('data_hora').groupby('cidade').last().reset_index()
            
            fig_bar = px.bar(
                df_atual, 
                x='cidade', 
                y='aqi', 
                color='aqi',
                title="Indice de Qualidade do Ar (AQI) - Atual",
                color_continuous_scale='RdYlGn_r',
                text_auto=True
            )
            st.plotly_chart(fig_bar, use_container_width=True)

            st.divider()

            # Analise Historica e Comparativo de Tendencia
            col1, col2 = st.columns([1, 2])
            
            with col1:
                cidade_sel = st.selectbox("Selecione uma cidade:", sorted(df['cidade'].unique()))
                df_cidade = df[df['cidade'] == cidade_sel]
                st.metric(label="Ultimo AQI", value=int(df_cidade.iloc[-1]['aqi']))
            
            with col2:
                fig_line = px.line(
                    df_cidade, 
                    x='data_hora', 
                    y=['aqi', 'tendencia_aqi'],
                    markers=True,
                    title="Evolucao e Tendencia Historica",
                    labels={'value': 'AQI', 'variable': 'Tipo'}
                )
                fig_line.data[0].name = "Valor Real"
                fig_line.data[1].name = "Tendencia"
                fig_line.data[1].line.dash = 'dot'
                st.plotly_chart(fig_line, use_container_width=True)

            # Inspecao da Materia-Prima da IA (Recuperado)
            if os.path.exists(PATH_PREPARADO):
                st.divider()
                with st.expander("Visualizar Dados Processados (Dataset da IA)"):
                    df_prep = pd.read_csv(PATH_PREPARADO)
                    st.markdown("Esta tabela exibe os atributos (features) que o modelo de IA utilizara:")
                    # Exibe as colunas tecnicas: periodo_dia, tendencia_aqi e variacao_imediata
                    st.dataframe(df_prep.tail(15), use_container_width=True)
            else:
                st.info("Arquivo de dados preparados nao detectado. Execute o processador.py localmente.")

    except Exception as e:
        st.error("Erro no processamento: " + str(e))
else:
    st.error("Arquivo historico_ar.csv nao encontrado.")