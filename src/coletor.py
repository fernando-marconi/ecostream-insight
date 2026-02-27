import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("WAQI_TOKEN")

# Lista de cidades estratégica para o portfólio
CIDADES = [
    "sao-paulo", "rio-de-janeiro", "curitiba", "manaus", 
    "beijing", "delhi", "new-york", "mexico-city", 
    "oslo", "reykjavik"
]

def coletar_e_salvar():
    caminho_arquivo = "data/historico_ar.csv"
    lista_novos_dados = []

    for cidade in CIDADES:
        url = f"https://api.waqi.info/feed/{cidade}/?token={TOKEN}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data_json = response.json().get('data')
                
                # Verificação extra: algumas cidades podem falhar momentaneamente
                if data_json and isinstance(data_json, dict):
                    aqi = data_json.get('aqi')
                    
                    lista_novos_dados.append({
                        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "cidade": cidade,
                        "aqi": aqi
                    })
                    print(f"Sucesso: {cidade} - AQI: {aqi}")
        except Exception as e:
            print(f"Erro ao coletar {cidade}: {e}")

    # Se coletamos algo, salvamos de uma vez só (mais eficiente)
    if lista_novos_dados:
        df_novos = pd.DataFrame(lista_novos_dados)
        if not os.path.isfile(caminho_arquivo):
            df_novos.to_csv(caminho_arquivo, index=False)
        else:
            df_novos.to_csv(caminho_arquivo, mode='a', header=False, index=False)

if __name__ == "__main__":
    coletar_e_salvar()