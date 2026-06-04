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
    ]
)

client = TestClient(app)

def test_api():
    logging.info("Verificando disponibilidad de api")
    try:
        
        response = client.get("/")
        
        assert response.status_code == 200

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "operativo",
        "sistema": "banco"
    }
