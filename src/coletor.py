import os
import requests
import pandas as pd
from datetime import datetime

TOKEN = os.getenv("WAQI_TOKEN")
CIDADES = ["sao-paulo", "rio-de-janeiro", "curitiba", "manaus", "beijing", "delhi", "new-york", "mexico-city", "oslo", "reykjavik"]

def coletar_e_salvar():
    # GARANTE QUE A PASTA DATA EXISTA NO SERVIDOR
    if not os.path.exists('data'):
        os.makedirs('data')
        
    caminho_arquivo = "data/historico_ar.csv"
    lista_novos_dados = []

    for cidade in CIDADES:
        url = f"https://api.waqi.info/feed/{cidade}/?token={TOKEN}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data_json = response.json().get('data')
                if data_json and isinstance(data_json, dict):
                    aqi = data_json.get('aqi')
                    lista_novos_dados.append({
                        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "cidade": cidade,
                        "aqi": aqi
                    })
        except Exception as e:
            print(f"Erro ao coletar {cidade}: {e}")

    if lista_novos_dados:
        df_novos = pd.DataFrame(lista_novos_dados)
        if not os.path.isfile(caminho_arquivo):
            df_novos.to_csv(caminho_arquivo, index=False)
        else:
            df_novos.to_csv(caminho_arquivo, mode='a', header=False, index=False)
        print("Dados salvos com sucesso.")

if __name__ == "__main__":
    coletar_e_salvar()