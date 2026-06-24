import joblib
import pandas as pd
import psycopg
from psycopg.rows import dict_row
from app.db import get_connection_params

def predict_suscripcion(cliente_id: int):
    # 1. Cargar el Pipeline completo (incluye preprocesamiento + MLP)
    model = joblib.load("models/modelo_perceptron_multicapa.pkl")
    
    # 2. Conectarse a Supabase y extraer los datos del cliente
    params = get_connection_params()
    
    with psycopg.connect(**params, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute('''SELECT 
                            age, job, marital, education, balance, housing, loan, 
                            contact, day, month, campaign, pdays, previous, poutcome, 
                            es_cliente_nuevo, tiene_doble_prestamo, duration_min, id
                        FROM bank_marketing 
                        WHERE id = %s''', (cliente_id,))
            cliente_data = cur.fetchone()
    
    # Si el cliente no existe
    if not cliente_data:
        return {"error": f"No existe el cliente con ID {cliente_id}"}

    # 3. Convertir el registro del cliente a un DataFrame de Pandas
    df_input = pd.DataFrame([cliente_data])
    
    # 4. PREDECIR DIRECTAMENTE
    # Como 'model' es un Pipeline, procesa las columnas y predice internamente
    prediccion = model.predict(df_input)[0]
    resultado_texto = "yes" if prediccion == 1 else "no"

    # 5. Retornar la respuesta final
    return {
        "cliente_id": cliente_id,
        "prediccion_deposito": resultado_texto,
        "mensaje": f"El modelo estima que el cliente {'sí' if resultado_texto == 'yes' else 'no'} aceptará el depósito."
    }
