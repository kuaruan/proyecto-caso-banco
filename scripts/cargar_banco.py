import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# variables archivo .env
load_dotenv()

# Configuración de rutas y conexión
FILE_PATH = "data/datos_02_bank_validados.csv"
DB_URL = f"postgresql://{os.getenv('SUPABASE_DB_USER')}:{os.getenv('SUPABASE_DB_PASSWORD')}@{os.getenv('SUPABASE_DB_HOST')}:{os.getenv('SUPABASE_DB_PORT')}/{os.getenv('SUPABASE_DB_NAME')}"

try:
    print(f"--- Iniciando carga de: {FILE_PATH} ---")
    
    # Intentamos leer el CSV
    df = pd.read_csv(FILE_PATH, sep=",")
    
    print(f"Filas detectadas: {len(df)}")
    print("Conectando a Supabase...")
    
    engine = create_engine(DB_URL)
    
    # Cargar a la tabla de Supabase
    df.to_sql('bank_marketing', engine, if_exists='replace', index=False)
    
    print("Datos cargados en la nube.")

except Exception as e:
    print(f"Error: {e}")