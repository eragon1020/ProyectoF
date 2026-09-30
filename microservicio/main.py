"""Microservicio de sugerencias de gastos (FastAPI + MongoDB Atlas).

Variables de entorno:
  MONGODB_URI  -> cadena de conexión de MongoDB Atlas
  MONGODB_DB   -> nombre de la base (opcional, por defecto 'cuentas_claras')
"""
import os

from fastapi import FastAPI
from pydantic import BaseModel, Field
from pymongo import MongoClient

app = FastAPI(title="Sugerencias de gastos")

SEMILLA = [
    {"nombre": "Mercado", "emoji": "🛒", "monto_sugerido": 120000},
    {"nombre": "Arriendo", "emoji": "🏠", "monto_sugerido": 900000},
    {"nombre": "Gasolina", "emoji": "⛽", "monto_sugerido": 80000},
    {"nombre": "Domicilio", "emoji": "🛵", "monto_sugerido": 45000},
    {"nombre": "Servicios públicos", "emoji": "💡", "monto_sugerido": 150000},
    {"nombre": "Salida a comer", "emoji": "🍽️", "monto_sugerido": 100000},
]


def get_coleccion():
    cliente = MongoClient(os.environ["MONGODB_URI"], serverSelectionTimeoutMS=5000)
    col = cliente[os.getenv("MONGODB_DB", "cuentas_claras")]["sugerencias"]
    if col.count_documents({}) == 0:
        col.insert_many([dict(s) for s in SEMILLA])
    return col


class Sugerencia(BaseModel):
    nombre: str = Field(min_length=1, max_length=60)
    emoji: str = "💸"
    monto_sugerido: int = Field(gt=0)


@app.get("/")
def salud():
    return {"estado": "ok"}


@app.get("/sugerencias")
def listar():
    col = get_coleccion()
    # Se expone el _id como "id" (string) para que los microservicios de
    # actualización y eliminación puedan referenciar cada documento.
    return [
        {"id": str(d["_id"]), **{k: v for k, v in d.items() if k != "_id"}}
        for d in col.find().sort("nombre")
    ]


@app.post("/sugerencias", status_code=201)
def crear(s: Sugerencia):
    get_coleccion().insert_one(s.model_dump())
    return s
