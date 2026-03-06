import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

def treinar_modelo():
    caminho_dados = "data/dados_preparados.csv"
    caminho_modelo = "models/modelo_aqi.pkl"
    
    if not os.path.exists(caminho_dados):
        print("Erro: Arquivo de dados preparados não encontrado.")
        return

    # Carregamento dos dados
    df = pd.read_csv(caminho_dados)
    
    # Criar a coluna alvo: AQI da próxima hora
    df['aqi_futuro'] = df.groupby('cidade')['aqi'].shift(-1)
    
    # Remover linhas sem o valor futuro (últimas coletas)
    df = df.dropna(subset=['aqi_futuro'])

    # Mapeamento para números com acentuação correta
    mapeamento_periodo = {
        'Madrugada': 0, 
        'Manhã': 1, 
        'Tarde': 2, 
        'Noite': 3
    }
    
    # Aplicar o mapeamento e garantir que não fiquem valores nulos
    df['periodo_num'] = df['periodo_dia'].map(mapeamento_periodo)
    df = df.dropna(subset=['periodo_num'])

    # Seleção de Atributos para a IA
    X = df[['aqi', 'hora', 'periodo_num', 'tendencia_aqi', 'variacao_imediata']]
    y = df['aqi_futuro']

    # Treinamento
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Iniciando treinamento do modelo Random Forest...")
    modelo = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    # Salvamento do Modelo
    if not os.path.exists('models'):
        os.makedirs('models')
        
    joblib.dump(modelo, caminho_modelo)
    
    # Métrica de desempenho
    score = modelo.score(X_test, y_test)
    print("Modelo treinado com sucesso.")
    print("Precisão do modelo (R2 Score): " + str(round(score, 4)))
    print("Arquivo salvo em: " + caminho_modelo)

if __name__ == "__main__":
    treinar_modelo()