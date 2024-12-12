# Imports
from enum import Enum
from fastapi import FastAPI, HTTPException
from typing import List, Dict, Optional
from pydantic import BaseModel
import db_usuarios
import datetime
from fastapi.middleware.cors import CORSMiddleware

# Inicializar la aplicación
app = FastAPI()

# Configuración del middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.22.2"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos
class Alumno(BaseModel):
    userid: int
    nombre: str
    mail: str
    passwd: str
    rol: str
    cardid:str


class Fichaje(BaseModel):
    fichajeid: int
    hentr: str
    hsal: str
    cardid: str
    deviceid: str

class Aula(BaseModel):
    aulaid: int
    nombre: str
    ubicacion: str
    deviceid: str




@app.get("/")
def read_root():
    return {"message": "API Proyecto Grupo 1 funcionando"}


@app.get("/dbCheck")
def check_db_connection():
    """Verifica la conexión con la base de datos."""
    result = db_usuarios.check_connection()
    if result["status"] == -1:
        raise HTTPException(status_code=500, detail=result["message"])
    return {"status": "Conexión exitosa"}

@app.get("/usuario/list", response_model=List[Alumno])
def read_user():
    """Obtiene la lista de todos los usuarios."""
    result = db_usuarios.read_users()
    if result["status"] == -1:
        raise HTTPException(status_code=500, detail=result["message"])
    return result["data"]

@app.get("/usuario/show/{id_usuario}", response_model=Alumno)
def read_user_id(id_usuario: int):
    """Obtiene la información de un usuario por ID."""
    result = db_usuarios.read_user_by_id(id_usuario)
    if result["status"] == -1:
        raise HTTPException(status_code=500, detail=result["message"])
    if not result["data"]:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return result["data"]

@app.get("/aula", response_model=List[Aula])
def get_aulas():
    """Obtiene todas las aulas registradas."""
    result = db_usuarios.read_aulas()
    if result["status"] == -1:
        raise HTTPException(status_code=500, detail=result["message"])
    return result["data"]

@app.get("/fichaje", response_model=List[Fichaje])
def read_fichaje():
    """Obtiene la lista de fichajes."""
    result = db_usuarios.read_fichajes()
    if result["status"] == -1:
        raise HTTPException(status_code=500, detail=result["message"])

    formatted_data = []
    for row in result["data"]:
        formatted_data.append({
            "fichajeid": row.get("fichajeid"),
            "hentr": row.get("hentr").isoformat() if row.get("hentr") else "",
            "hsal": row.get("hsal").isoformat() if row.get("hsal") else "",
            "cardid": row.get("cardid",""),  # Asegurar un valor por defecto
            "deviceid": row.get("deviceid","")
        })

    return formatted_data


@app.post("/insert/{table_name}")
def insert_data(table_name: str, data: dict):
    """Inserta un registro en la tabla especificada."""
    result = db_usuarios.insert_data(table_name, data)
    if result["status"] == -1:
        raise HTTPException(status_code=500, detail=result["message"])
    return {"message": "Inserción exitosa", "id": result["id"]}

@app.put("/update/{table_name}")
def update_data(table_name: str, data: dict, condition: dict):
    """Actualiza un registro en la tabla especificada basado en una condición."""
    result = db_usuarios.update_data(table_name, data, condition)
    if result["status"] == -1:
        raise HTTPException(status_code=500, detail=result["message"])
    return {"message": "Actualización exitosa"}

@app.delete("/delete/{table_name}")
def delete_data(table_name: str, condition: dict):
    """Elimina un registro en la tabla especificada basado en una condición."""
    result = db_usuarios.delete_data(table_name, condition)
    if result["status"] == -1:
        raise HTTPException(status_code=500, detail=result["message"])
    return {"message": "Eliminación exitosa", "rows_affected": result.get("rows_affected", 0)}

@app.get("/select/{table_name}", response_model=List[Dict])
def select_data(table_name: str):
    """Hace un SELECT en la tabla especificada."""
    valid_tables = ["usuario", "aula", "horario", "asignatura", "fichaje"]  # Tabla válidas
    if table_name not in valid_tables:
        raise HTTPException(status_code=400, detail="Tabla no válida")

    result = db_usuarios.select_data(table_name)
    if result["status"] == -1:
        raise HTTPException(status_code=500, detail=result["message"])
    return result["data"]
