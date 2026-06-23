import joblib
import pandas as pd
import psycopg
from psycopg.rows import dict_row
from app.db import get_connection_params

def predict_suscripcion(cliente_id: int):
    # 1. Cargar el modelo MLP y el preprocesador correcto
    preprocessor = joblib.load("models/modelo_perceptron_multicapa.pkl")
    model = joblib.load("artifacts/bank_model.joblib") 
    
    # 2. Conectarse a Supabase y extraer los datos del cliente
    params = get_connection_params()
    
    with psycopg.connect(**params, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM bank_marketing WHERE id = %s", (cliente_id,))
            cliente_data = cur.fetchone()
    
    # Si el cliente no existe
    if not cliente_data:
        return {"error": f"No existe el cliente con ID {cliente_id}"}

    # 3. Convertir el registro del cliente a un DataFrame de Pandas
    df_input = pd.DataFrame([cliente_data])
    
    # 4. Transformar los datos usando el PREPROCESADOR (Asegura las 18 columnas)
    input_data_transformed = preprocessor.transform(df_input)
    
    # 5. Realizar la predicción matemática con el MODELO
    prediccion = model.predict(input_data_transformed)[0]
    resultado_texto = "yes" if prediccion == 1 else "no"

    # 6. Retornar la respuesta final
    return {
        "cliente_id": cliente_id,
        "prediccion_deposito": resultado_texto,
        "mensaje": f"El modelo estima que el cliente {'sí' if resultado_texto == 'yes' else 'no'} aceptará el depósito."
    }
