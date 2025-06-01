
import pandas as pd
import matplotlib.pyplot as plt
import os

# Criar pasta 'dados' se não existir
os.makedirs('src/dados', exist_ok=True)

# Ler os dados do CSV multiclasse
df = pd.read_csv("leituras_multiclasse.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Gráfico de barras: contagem de classificações
contagem = df['classificacao'].value_counts().sort_index()

plt.figure(figsize=(6, 4))
contagem.plot(kind='bar', color=['green', 'orange', 'red'])
plt.title("Classificações Registradas")
plt.xlabel("Classificação")
plt.ylabel("Quantidade")
plt.xticks(rotation=0)
plt.tight_layout()
plt.grid(True)
plt.savefig("src/dados/classificacoes_barras.png")
plt.close()

# Gráfico temporal: linha com classificação ao longo do tempo
mapa_classe = {'OK': 0, 'ATENÇÃO': 1, 'RISCO': 2}
df['classificacao_num'] = df['classificacao'].map(mapa_classe)

df_ordenado = df.sort_values('timestamp')

plt.figure(figsize=(12, 4))
plt.plot(df_ordenado['timestamp'], df_ordenado['classificacao_num'], marker='o', linestyle='-')
plt.title("Evolução Temporal da Classificação")
plt.xlabel("Tempo")
plt.ylabel("Classificação (0=OK, 1=ATENÇÃO, 2=RISCO)")
plt.yticks([0, 1, 2], ['OK', 'ATENÇÃO', 'RISCO'])
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("src/dados/evolucao_classificacao.png")
plt.close()
