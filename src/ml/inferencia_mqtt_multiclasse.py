
import paho.mqtt.client as mqtt
import joblib
import json
import csv
import sqlite3
from datetime import datetime
import pandas as pd

# Carrega o modelo multiclasse
model = joblib.load('modelo_multiclasse.pkl')

# Configura arquivos de armazenamento
CSV_FILE = 'leituras_multiclasse.csv'
DB_FILE = 'leituras_multiclasse.db'
CSV_FIELDS = ['timestamp', 'pot1', 'pot2', 'ax', 'ay', 'az', 'classificacao']

# Inicializa banco SQLite
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leituras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            pot1 REAL,
            pot2 REAL,
            ax REAL,
            ay REAL,
            az REAL,
            classificacao TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Callback ao receber mensagem
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    print("Recebido:", payload)

    features = pd.DataFrame([payload], columns=['pot1', 'pot2', 'ax', 'ay', 'az'])
    prediction = model.predict(features)[0]
    print("Classificação:", prediction)

    registro = {
        'timestamp': datetime.now().isoformat(),
        'pot1': payload['pot1'],
        'pot2': payload['pot2'],
        'ax': payload['ax'],
        'ay': payload['ay'],
        'az': payload['az'],
        'classificacao': prediction
    }

    # Salvar em CSV
    try:
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(registro)
        print("Salvo no CSV.")
    except Exception as e:
        print("Erro ao salvar CSV:", e)

    # Salvar em SQLite
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO leituras (timestamp, pot1, pot2, ax, ay, az, classificacao)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            registro['timestamp'],
            registro['pot1'],
            registro['pot2'],
            registro['ax'],
            registro['ay'],
            registro['az'],
            registro['classificacao']
        ))
        conn.commit()
        conn.close()
        print("Salvo no SQLite.")
    except Exception as e:
        print("Erro ao salvar no SQLite:", e)

# Configura MQTT
client = mqtt.Client()
client.connect("mqtt.eclipseprojects.io", 1883, 60)
client.subscribe("esp32/sensores")
client.on_message = on_message

# Inicia loop MQTT
client.loop_forever()
