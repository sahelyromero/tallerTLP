import unittest
import os
import json
from fastapi.testclient import TestClient
from main import app

ARCHIVO_PRUEBA = "test_data.json"  

import main
main.ARCHIVO_OBRAS = ARCHIVO_PRUEBA

client = TestClient(app)

class TestGaleriaArte(unittest.TestCase):

    def setUp(self):
         
        obras_prueba = [{
            "id": 1,
            "titulo": "La noche estrellada",
            "autor": "Vicent van Gogh",
            "año": 1889,
            "precio": 1000000.0,
            "tipo": "Pintura"
        }]
        with open(ARCHIVO_PRUEBA, "w", encoding="utf-8") as f:
            json.dump(obras_prueba, f, indent=4, ensure_ascii=False)
    
    def tearDown(self):

        if os.path.exists(ARCHIVO_PRUEBA):
            os.remove(ARCHIVO_PRUEBA)

    def test_obtener_obras(self):
        response = client.get("/obras")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
    
    def test_agregar_obra(self):
        nueva_obra = {
            "id": 2,
            "titulo": "El Estanque de Ninfeas",
            "autor": "Claude Monet",
            "año": 1889,
            "precio": 75000.0,
            "tipo": "Pintura"
        }
        response = client.post("/obras", json=nueva_obra)
        self.assertEqual(response.status_code, 200)
        self.assertIn("mensaje", response.json())
    
    def test_borrar_obra(self):
        response = client.delete("/obras/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("mensaje", response.json())
        
    def test_actualizar_precio(self):
        response = client.put("/obras/1?nuevo_precio=89647521")
        self.assertEqual(response.status_code, 200)
        self.assertIn("mensaje", response.json())

    def test_actualizar_precio_id_inexistente(self):
        response = client.put("/obras/9999?nuevo_precio=123456")  
        self.assertEqual(response.status_code, 404)
        self.assertIn("detail", response.json())
    
    def test_borrar_obra_id_inexistente(self):
        response = client.delete("/obras/9999")  
        self.assertEqual(response.status_code, 404)
        self.assertIn("detail", response.json())

    def test_agregar_obra_id_duplicado(self):
        obra_duplicada = {
            "id": 1, 
            "titulo": "Duplicado",
            "autor": "Autor Falso",
            "año": 2024,
            "precio": 1000.0,
            "tipo": "Escultura"
        }
        response = client.post("/obras", json=obra_duplicada)
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.json())
        self.assertEqual(response.json()["detail"], "Ya existe una obra con ese ID.")



if __name__ == '__main__':
    unittest.main()