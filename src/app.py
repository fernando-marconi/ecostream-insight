import os
import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração da Página
st.set_page_config(page_title="EcoStream Insight", layout="wide")

st.title("EcoStream Insight: Qualidade do Ar")
st.markdown("Monitoramento global automatizado via GitHub Actions.")

# Caminho para o arquivo de dados gerado pelo robô
PATH_DATA = "data/historico_ar.csv"

# Verificação de existência do arquivo físico
if os.path.exists(PATH_DATA):
    try:
        # Carregando os dados coletados
        df = pd.read_csv(PATH_DATA)
        
        # Limpeza básica: remove linhas vazias para evitar erros no gráfico
        df = df.dropna()

        if not df.empty:
            # Converte a coluna de data para o formato de tempo do Python
            df['data_hora'] = pd.to_datetime(df['data_hora'])
            
            # SITUAÇÃO ATUAL
            st.subheader("Situação Atual das Cidades")
            
            # Obtém apenas a última leitura registrada para cada cidade
            df_atual = df.sort_values('data_hora').groupby('cidade').last().reset_index()
            
            # Gráfico de Barras com escala de cores (Verde para bom, Vermelho para ruim)
            fig_bar = px.bar(
                df_atual, 
                x='cidade', 
                y='aqi', 
                color='aqi',
                title="Índice de Qualidade do Ar (AQI) - Última Coleta",
                color_continuous_scale='RdYlGn_r',
                text_auto=True
            )
            
            # Atualização das legendas e eixos
            fig_bar.update_layout(xaxis_title="Cidade", yaxis_title="Índice AQI")
            st.plotly_chart(fig_bar, use_container_width=True)

            st.divider()

            # SEÇÃO DE ANÁLISE HISTÓRICA POR CIDADE
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # Menu de seleção com as cidades disponíveis no histórico
                cidades_lista = sorted(df['cidade'].unique())
                cidade_sel = st.selectbox("Selecione uma cidade para detalhamento:", cidades_lista)
                
                # Filtra os dados apenas da cidade selecionada
                df_cidade = df[df['cidade'] == cidade_sel]
                
                # Exibe a métrica da última medição dessa cidade específica
                ultimo_valor = int(df_cidade.iloc[-1]['aqi'])
                st.metric(label=f"Último AQI em {cidade_sel.title()}", value=ultimo_valor)
            
            with col2:
                # Gráfico de linha mostrando a evolução do AQI ao longo do tempo
                fig_line = px.line(
                    df_cidade, 
                    x='data_hora', 
                    y='aqi', 
                    markers=True,
                    title=f"Evolução Histórica: {cidade_sel.title()}"
                )
                fig_line.update_layout(xaxis_title="Data e Hora da Coleta", yaxis_title="Índice AQI")
                st.plotly_chart(fig_line, use_container_width=True)
            
            # Expansor para visualização da tabela de dados brutos
            with st.expander("Clique para ver a tabela completa de dados brutos"):
                st.dataframe(df.sort_values('data_hora', ascending=False), use_container_width=True)

        else:
            st.warning("O arquivo de dados foi encontrado, mas ainda não contém registros válidos.")

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar os dados: {e}")
        st.info("Verifique se o arquivo CSV possui as colunas: data_hora, cidade, aqi")
else:
    st.error("O arquivo 'data/historico_ar.csv' não foi detectado no sistema local.")
    st.info("Certifique-se de que o robô do GitHub já executou com sucesso e faça um 'git pull'.")