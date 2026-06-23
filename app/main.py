import os
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from app.db import test_connection, get_servicio, get_servicios_stats
from app.predict import predict_bank_deposit  

app = FastAPI(
    title="API Bank Marketing",
    description="Sistema DataOps para la consulta analítica y predicción de suscripciones a depósitos a plazo"
)

# Zona de Esquemas y Validación de Datos ( con Pydantic) 
class ClienteInput(BaseModel):
    age: int = Field(..., description="Edad del cliente", example=35)
    balance: float = Field(..., description="Balance anual medio en la cuenta (en euros)", example=1500.0)
    day: int = Field(..., description="Último día del mes en que fue contactado", example=15)
    duration_min: float = Field(..., description="Duración de la llamada de campaña en minutos", example=3.5)
    campaign: int = Field(..., description="Número de contactos realizados durante esta campaña", example=2)
    pdays: int = Field(..., description="Días transcurridos desde la campaña anterior (-1 si no fue contactado)", example=-1)
    previous: int = Field(..., description="Número de contactos realizados antes de esta campaña", example=0)


# Endpoints de Información y Diagnóstico 

@app.get("/")
def root():
    return {
        "message": "API: Activa.Proyecto Gestión de Datos para Bank Marketing ",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    return {"status": "ok"}
    
@app.get("/db-health")
def db_health():
    """Verificar salud de la conexión directa con Supabase"""
    return test_connection()


# Endpoints de Datos (Sincronizados con tu app/db.py original) 

@app.get("/bank-data-demo")
def listar_suscripciones(limit: int = Query(default=20, ge=1, le=100)):
    """Obtiene una muestra de registros directamente desde la tabla en Supabase"""
    try:
        data = get_servicio(limit=limit)
        return {
            "status": "ok",
            "total_registros": len(data),
            "limit": limit,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/bank-data/stats")
def estadisticas_banco():
    """Muestra análisis descriptivo y agregados de la campaña de marketing (tasas de éxito, promedios)"""
    try:
        stats = get_servicios_stats()
        return {
            "status": "ok",
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint de Inferencia Predictiva 

@app.post("/predict")
def predecir_suscripcion(payload: ClienteInput):
    """
    Recibe los datos en crudo (JSON), procesa los cálculos matemáticos
    y evalúa mediante el modelo si el cliente se suscribirá (variable objetivo: deposit)
    """
    try:
        input_data = payload.model_dump()
        resultado = predict_bank_deposit(input_data)
        
        return {
            "status": "ok",
            "prediction": int(resultado["prediction"]),
            "prediction_label": resultado["label"]  # Retorna "Deposit" o "No Deposit"
        }

    except ValueError as ve:
        
        raise HTTPException(status_code=503, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el proceso de inferencia: {str(e)}")
