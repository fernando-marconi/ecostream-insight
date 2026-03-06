import os
import pandas as pd
import streamlit as st
import plotly.express as px
import joblib
from groq import Groq
from dotenv import load_dotenv

# Carrega as variaveis do arquivo .env
load_dotenv()

# Configuracao da Pagina
st.set_page_config(page_title="EcoStream Insight", layout="wide")

# Busca a chave de forma segura
CHAVE_API_GROQ = os.getenv("GROQ_API_KEY")

# Valida se a chave existe
if not CHAVE_API_GROQ:
    st.error("Erro: Chave API nao encontrada. Verifique o arquivo .env")
    st.stop()

client = Groq(api_key=CHAVE_API_GROQ)

PATH_DATA = "data/historico_ar.csv"
PATH_PREPARADO = "data/dados_preparados.csv"
PATH_MODELO = "models/modelo_aqi.pkl"

def gerar_analise_llama(cidade, aqi_atual, previsao_futura):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {
                    "role": "system", 
                    "content": "Voce e um especialista ambiental. Forneca analises tecnicas em um unico paragrafo, sem saudacoes, sem emojis e sem numeracoes."
                },
                {
                    "role": "user", 
                    "content": f"Analise tecnica: {cidade}. AQI atual {aqi_atual}, previsto {previsao_futura}. Riscos e recomendacoes."
                }
            ],
            temperature=0.3,
        )
        return completion.choices[0].message.content
    except:
        return "Analise tecnica indisponivel no momento."

def prever_proximo_aqi(dados_atuais):
    if os.path.exists(PATH_MODELO):
        try:
            modelo = joblib.load(PATH_MODELO)
            mapeamento = {'Madrugada': 0, 'Manhã': 1, 'Tarde': 2, 'Noite': 3}
            periodo = str(dados_atuais['periodo_dia']).strip()
            periodo_num = mapeamento.get(periodo, 1)

            entrada = pd.DataFrame([{
                'aqi': dados_atuais['aqi'],
                'hora': dados_atuais['hora'],
                'periodo_num': periodo_num,
                'tendencia_aqi': dados_atuais['tendencia_aqi'],
                'variacao_imediata': dados_atuais['variacao_imediata']
            }])
            
            previsao = modelo.predict(entrada)[0]
            return round(previsao, 1)
        except:
            return None
    return None

st.title("EcoStream Insight: Qualidade do Ar")

if os.path.exists(PATH_DATA):
    try:
        df = pd.read_csv(PATH_DATA)
        df['aqi'] = pd.to_numeric(df['aqi'], errors='coerce')
        df = df.dropna(subset=['aqi'])
        
        if not df.empty:
            df['data_hora'] = pd.to_datetime(df['data_hora'])
            df = df.sort_values(by=['cidade', 'data_hora'])
            
            # Calculo de tendencia local idêntico ao seu código de referência
            df['tendencia_aqi'] = df.groupby('cidade')['aqi'].transform(
                lambda x: x.rolling(window=3, min_periods=1).mean()
            )

            # Grafico Superior
            df_atual = df.sort_values('data_hora').groupby('cidade').last().reset_index()
            fig_bar = px.bar(
                df_atual, x='cidade', y='aqi', color='aqi',
                title="Situacao Atual por Cidade",
                color_continuous_scale='RdYlGn_r',
                text_auto=True
            )
            st.plotly_chart(fig_bar, use_container_width=True)

            st.divider()

            col1, col2 = st.columns([1, 2])
            
            with col1:
                cidade_sel = st.selectbox("Selecione uma cidade:", sorted(df['cidade'].unique()))
                df_cidade = df[df['cidade'] == cidade_sel].copy()
                
                ultimo_valor = int(df_cidade.iloc[-1]['aqi'])
                st.metric(label="Ultimo AQI", value=ultimo_valor)

                previsao = None
                if os.path.exists(PATH_PREPARADO):
                    df_prep = pd.read_csv(PATH_PREPARADO)
                    df_prep_cidade = df_prep[df_prep['cidade'] == cidade_sel]
                    
                    if not df_prep_cidade.empty:
                        dados_ia = df_prep_cidade.iloc[-1]
                        previsao = prever_proximo_aqi(dados_ia)
                        
                        if previsao:
                            delta = round(previsao - ultimo_valor, 1)
                            st.metric(label="Previsao Proxima Hora", value=previsao, delta=delta, delta_color="inverse")
                            
                            st.divider()
                            st.subheader("Analise Tecnica Especializada")
                            analise = gerar_analise_llama(cidade_sel, ultimo_valor, previsao)
                            st.info(analise)

            with col2:
                # Grafico de Evolucao usando a coluna tendencia_aqi do DataFrame
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
                
                # Configuracao de Hover para mostrar dados corretamente
                fig_line.update_layout(hovermode="x unified")
                st.plotly_chart(fig_line, use_container_width=True)

    except Exception as e:
        st.error(f"Erro no processamento: {e}")
else:
    st.error("Arquivo historico_ar.csv nao encontrado.")