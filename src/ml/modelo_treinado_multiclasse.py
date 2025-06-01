
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Geração de dados simulados
n = 1000
df = pd.DataFrame({
    'pot1': np.random.randint(0, 4096, n),
    'pot2': np.random.randint(0, 4096, n),
    'ax': np.random.randint(-16000, 16000, n),
    'ay': np.random.randint(-16000, 16000, n),
    'az': np.random.randint(-16000, 16000, n),
})

# Cálculo de intensidade de vibração
df['vib_total'] = df[['ax', 'ay', 'az']].abs().max(axis=1)

# Classificação multiclasse:
# 0 = OK, 1 = ATENÇÃO, 2 = RISCO
def classificar(row):
    if row['pot2'] > 3000 and row['vib_total'] > 10000:
        return 'RISCO'
    elif row['pot2'] > 2000 or row['vib_total'] > 7000:
        return 'ATENÇÃO'
    else:
        return 'OK'

df['classificacao'] = df.apply(classificar, axis=1)

# Treinamento do modelo
X = df[['pot1', 'pot2', 'ax', 'ay', 'az']]
y = df['classificacao']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Salvar modelo multiclasse
joblib.dump(modelo, 'modelo_multiclasse.pkl')
print("Modelo salvo como modelo_multiclasse.pkl")
