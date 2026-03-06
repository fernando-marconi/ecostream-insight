import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN_WAQI")

def processar_dados():
    caminho_bruto = "data/historico_ar.csv"
    caminho_limpo = "data/dados_preparados.csv"

    if not os.path.exists(caminho_bruto):
        print("Erro: Arquivo bruto nao encontrado.")
        return

    # Carregamento e Limpeza
    df = pd.read_csv(caminho_bruto)
    df['aqi'] = pd.to_numeric(df['aqi'], errors='coerce')
    df = df.dropna(subset=['aqi'])
    df['data_hora'] = pd.to_datetime(df['data_hora'])
    
    # Ordenar por cidade e tempo
    df = df.sort_values(by=['cidade', 'data_hora'])

    # Engenharia de Atributos (Ajuste de Horarios)
    df['hora'] = df['data_hora'].dt.hour
    
    # Definicao dos periodos:
    # 0-5: Madrugada | 6-11: Manha | 12-17: Tarde | 18-23: Noite
    bins = [-1, 5, 11, 17, 23] 
    labels = ['Madrugada', 'Manhã', 'Tarde', 'Noite']
    df['periodo_dia'] = pd.cut(df['hora'], bins=bins, labels=labels)

    # Calculos de Tendencia e Variacao
    # Media movel (Tendencia) - Usando min_periods=1 para evitar NaNs
    df['tendencia_aqi'] = df.groupby('cidade')['aqi'].transform(
        lambda x: x.rolling(window=3, min_periods=1).mean()
    )
    
    # Variacao em relacao a leitura anterior
    df['variacao_imediata'] = df.groupby('cidade')['aqi'].diff().fillna(0)

    # Salvamento
    df.to_csv(caminho_limpo, index=False)
    print("Processamento concluido com as novas regras de horários.")
    print("Arquivo gerado: " + caminho_limpo)

if __name__ == "__main__":
    processar_dados()