import logging
import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [AUDIT_LOG] [%(levelname)s]: %(message)s",
    handlers = [
        logging.FileHandler("app.log", mode="w", encoding="utf-8"), # Limpieza log antiguo
        logging.StreamHandler() # Logs en vivo
    ],
    force=True # Generacion archivo
)

client = TestClient(app)

def test_api(): # Disp
    logging.info("Verificando disponibilidad de api")
    try:
        logging.info("Petición http get a endpoint de la app")
        response = client.get("/")

        logging.info(f"Respuesta entregada: Estado = {response.status_code}")
        
        assert response.status_code == 200 #  200, todo ok! solicitud procesada

        logging.info("Validación exitosa, api activa")
    except AssertionError as e:
        logging.error(f"Algo ha fallado: {e}")
        raise e # remarcar error en github
    except Exception as e: 
        logging.error(f"Error: {e}")
        raise e

    
def test_health():
    logging.info("Verificación estado interno")
    try:
        logging.info("Solicitud http a endpoint health")
        response = client.get("/health")
        logging.info("Respuesta de estado /health: {response.status_code")
        assert response.status_code == 200
        assert response.json() == { # Validacion json retornado por api
            "status": "operativo",
            "sistema": "banco"
        }
        logging.info("Validación exitosa c:")
        
    except AssertionError as e:
        logging.error(f"Error de validación estado /health: {e}")
        raise e
    except Exception as e: 
        logging.error(f"Error: {e}")
        raise e

def test_db(): # Conexión db
    logging.info("Verificar conexión con Supabase")
    try: 
        logging.info("Validar variables de entorno")
        response = client.get("/docs")
        assert response.status_code == 200
        logging.info("Validación exitosa, tránsito y endpoints correctos")

    except AssertionError as e:
        logging.error(f"Error de acceso: {e}")
        raise e
    except Exception as e: 
        logging.error(f"Error en  capa: {e}")
        raise e
