from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import pandas as pd
import pickle
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '..', '..', 'ml', 'modelo_multiclasse_ajustado_v2.pkl')
DB_PATH = os.path.join(BASE_DIR, '..', '..', 'data', 'gs_deslizamento.db')

# Load ML model
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

app = FastAPI(title="GS 2025.1 API")

class SensorInput(BaseModel):
    umidade: float
    chuva: float
    acc_z: float

@app.post('/predict')
def predict(data: SensorInput):
    try:
        df = pd.DataFrame([[data.umidade, data.chuva, data.acc_z]],
                          columns=['umidade', 'chuva', 'acc_z'])
        pred = model.predict(df)[0]
        response = {'classe': pred}
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(df)[0].max().item()
            response['probabilidade'] = proba
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/leituras')
def get_leituras(limit: int = 10):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM leituras ORDER BY id DESC LIMIT ?", (limit,))
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return {'leituras': rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
