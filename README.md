# EcoStream Insight: Monitoramento e Analise Preditiva de Qualidade do Ar

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-F7931E.svg)](https://scikit-learn.org/)
[![IA Generativa](https://img.shields.io/badge/IA-Llama%203.1-0668E1.svg)](https://groq.com/)

O EcoStream Insight e uma plataforma de monitoramento ambiental que integra coleta automatizada de dados, modelos de aprendizado de maquina para previsao de indices e inteligencia artificial generativa para analise de riscos. O sistema foi projetado para transformar dados brutos de sensores globais em informacoes estrategicas para a saude publica.

## Arquitetura do Sistema

A solucao e estruturada em quatro camadas principais:

### Ingestao de Dados
O sistema utiliza a API do World Air Quality Index (WAQI) para capturar indices de qualidade do ar em tempo real. A coleta e orquestrada pelo GitHub Actions, garantindo a atualizacao do historico sem dependencia de infraestrutura local permanente.

### Processamento e Tratamento
Os dados brutos passam por um pipeline de limpeza e transformacao, onde e aplicada uma tecnica de media movel (Rolling Window) de tres periodos. Este processo permite a geracao de uma linha de tendencia que suaviza ruidos e identifica a trajetoria real dos indices ambientais.

### Camada de Inteligencia Artificial
O projeto utiliza uma abordagem hibrida de IA:
* Aprendizado de Maquina (Preditivo): Modelo baseado em Random Forest treinado para prever o AQI da proxima hora com base em tendencias calculadas e variacoes imediatas.
* Modelagem de Linguagem (Generativo): Integracao com o modelo Llama 3.1 da Meta (via Groq) para interpretar a relacao entre o valor atual e a previsao, gerando relatorios tecnicos sobre riscos respiratorios e recomendacoes preventivas.

### Visualizacao e Insights
A interface desenvolvida em Streamlit apresenta graficos interativos via Plotly. O destaque e a sintonia visual entre os dados reais coletados e a linha de tendencia analitica, permitindo uma leitura clara do comportamento atmosferico.

## Especificacoes Tecnicas

### Requisitos de Software
* Python 3.9 ou superior
* Bibliotecas: Pandas, Numpy, Scikit-learn, Plotly, Streamlit, Groq, Dotenv

### Estrutura de Diretorios
* /src: Codigo fonte do dashboard e do processador de dados.
* /data: Arquivos CSV contendo o historico acumulado e dados preparados para IA.
* /models: Binarios dos modelos de Machine Learning treinados.
* /.github/workflows: Arquivos de configuracao da automacao de coleta.

## Seguranca e Variaveis de Ambiente

O projeto implementa protocolos de seguranca para proteger as credenciais de acesso as APIs. Nenhuma chave de acesso e exposta no repositorio publico. O sistema utiliza um arquivo .env local e GitHub Secrets no ambiente de producao para gerenciar:
* TOKEN_WAQI: Credencial de acesso aos dados globais de sensores.
* GROQ_API_KEY: Chave de autenticacao para o modelo Llama 3.1.

## Procedimento de Execucao

Para replicar o ambiente localmente, siga as instrucoes abaixo:

1. Instalar dependencias:
   pip install -r requirements.txt

2. Configurar o arquivo .env na raiz do projeto com as chaves necessarias.

3. Executar o processador para atualizar o dataset e treinar o modelo:
   python src/processador.py

4. Iniciar o servidor de visualizacao:
   streamlit run src/app.py
