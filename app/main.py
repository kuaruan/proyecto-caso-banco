from fastapi import FastAPI, HTTPException, Query
from app.db import test_connection, get_servicio, get_servicios_stats

app = FastAPI(
    title="API de Gestión de Datos - Bank Marketing",
    description="Sistema para la consulta y análisis descriptivode suscripciones"
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
            "indicadores": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))