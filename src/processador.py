import pandas as pd
import os

def processar_dados():
    caminho_bruto = "data/historico_ar.csv"
    caminho_limpo = "data/dados_preparados.csv"

    if not os.path.exists(caminho_bruto):
        print("Erro: Arquivo bruto nao encontrado para processamento.")
        return

    # 1. Carregamento e Limpeza Inicial
    df = pd.read_csv(caminho_bruto)
    df['aqi'] = pd.to_numeric(df['aqi'], errors='coerce')
    df = df.dropna(subset=['aqi'])
    df['data_hora'] = pd.to_datetime(df['data_hora'])
    
    # Ordenar por cidade e tempo para os calculos fazerem sentido
    df = df.sort_values(by=['cidade', 'data_hora'])

    # 2. Engenharia de Atributos (Feature Engineering)
    
    # Extrair a hora do dia
    df['hora'] = df['data_hora'].dt.hour
    
    # Criar categorias de periodo do dia
    # 0-6: Madrugada, 6-12: Manha, 12-18: Tarde, 18-24: Noite
    bins = [0, 6, 12, 18, 24]
    labels = ['Madrugada', 'Manha', 'Tarde', 'Noite']
    df['periodo_dia'] = pd.cut(df['hora'], bins=bins, labels=labels, include_lowest=True)

    # 3. Calculos de Tendencia (Por Cidade)
    # Media movel das ultimas 3 coletas para suavizar picos isolados
    df['tendencia_aqi'] = df.groupby('cidade')['aqi'].transform(lambda x: x.rolling(window=3, min_periods=1).mean())
    
    # Variacao imediata (Diferenca entre a leitura atual e a anterior)
    df['variacao_imediata'] = df.groupby('cidade')['aqi'].diff().fillna(0)

    # 4. Salvar o "Dataset" Pronto para a IA
    df.to_csv(caminho_limpo, index=False)
    print(f"✅ Sucesso! Dados processados e salvos em: {caminho_limpo}")
    print(f"📈 Total de registros prontos: {len(df)}")

if __name__ == "__main__":
    processar_dados()