# modelo_treinado_multiclasse.py
"""
Treinamento de modelo de classificação multiclasse para prever risco de deslizamento
com base em sensores: umidade, chuva e vibração no eixo Z (acc_z).
As classes são: "ok", "atencao" e "risco".
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os

# ------------------------------
# 1. Geração de dados simulados
# ------------------------------

np.random.seed(42)

# Classe "ok"
ok_data = pd.DataFrame({
    'umidade': np.random.uniform(60, 100, 100),
    'chuva': np.random.uniform(0, 60, 100),
    'acc_z': np.random.uniform(-3, 3, 100),
    'classe': 'ok'
})

# Classe "atencao"
atencao_data = pd.DataFrame({
    'umidade': np.random.uniform(40, 59, 100),
    'chuva': np.random.uniform(60, 120, 100),
    'acc_z': np.random.uniform(-6, -3, 100),
    'classe': 'atencao'
})

# Classe "risco"
risco_data = pd.DataFrame({
    'umidade': np.random.uniform(0, 39, 100),
    'chuva': np.random.uniform(120, 150, 100),
    'acc_z': np.random.uniform(-20, -6, 100),
    'classe': 'risco'
})

# Junta todos os dados
df = pd.concat([ok_data, atencao_data, risco_data], ignore_index=True)

# Embaralha os dados
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# ------------------------------
# 2. Separação em treino/teste
# ------------------------------

X = df[['umidade', 'chuva', 'acc_z']]
y = df['classe']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ------------------------------
# 3. Treinamento do modelo
# ------------------------------

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ------------------------------
# 4. Avaliação do modelo
# ------------------------------

y_pred = model.predict(X_test)
print("📊 Relatório de Classificação:")
print(classification_report(y_test, y_pred))

# ------------------------------
# 5. Salvamento do modelo
# ------------------------------

# Caminho para salvar o modelo
save_path = os.path.join("ml", "modelo_multiclasse_ajustado_v2.pkl")

# Garante que a pasta exista
os.makedirs(os.path.dirname(save_path), exist_ok=True)

# Salva com pickle
with open(save_path, "wb") as f:
    pickle.dump(model, f)

print(f"✅ Modelo salvo com sucesso em: {save_path}")
