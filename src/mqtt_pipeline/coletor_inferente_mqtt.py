"""
Script: coletor_inferente_mqtt.py
Descrição: Escuta um tópico MQTT, grava os dados recebidos em PostgreSQL e realiza inferência imediata.
Se a classe prevista for "risco", envia alerta via SNS e registra na tabela 'alertas'.
"""

import psycopg2
import json
import paho.mqtt.client as mqtt
import pandas as pd
import pickle
import os
from dotenv import load_dotenv
from datetime import datetime
import boto3

# =======================
# 🔧 Configurações Gerais
# =======================

# Caminhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "gs_deslizamento")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
MODEL_PATH = os.path.join(BASE_DIR, "..", "..", "ml", "modelo_multiclasse_ajustado_v2.pkl")

# MQTT
TOPICO_MQTT = "gs2025/grupo11/deslizamento"
BROKER_MQTT = "mqtt.eclipseprojects.io"

# SNS / .env
load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")

# Cliente SNS
sns_client = boto3.client(
    "sns",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

# ============================
# 🧠 Carregamento do Modelo ML
# ============================

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# ================================
# 🧱 Inicializa o Banco de Dados
# ================================

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def inicializar_banco():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabela de leituras
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leituras (
            id SERIAL PRIMARY KEY,
            timestamp TEXT,
            umidade REAL,
            chuva REAL,
            acc_z REAL
        )
    """)

    # Tabela de inferências
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inferencias (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            umidade REAL,
            chuva REAL,
            acc_z REAL,
            classe TEXT
        )
    """)

    # Tabela de alertas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alertas (
            id SERIAL PRIMARY KEY,
            timestamp TEXT,
            umidade REAL,
            chuva REAL,
            acc_z REAL,
            classe TEXT,
            alerta_enviado BOOLEAN
        )
    """)

    conn.commit()
    conn.close()

# ==========================================
# 📩 Função chamada a cada nova mensagem MQTT
# ==========================================

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        umidade = float(payload.get("umidade", 0))
        chuva = float(payload.get("chuva", 0))
        acc_z = float(payload.get("acc_z", 0))
        timestamp = datetime.now().isoformat()

        conn = get_connection()
        cursor = conn.cursor()

        # Grava leitura
        cursor.execute(
            "INSERT INTO leituras (timestamp, umidade, chuva, acc_z) VALUES (%s, %s, %s, %s) RETURNING id",
            (timestamp, umidade, chuva, acc_z),
        )
        leitura_id = cursor.fetchone()[0]
        print(f"📥 Leitura gravada: ID={leitura_id} U={umidade} C={chuva} Z={acc_z}")

        # Realiza inferência
        features = pd.DataFrame([[umidade, chuva, acc_z]], columns=["umidade", "chuva", "acc_z"])
        classe = model.predict(features)[0]
        print(f"🔎 Classe inferida: {classe}")

        # Grava inferência
        cursor.execute(
            "INSERT INTO inferencias (id, timestamp, umidade, chuva, acc_z, classe) VALUES (%s, %s, %s, %s, %s, %s)",
            (leitura_id, timestamp, umidade, chuva, acc_z, classe),
        )

        # Se risco, envia alerta
        if classe == "risco":
            mensagem = (
                f"⚠️ ALERTA DE DESLIZAMENTO ⚠️\n\n"
                f"Umidade: {umidade}\n"
                f"Chuva: {chuva}\n"
                f"Aceleração Z: {acc_z}\n"
                f"Timestamp: {timestamp}"
            )

            try:
                sns_client.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Message=mensagem,
                    Subject="Alerta de Deslizamento - GS 2025.1"
                )
                alerta_enviado = True
                print("🚨 Alerta SNS enviado com sucesso.")
            except Exception as e:
                alerta_enviado = False
                print("❌ Erro ao enviar alerta SNS:", e)

            # Grava o alerta
            cursor.execute(
                "INSERT INTO alertas (timestamp, umidade, chuva, acc_z, classe, alerta_enviado) VALUES (%s, %s, %s, %s, %s, %s)",
                (timestamp, umidade, chuva, acc_z, classe, alerta_enviado),
            )

        conn.commit()
        conn.close()

    except Exception as e:
        print("❌ Erro ao processar mensagem:", e)

# ===================
# 🚀 Execução Principal
# ===================

def main():
    inicializar_banco()
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER_MQTT, 1883, 60)
    client.subscribe(TOPICO_MQTT)
    print(f"📡 Escutando MQTT: {TOPICO_MQTT}")
    client.loop_forever()

if __name__ == "__main__":
    main()
