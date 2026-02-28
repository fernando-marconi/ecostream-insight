import os
import requests
import pandas as pd
from datetime import datetime

# Buscando o token
TOKEN = os.environ.get("WAQI_TOKEN")

def coletar_e_salvar():
    # DIAGNÓSTICO DE TOKEN
    if not TOKEN:
        print("❌ ERRO: O sistema nao encontrou a variavel WAQI_TOKEN.")
        return
    else:
        print(f"✅ Token detectado (Inicia com: {TOKEN[:4]}...)")

    os.makedirs('data', exist_ok=True)
    caminho_arquivo = "data/historico_ar.csv"
    
    CIDADES = ["sao-paulo", "santos", "cubatao", "beijing", "delhi", "negotin", "new-york", "mexico-city", "oslo", "reykjavik"]
    lista_novos_dados = []

    for cidade in CIDADES:
        url = f"https://api.waqi.info/feed/{cidade}/?token={TOKEN}"
        try:
            response = requests.get(url, timeout=15)
            dados = response.json()
            if dados.get('status') == 'ok':
                aqi = dados['data'].get('aqi')
                lista_novos_dados.append({
                    "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "cidade": cidade,
                    "aqi": aqi
                })
                print(f"✓ {cidade}: {aqi}")
        except Exception as e:
            print(f"Error {cidade}: {e}")

    if lista_novos_dados:
        df = pd.DataFrame(lista_novos_dados)
        # Salva ou anexa ao CSV
        if not os.path.exists(caminho_arquivo):
            df.to_csv(caminho_arquivo, index=False)
        else:
            df.to_csv(caminho_arquivo, mode='a', header=False, index=False)
        print(f"🚀 Sucesso! {len(lista_novos_dados)} registros salvos.")

if __name__ == "__main__":
    coletar_e_salvar()