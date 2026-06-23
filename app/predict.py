import joblib
import pandas as pd
from app.db import get_connection_params
import psycopg
from psycopg.rows import dict_row

def predict_suscripcion(cliente_id: int):
    # Cargar modelo
    model = joblib.load("models/bank_model.pkl")
    params = get_connection_params()
    
    with psycopg.connect(**params, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            # IMPORTANTE: Usamos la columna 'id' que agregamos con el comando ALTER TABLE
            cur.execute("SELECT * FROM bank_marketing WHERE id = %s", (cliente_id,))
            cliente_data = cur.fetchone()
    
    if not cliente_data:
        return {"error": f"No existe el cliente con ID {cliente_id}"}

    # Preparamos las variables exactamente como las espera el RandomForest
    input_data = pd.DataFrame([{
        'age': int(cliente_data['age']),
        'balance': int(cliente_data['balance']),
        'day': int(cliente_data['day']),
        'duration': int(cliente_data['duration']),
        'campaign': int(cliente_data['campaign'])
    }])
    
    prediccion = model.predict(input_data)[0]
    resultado_texto = "yes" if prediccion == 1 else "no"

    return {
        "cliente_id": cliente_id,
        "prediccion_deposito": resultado_texto,
        "mensaje": f"El modelo estima que el cliente {'sí' if resultado_texto == 'yes' else 'no'} aceptará el depósito."
    }

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
