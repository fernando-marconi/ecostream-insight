# EcoStream Insight: Monitoramento Preditivo de Ar

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Sobre o Projeto
O EcoStream Insight e uma plataforma inteligente de monitoramento ambiental. O sistema coleta dados em tempo real de sensores globais de qualidade do ar, utiliza modelos de redes neurais para prever niveis de poluicao e aplica IA Generativa para traduzir dados tecnicos em alertas compreensíveis para a populacao.

### Diferenciais Tecnicos
* Ingestao em Tempo Real: Conexao direta com a API WAQI.
* Pipeline de Dados (ETL): Automacao via GitHub Actions para criacao de historico de dados.
* Previsao (ML): Modelo de Series Temporais para prever picos de poluicao nas proximas 24h.
* IA Generativa: Integracao com o modelo Gemini para analise qualitativa dos dados.

## Tecnologias Utilizadas
* Linguagem: Python
* Analise de Dados: Pandas, Plotly
* Machine Learning: Scikit-learn / TensorFlow (LSTM)
* IA Generativa: Google Gemini API
* Deployment: Streamlit Cloud e GitHub Actions

## Estrutura do Repositorio
* /data: Armazenamento de snapshots historicos (CSV).
* /notebooks: Analise exploratoria e treinamento do modelo.
* /src: Codigo fonte do dashboard e logica da API.
* /.github/workflows: Automacao do pipeline de coleta.

---
Projeto em desenvolvimento para portfolio de Ciencia de Dados.
