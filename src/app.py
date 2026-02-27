import os
import requests
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
from dotenv import load_dotenv

# Configuração da Página
st.set_page_config(page_title="EcoStream Insight", layout="wide")

# Carregamento de chaves
load_dotenv()
TOKEN = os.getenv("WAQI_TOKEN")

def salvar_historico(cidade, aqi):
    """Salva o AQI e o Timestamp em um CSV na pasta /data"""
    caminho_arquivo = "data/historico_ar.csv"
    novo_dado = pd.DataFrame([{
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cidade": cidade,
        "aqi": aqi
    }])
    
    # Se o arquivo não existir, cria com cabeçalho. Se existir, apenas adiciona a linha.
    if not os.path.isfile(caminho_arquivo):
        novo_dado.to_csv(caminho_arquivo, index=False)
    else:
        novo_dado.to_csv(caminho_arquivo, mode='a', header=False, index=False)

def buscar_dados_aqi(cidade):
    try:
        url = f"https://api.waqi.info/feed/{cidade}/?token={TOKEN}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('data')
    except Exception as e:
        st.error(f"Erro na requisição: {e}")
    return None

# Interface Streamlit
st.title("EcoStream Insight")

cidade = st.text_input("Digite o nome de uma cidade", "sao-paulo")

if st.button("Consultar e Salvar"):
    dados = buscar_dados_aqi(cidade)
    
    if dados:
        aqi = dados.get('aqi')
        
        # Salvando no CSV
        salvar_historico(cidade, aqi)
        st.success(f"Dados salvos com sucesso às {datetime.now().strftime('%H:%M:%S')}!")

        # Exibição das métricas
        st.metric(label=f"AQI atual em {cidade.title()}", value=aqi)
        
        # Visualização do Histórico Atual
        if os.path.exists("data/historico_ar.csv"):
            df_hist = pd.read_csv("data/historico_ar.csv")
            # Filtra apenas a cidade atual para o gráfico
            df_cidade = df_hist[df_hist['cidade'] == cidade]
            
            if not df_cidade.empty:
                fig = px.line(df_cidade, x="data_hora", y="aqi", title=f"Evolução do AQI: {cidade.title()}")
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Erro ao obter dados. Verifique o Token.")