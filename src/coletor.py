import os
import requests
import pandas as pd
from datetime import datetime

TOKEN = os.getenv("WAQI_TOKEN")
CIDADES = ["sao-paulo", "rio-de-janeiro", "curitiba", "manaus", "beijing", "delhi", "new-york", "mexico-city", "oslo", "reykjavik"]

def coletar_e_salvar():
    # Cria a pasta se ela sumir por algum motivo no ambiente temporário
    os.makedirs('data', exist_ok=True)
        
    caminho_arquivo = "data/historico_ar.csv"
    lista_novos_dados = []

    print(f"Iniciando coleta para {len(CIDADES)} cidades...")

    for cidade in CIDADES:
        try:
            url = f"https://api.waqi.info/feed/{cidade}/?token={TOKEN}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data_json = response.json().get('data')
                if data_json and isinstance(data_json, dict):
                    aqi = data_json.get('aqi')
                    # Verifica se o AQI é um número válido antes de salvar
                    if aqi is not None:
                        lista_novos_dados.append({
                            "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "cidade": cidade,
                            "aqi": aqi
                        })
                        print(f"Sucesso: {cidade} ({aqi})")
            else:
                print(f"Erro API {cidade}: Status {response.status_code}")
        except Exception as e:
            print(f"Falha critica em {cidade}: {str(e)}")

    if lista_novos_dados:
        df_novos = pd.DataFrame(lista_novos_dados)
        if not os.path.isfile(caminho_arquivo):
            df_novos.to_csv(caminho_arquivo, index=False)
        else:
            df_novos.to_csv(caminho_arquivo, mode='a', header=False, index=False)
        print(f"Arquivo atualizado com {len(lista_novos_dados)} novas linhas.")
    else:
        print("ALERTA: Nenhum dado foi coletado. O arquivo nao sera gerado.")
        # Cria um arquivo vazio apenas para o git add nao dar erro fatal
        if not os.path.isfile(caminho_arquivo):
            with open(caminho_arquivo, 'w') as f:
                f.write("data_hora,cidade,aqi\n")

if __name__ == "__main__":
    coletar_e_salvar()