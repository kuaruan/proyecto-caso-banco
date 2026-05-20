from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from app.db import test_connection, get_servicio, get_servicios_stats
from app.predict import predict_suscripcion

app = FastAPI(title="Bank Marketing Dataset")

class PredictAprobacionRequest(BaseModel):
    edad: int
    ingresos_mensuales: int
    score_crediticio: int
    monto_prestamo: int
    cuotas: int
    es_propietario: str 
    empleo: str        
    deuda_total: int

@app.get("/")
def root():
    return {"message": "API activa"}

@app.get("/health")
def health():
    return {"status": "operativo", "sistema": "banco"}

@app.get("/db-health")
def db_health():
    """Verificar la conexión con Supabase"""
    return test_connection()

@app.get("/servicio")
def listar_suscripciones(limit: int = Query(default=20, ge=1, le=100)):
    """Obtiene los últimos usuarios en suscribir un depósito"""
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
    """Análisis estadístico de suscripciones"""
    try:
        stats = get_servicios_stats()
        return {
            "status": "ok",
            "indicadores": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict-suscripcion")
def evaluar_credito(payload: PredictSuscripcionRequest):
    """Endpoint para predecir que clientes tienen mayor probabilidad de suscribir un depósito"""
    try:
        result = predict_suscripcion(payload.model_dump())
        return {
            "status": "ok",
            "id_cliente": "evaluacion_temporal", 
            "resultado": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
