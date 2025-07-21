from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI()

ARCHIVO_OBRAS = "obras.json"

class ObraDeArte(BaseModel):
    id: int
    titulo: str
    autor: str
    año: int
    precio: float
    tipo: str

def cargar_obras():
    if os.path.exists(ARCHIVO_OBRAS):
        with open(ARCHIVO_OBRAS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_obras(obras):
    with open(ARCHIVO_OBRAS, "w", encoding="utf-8") as f:
        json.dump(obras, f, indent=4, ensure_ascii=False)

@app.get("/obras")
def obtener_obras():
    return cargar_obras()

@app.post("/obras")
def agregar_obra(obra: ObraDeArte):
    obras = cargar_obras()
    if any(o["id"] == obra.id for o in obras):
        raise HTTPException(status_code=400, detail="Ya existe una obra con ese ID.")
    obras.append(obra.dict())
    guardar_obras(obras)
    return {"mensaje": "Obra agregada exitosamente."}

@app.delete("/obras/{id}")
def eliminar_obra(id: int):
    obras = cargar_obras()
    obras_nuevas = [o for o in obras if o["id"] != id]
    if len(obras_nuevas) == len(obras):
        raise HTTPException(status_code=404, detail="Obra no encontrada.")
    guardar_obras(obras_nuevas)
    return {"mensaje": "Obra eliminada exitosamente."}

@app.put("/obras/{id}")
def actualizar_precio(id: int, nuevo_precio: float):
    obras = cargar_obras()
    for obra in obras:
        if obra["id"] == id:
            obra["precio"] = nuevo_precio
            guardar_obras(obras)
            return {"mensaje": "Precio actualizado correctamente."}
    raise HTTPException(status_code=404, detail="Obra no encontrada.")
