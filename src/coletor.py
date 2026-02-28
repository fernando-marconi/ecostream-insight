import os
import requests
import pandas as pd
from datetime import datetime

# Teste de leitura do Token
TOKEN = os.getenv("WAQI_TOKEN")
CIDADES = ["sao-paulo", "rio-de-janeiro", "curitiba", "manaus", "beijing", "delhi", "new-york", "mexico-city", "oslo", "reykjavik"]

def coletar_e_salvar():
    if not TOKEN:
        print("ERRO CRITICO: Token WAQI_TOKEN nao encontrado nas variaveis de ambiente!")
        return

    os.makedirs('data', exist_ok=True)
    caminho_arquivo = "data/historico_ar.csv"
    lista_novos_dados = []

    print(f"Iniciando coleta para {len(CIDADES)} cidades...")

    for cidade in CIDADES:
        try:
            url = f"https://api.waqi.info/feed/{cidade}/?token={TOKEN}"
            response = requests.get(url, timeout=15)
            dados = response.json()
            
            if response.status_code == 200 and dados.get('status') == 'ok':
                aqi = dados['data'].get('aqi')
                lista_novos_dados.append({
                    "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "cidade": cidade,
                    "aqi": aqi
                })
                print(f"Sucesso: {cidade} ({aqi})")
            else:
                print(f"Falha na cidade {cidade}: {dados.get('data', 'Sem detalhes')}")
        except Exception as e:
            print(f"Erro na conexao com {cidade}: {e}")

    if lista_novos_dados:
        df_novos = pd.DataFrame(lista_novos_dados)
        if not os.path.isfile(caminho_arquivo):
            df_novos.to_csv(caminho_arquivo, index=False)
        else:
            df_novos.to_csv(caminho_arquivo, mode='a', header=False, index=False)
        print("Processo concluido com sucesso.")
    else:
        print("ALERTA: Nenhum dado foi coletado. Verifique o Token ou a conexao da API.")

if __name__ == "__main__":
    coletar_e_salvar()