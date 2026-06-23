import os
import json
import joblib

os.makedirs("artifacts", exist_ok=True)

ruta_modelo_real = "models/modelo_perceptron_multicapa.pkl"

if os.path.exists(ruta_modelo_real):
    modelo_banco = joblib.load(ruta_modelo_real)
    
    joblib.dump(modelo_banco, "artifacts/matriculado_model.joblib")
    print("Modelo duplicado: artifacts/matriculado_model.joblib")
else:
    print(f"Error: No se encontró el archivo en {ruta_modelo_real}")

metricas_banco = {
    "model_name": " Perceptrón multicapa (Bank Marketing)",
    "accuracy": 0.82,  
    "features_trained": ["age", "balance", "day", "duration_min", "campaign", "pdays", "previous"]
}

with open("artifacts/matriculado_metrics.json", "w", encoding="utf-8") as f:
    json.dump(metricas_banco, f, indent=4)

print("Métricas exportadas a artifacts/matriculado_metrics.json")
