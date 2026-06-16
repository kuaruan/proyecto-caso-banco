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

@app.post("/predict")
def predecir_suscripcion(cliente: ClienteInput):
    """Se reciben los datos (crudos en forma Json) para aplicar escalado y predicción de suscripción de depósito con algoritmo de predicción : Perceptrón Multicapa"""
    if modelo_predictivo is None or escalador_datos is None:
        raise HTTPException(
            status_code=503,
            detail="Servicio no disponible"
        )
    try:
        datos_crudos = [
            cliente.age,
            cliente.balance,
            cliente.day,
            cliente.duration,
            cliente.campaign,
            cliente.pdays,
            cliente.previous
        ]

        matriz_datos = np.array([datos_crudos])
        datos_escalados = escalador_datos.transform(matriz_datos)
        prediccion = modelo_predictive.predict(datos_escalados)
        resultado_final = int(prediccion[0])

        mensaje_negocio = (
            "Cliente se suscribirá, priorizar contacto"
            if resultado_final == 1 
            else "Cliente no se suscribirá, no priorizar" 
        )

        return {
            "status": "success",
            "prediction_code": resultado_final,
            "prediction_label": "Deposit" if resultado_final == 1 else "No Deposit",
            "recomendacion": mensaje_negocio
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al predecir: {str(e)}")
