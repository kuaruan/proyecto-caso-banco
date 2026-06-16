import os
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from app.db import test_connection, get_servicio, get_servicios_stats

# Detección raíz del proyecto -> evita problemas en Docker
RUTA_MODELO = os.path.join(BASE_DIR, "models", "modelo_perceptron_multicapa.pkl")
RUTA_ESCALADOR = os.path.join(BASE_DIR, "models", "escalador_minmax.pkl")

try:
    #cargar archivos en memoria global una sola vez al encender la API
    modelo_predictivo = joblib.load(RUTA_MODELO)
    escalador_datos = joblib.load(RUTA_ESCALADOR)
    print("Perceptrón Multicapa y Escalador MinMax acoplados con éxito en producción.")
except Exception as e:
    print(f"No se pudieron cargar los archivos de modelos (.pkl). Error: {e}")
    modelo_predictivo = None
    escalador_datos = None

# Zona de esquema y validación de datos 
class ClienteInput(BaseModel):
    age: int = Field(..., description="Edad del cliente", example=35)
    balance: float = Field(..., description="Balance anual en la cuenta", example=1500.0)
    day: int = Field(..., description="Último día del mes en que fue contactado", example=15)
    duration_min: float = Field(..., description="Duración de la llamada en minutos", example=240)
    campaign: int = Field(..., description="Número de contactos realizados en esta campaña", example=2)
    pdays: int = Field(..., description="Días transcurridos desde la campaña anterior (-1 si no)", example=-1)
    previous: int = Field(..., description="Número de contactos previos a esta campaña", example=0)


app = FastAPI(
    title="API de Gestión de Datos - Bank Marketing",
    description="Sistema para la consulta y análisis descriptivo de suscripciones"
)

# --- Endpoints de Información ---

@app.get("/")
def root():
    return {
        "message": "API de Gestión de Datos para Bank Marketing",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    return {"status": "operativo", "sistema": "banco"}
    
@app.get("/db-health")
def db_health():
    """Verificar la conexión con Supabase"""
    return test_connection()

# --- Endpoints de Datos ---

@app.get("/servicio")
def listar_suscripciones(limit: int = Query(default=20, ge=1, le=100)):
    """Obtiene los registros de la base de datos en Supabase"""
    try:
        data = get_servicio(limit=limit)
        return {
            "status": "ok",
            "total_registros": len(data),
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/suscripciones/estadisticas")
def estadisticas_banco():
    """Análisis estadístico descriptivo de la campaña"""
    try:
        stats = get_servicios_stats()
        return {
            "status": "ok",
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict")
def predecir_suscripcion(payload: ClienteInput):
    """Se reciben los datos (crudos en forma Json) para aplicar escalado y predicción de suscripción de depósito con algoritmo de predicción : Perceptrón Multicapa"""
    if modelo_predictivo is None or escalador_datos is None:
        raise HTTPException(
            status_code=503,
            detail="Servicio no disponible"
        )
    try:
        datos_crudos = [
            payload.age,
            payload.balance,
            payload.day,
            payload.duration_min,
            payload.campaign,
            payload.pdays,
            payload.previous
        ]

        matriz_datos = np.array([datos_crudos])
        datos_escalados = escalador_datos.transform(matriz_datos)
        prediccion = modelo_predictivo.predict(datos_escalados)
        resultado_final = int(prediccion[0])

        return {
            "status": "ok",
            "prediction": resultado_final,
            "prediction_label": "Deposit" if resultado_final == 1 else "No Deposit"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al predecir: {str(e)}")
