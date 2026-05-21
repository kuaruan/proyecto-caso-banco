import joblib
import pandas as pd
from app.db import get_connection_params
import psycopg
from psycopg.rows import dict_row

def predict_suscripcion(cliente_id: int):
    # 1. Cargar el modelo 
    model = joblib.load("models/bank_model.pkl")
    
    # 2. Buscar datos en Supabase
    params = get_connection_params()
    with psycopg.connect(**params, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM bank_marketing WHERE id = %s", (cliente_id,))
            cliente_data = cur.fetchone()
    
    if not cliente_data:
        return {"error": "Cliente no encontrado"}

    # 3. Preparar los datos para el modelo
    input_data = {
        'age': cliente_data['age'],
        'balance': cliente_data['balance'],
        'day': cliente_data['day'],
        'duration': cliente_data['duration'],
        'campaign': cliente_data['campaign']
    }
    
    df_input = pd.DataFrame([input_data])
    
    # 4. Predicción
    prediccion = model.predict(df_input)
    # Convertimos a 'yes'/'no' según lo que el LabelEncoder aprendió
    resultado = "yes" if prediccion[0] == 1 else "no"

    return {
        "cliente_id": cliente_id,
        "prediccion_deposito": resultado,
        "mensaje": "El modelo estima que el cliente " + ("sí" if resultado == "yes" else "no") + " aceptará el depósito."
    }