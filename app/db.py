from dotenv import load_dotenv
import os
import psycopg
from psycopg.rows import dict_row

load_dotenv()

def get_connection_params():
    return {
        "host": os.getenv("SUPABASE_DB_HOST"),
        "port": os.getenv("SUPABASE_DB_PORT", "5432"),
        "dbname": os.getenv("SUPABASE_DB_NAME", "postgres"),
        "user": os.getenv("SUPABASE_DB_USER"),
        "password": os.getenv("SUPABASE_DB_PASSWORD"),
        "sslmode": "require",
    }

def test_connection():
    params = get_connection_params()
    missing = [k for k, v in params.items() if k != "sslmode" and not v]
    if missing:
        return {"status": "error", "detail": "Faltan variables: " + ", ".join(missing)}

    try:
        with psycopg.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()[0]
        return {"status": "ok", "detail": "Conexión exitosa", "db_version": version}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

def get_servicio(limit: int = 20):
    """Obtiene los registros con limpieza de tipos para evitar errores 422"""
    params = get_connection_params()
    with psycopg.connect(**params, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM public.bank_marketing LIMIT %s;', (limit,))
            rows = cur.fetchall()
            
            # Convertimos todo a tipos básicos de Python (int, float, str)
            clean_rows = []
            for row in rows:
                clean_row = {k: (int(v) if isinstance(v, (int, float)) else str(v)) 
                             for k, v in row.items()}
                clean_rows.append(clean_row)
            return clean_rows

def get_servicios_stats():
    """Obtiene estadísticas de las suscripciones (usando la columna 'deposit')"""
    params = get_connection_params()
    
    
    summary_query = '''
    SELECT 
    count(*) as total_registros,
    round(avg(age)::numeric, 2) as promedio_edad,
    count(*) FILTER (WHERE deposit = 1) as suscritos_si,
    count(*) FILTER (WHERE deposit = 0) as suscritos_no
    FROM public.bank_marketing;
    '''

    # Consulta por tipo de trabajo (job)
    job_query = '''
    SELECT job, count(*) as total
    FROM public.bank_marketing
    GROUP BY job
    ORDER BY total DESC;
    '''

    # Consulta por educación
    education_query = '''
    SELECT education, count(*) as total
    FROM public.bank_marketing
    GROUP BY education
    ORDER BY total DESC;
    '''

    with psycopg.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute(summary_query)
            summary = cur.fetchone()

            cur.execute(job_query)
            job_rows = cur.fetchall()

            cur.execute(education_query)
            education_rows = cur.fetchall()

    # Manejo de nulos por si la tabla está vacía
    total_clientes = int(summary[0]) if summary[0] else 0
    promedio_edad = float(summary[1]) if summary[1] else 0.0
    si = int(summary[2]) if summary[2] else 0
    no = int(summary[3]) if summary[3] else 0

    return {
        "total_clientes": total_clientes,
        "promedio_edad": promedio_edad,
        "tasa_suscripcion": {
            "si": si,
            "no": no
        },
        "por_trabajo": [{"trabajo": row[0], "total": int(row[1])} for row in job_rows],
        "por_educacion": [{"nivel": row[0], "total": int(row[1])} for row in education_rows]
    }