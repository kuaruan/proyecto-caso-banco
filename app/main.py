from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from app.db import test_connection, get_servicio, get_servicios_stats
from app.predict import predict_suscripcion

app = FastAPI(title="Bank Marketing Dataset API")

# --- Endpoints de Información ---

@app.get("/")
def root():
    return {"message": "API de Predicción de suscripciones para Bank Marketing"}

@app.get("/health")
async def health():
    return {
        "status": "operativo",
        "sistema": "banco"
    }
    
@app.get("/db-health")
def db_health():
    """Verificar la conexión con Supabase"""
    return test_connection()

# --- Endpoints de Datos ---

@app.get("/servicio")
def listar_suscripciones(limit: int = Query(default=20, ge=1, le=100)):
    """Obtiene los últimos registros de la base de datos"""
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

# --- Endpoint de Predicción con IA ---

@app.get("/predict/{cliente_id}")
def predecir_por_id(cliente_id: int):
    """
    Endpoint que toma un ID de cliente, busca sus datos en Supabase 
    y usa el modelo .pkl para predecir si suscribirá un depósito.
    """
    try:
        result = predict_suscripcion(cliente_id)
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
            
        return {
            "status": "ok",
            "resultado": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la predicción: {str(e)}")
