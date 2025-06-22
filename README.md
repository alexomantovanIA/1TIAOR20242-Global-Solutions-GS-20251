
# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width="40%" height="40%"></a>
</p>

---

# Global Solutions (GS) 2025.1  
## Fase 7 — Previsão de Deslizamentos com IoT + ML

---

## 👨‍🎓 Integrantes:

- [Alexandre Oliveira Mantovani](https://www.linkedin.com/in/alexomantovani)
- [Edmar Ferreira Souza](https://www.linkedin.com/in/)
- [Enyd Crystina Rodrigues de Oliveira Bentivoglio](https://www.linkedin.com/in/enyd-bentivoglio-a47608364/)
- [Ricardo Lourenço Coube](https://www.linkedin.com/in/ricardolcoube/)
- [Jose Andre Filho](https://www.linkedin.com/in/joseandrefilho)

## 👩‍🏫 Professores:

- Tutor: [Leonardo Ruiz Orabona](https://www.linkedin.com/in/leonardoorabona)
- Coordenador: [André Godoi](https://www.linkedin.com/in/profandregodoi)

---

## 📌 Descrição do Projeto

Esta solução tem como objetivo prever e monitorar riscos de deslizamentos de terra, utilizando sensores simulados, ESP32, MQTT, PostgreSQL e Machine Learning.

A arquitetura executa inferência em tempo real logo após a recepção dos dados. Ao identificar a classe “risco”, um alerta é automaticamente enviado via AWS SNS. Todo o histórico é armazenado localmente e pode ser analisado por um dashboard em Jupyter Notebook.

---

## 📦 Entregáveis

- Simulação com ESP32 no Wokwi (chuva, umidade, vibração)
- Coletor MQTT com inferência imediata (`coletor_inferente_mqtt.py`)
- Modelo treinado (`modelo_multiclasse_ajustado_v2.pkl`)
- Banco PostgreSQL com leituras, inferências e alertas
- API REST em FastAPI para consulta dos dados
- Notebook com análise estatística e visual (`analise_inferencias.ipynb`)
- PDF com documentação e arquitetura do sistema
- Repositório GitHub público e vídeo demonstrativo

---

## 🔧 Tecnologias e Metodologia

- **Sensores**: potenciômetro (chuva e umidade), MPU6050 (vibração eixo Z)
- **Transmissão**: MQTT no tópico `gs2025/grupo11/deslizamento`
- **Processamento**: inferência imediata com RandomForest em Python
- **Armazenamento**: banco PostgreSQL com estrutura normalizada
- **Alertas**: integração com Amazon SNS para envio automático
- **API**: consulta dos dados via FastAPI
- **Análise de dados**: gráficos em Seaborn e Matplotlib (Jupyter Notebook)
- **Boas práticas**: uso de `.env`, estrutura modular e separação de responsabilidades

---

## 📊 Métricas e Classificação

- Entrada: umidade (%), chuva (nível), acc_z (vibração)
- Saída: classe predita (`ok`, `atencao`, `risco`)
- Inferência realizada **em tempo real**
- Envio de alerta quando `classe == risco`

---

## 📈 Visualizações no Notebook

- Correlação entre sensores
- Distribuição temporal de alertas
- Dispersão entre chuva e aceleração
- Evolução temporal dos sensores
- Frequência de classificações (ok, atenção, risco)
- Análise de médias e desvios por classe

---

## 🗂️ Estrutura do Projeto

```
📦 1TIAOR20242-Global-Solutions-GS-20251
├── assets/
│   └── logo-fiap.png
├── ml/
│   └── modelo_multiclasse_ajustado_v2.pkl
├── src/
│   │── ml/
│   │   └── modelo_treinado_multiclasse.py
│   ├── mqtt_pipeline/
│   │   └── coletor_inferente_mqtt.py
│   ├── api/
│   │   └── main.py
│   ├── visualizacao/
│   │   └── analise_inferencias.ipynb
│   └── wokwi/
│       └── diagram.json, libraries.txt, sketch.ino, wokwi-project
├── .env.example
├── requirements.txt
├── README.md
└── GS_2025_Entrega_Final.pdf
```

---

## ✅ Requisitos para Execução

1. Clonar o repositório
2. Criar `.env` a partir de `.env.example`
3. Instalar dependências:
```bash
pip install -r requirements.txt
```
4. Executar o coletor MQTT:
```bash
python src/mqtt_pipeline/coletor_inferente_mqtt.py
```

5. Iniciar a API FastAPI:
```bash
uvicorn src.api.main:app --reload
```

6. Execute o projeto no Wokwi:
- Você pode visualizar e interagir com a simulação do projeto no Wokwi clicando [aqui](https://wokwi.com/projects/431525090602695681).

7. Visualizar análises:
```bash
jupyter notebook src/visualizacao/analise_inferencias.ipynb
```

---

## 📽️ Demonstração em Vídeo

[🔗 Link para o vídeo demonstrativo (YouTube - não listado)](https://youtu.be/nBH2K_tjtSo)

---

## 📝 Licença

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/">
Este projeto segue o modelo FIAP e está licenciado sob 
<a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer">Attribution 4.0 International (CC BY 4.0)</a>.
</p>
