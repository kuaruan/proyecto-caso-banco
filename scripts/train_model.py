import pandas as pd
import joblib
import os
import sys
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# 0. Cargar variables de entorno
load_dotenv()

# Configuración de conexión (Asegúrate de que coincidan con tu .env)
user = os.getenv('SUPABASE_DB_USER')
password = os.getenv('SUPABASE_DB_PASSWORD') or os.getenv('SUPABASE_DB_PASS')
host = os.getenv('SUPABASE_DB_HOST')
port = os.getenv('SUPABASE_DB_PORT', '5432')
dbname = os.getenv('SUPABASE_DB_NAME', 'postgres')

DB_URL = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
engine = create_engine(DB_URL)

def run_training():
    try:
        # 1. Conectar y traer datos
        print("--- Conectando a Supabase ---")
        # Intentamos con bank_marketing, si falla podrías cambiarlo a postulaciones_demo
        df = pd.read_sql("SELECT * FROM bank_marketing", engine)
        
        if df.empty:
            print("Error: La tabla está vacía.")
            return

        # 2. Limpieza de nombres de columnas
        # Esto elimina espacios en blanco o caracteres raros que causan el KeyError
        df.columns = df.columns.str.strip().str.lower()
        print(f"Columnas detectadas y limpias: {df.columns.tolist()}")

        # 3. Identificar la columna objetivo
        # Buscamos 'y' o la última columna si 'y' no existe exactamente
        target_col = 'deposit'
        print(f"Usando '{target_col}' como columna de predicción.")

        # 4. Preprocesamiento
        le = LabelEncoder()
        df[target_col] = le.fit_transform(df[target_col].astype(str))

        # Seleccionamos variables numéricas que existen en el dataset bank
        # Ajustado a las columnas estándar del dataset bank marketing
        features = ['age', 'balance', 'day', 'duration', 'campaign']
        
        # Validar que las features existan en el DF
        features_presentes = [f for f in features if f in df.columns]
        print(f"Entrenando con las variables: {features_presentes}")

        X = df[features_presentes]
        y = df[target_col]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 5. Entrenar el modelo
        print("Entrenando RandomForestClassifier...")
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # 6. Guardar el modelo
        os.makedirs('models', exist_ok=True)
        model_path = 'models/bank_model.pkl'
        joblib.dump(model, model_path)
        
        print(f"Éxito")
        print(f"Modelo guardado en: {os.path.abspath(model_path)}")
        print(f"Precisión en test: {model.score(X_test, y_test):.2f}")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    run_training()