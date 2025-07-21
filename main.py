from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a la galería de arte API"}


# Modelo de Obra de Arte
class ObraDeArte(BaseModel):
    id: int
    autor: str
    año: int
    precio: float
    tipo: str  # pintura, escultura, fotografía, etc.

# Catálogo inicial (como base de datos temporal)
catalogo_obras: List[ObraDeArte] = [
    ObraDeArte(id=1, autor="Frida Kahlo", año=1939, precio=150000.0, tipo="Pintura"),
    ObraDeArte(id=2, autor="Fernando Botero", año=1995, precio=70000.0, tipo="Escultura")
]

# 1. Listar todas las obras
@app.get("/obras", response_model=List[ObraDeArte])
def listar_obras():
    return catalogo_obras

# 2. Eliminar una obra por ID
@app.delete("/obras/{obra_id}")
def eliminar_obra(obra_id: int):
    for obra in catalogo_obras:
        if obra.id == obra_id:
            catalogo_obras.remove(obra)
            return {"mensaje": f"Obra con ID {obra_id} eliminada"}
    raise HTTPException(status_code=404, detail="Obra no encontrada")

# 3. Actualizar el precio de una obra
@app.put("/obras/{obra_id}/precio")
def actualizar_precio(obra_id: int, nuevo_precio: float):
    for obra in catalogo_obras:
        if obra.id == obra_id:
            obra.precio = nuevo_precio
            return {"mensaje": f"Precio actualizado a {nuevo_precio}"}
    raise HTTPException(status_code=404, detail="Obra no encontrada")
