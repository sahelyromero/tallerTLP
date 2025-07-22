from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
from typing import List

app = FastAPI()

ARCHIVO_OBRAS = "obras.json"

class ObraDeArte(BaseModel):
    id: int
    titulo: str
    autor: str
    año: int
    precio: float
    tipo: str

# Funciones de archivo
def cargar_obras() -> List[dict]:
    return (
        json.load(open(ARCHIVO_OBRAS, "r", encoding="utf-8"))
        if os.path.exists(ARCHIVO_OBRAS) else []
    )

def guardar_obras(obras: List[dict]):
    with open(ARCHIVO_OBRAS, "w", encoding="utf-8") as f:
        json.dump(obras, f, indent=4, ensure_ascii=False)

# Rutas
@app.get("/obras")
def obtener_obras():
    return cargar_obras()

@app.post("/obras")
def agregar_obra(obra: ObraDeArte):
    obras = cargar_obras()

    if any(map(lambda o: o["id"] == obra.id, obras)):
        raise HTTPException(status_code=400, detail="Ya existe una obra con ese ID.")

    nuevas_obras = obras + [obra.dict()]
    guardar_obras(nuevas_obras)

    return {"mensaje": "Obra agregada exitosamente."}

@app.delete("/obras/{id}")
def eliminar_obra(id: int):
    obras = cargar_obras()
    obras_nuevas = list(filter(lambda o: o["id"] != id, obras))

    if len(obras_nuevas) == len(obras):
        raise HTTPException(status_code=404, detail="Obra no encontrada.")

    guardar_obras(obras_nuevas)
    return {"mensaje": "Obra eliminada exitosamente."}

@app.put("/obras/{id}")
def actualizar_precio(id: int, nuevo_precio: float):
    obras = cargar_obras()

    def actualizar(obra):
        return {**obra, "precio": nuevo_precio} if obra["id"] == id else obra

    if not any(o["id"] == id for o in obras):
        raise HTTPException(status_code=404, detail="Obra no encontrada.")

    obras_actualizadas = list(map(actualizar, obras))
    guardar_obras(obras_actualizadas)

    return {"mensaje": "Precio actualizado correctamente."}
