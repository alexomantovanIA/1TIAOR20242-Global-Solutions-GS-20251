from fastapi import FastAPI
from typing import List
import os
import psycopg2

app = FastAPI(title="GS Deslizamento API")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "gs_deslizamento")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


@app.get("/leituras")
def listar_leituras() -> List[dict]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, timestamp, umidade, chuva, acc_z FROM leituras ORDER BY id DESC")
            rows = cur.fetchall()
    return [
        {
            "id": r[0],
            "timestamp": r[1],
            "umidade": r[2],
            "chuva": r[3],
            "acc_z": r[4],
        }
        for r in rows
    ]


@app.get("/inferencias")
def listar_inferencias() -> List[dict]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, timestamp, umidade, chuva, acc_z, classe FROM inferencias ORDER BY id DESC"
            )
            rows = cur.fetchall()
    return [
        {
            "id": r[0],
            "timestamp": r[1],
            "umidade": r[2],
            "chuva": r[3],
            "acc_z": r[4],
            "classe": r[5],
        }
        for r in rows
    ]


@app.get("/alertas")
def listar_alertas() -> List[dict]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, timestamp, umidade, chuva, acc_z, classe, alerta_enviado FROM alertas ORDER BY id DESC"
            )
            rows = cur.fetchall()
    return [
        {
            "id": r[0],
            "timestamp": r[1],
            "umidade": r[2],
            "chuva": r[3],
            "acc_z": r[4],
            "classe": r[5],
            "alerta_enviado": r[6],
        }
        for r in rows
    ]

