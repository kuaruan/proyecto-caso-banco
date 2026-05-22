Proyecto de Predicción de Suscripción de Depósitos Bancarios 

Este proyecto utiliza una API construida con **FastAPI** para predecir si un cliente se suscribirá a un depósito
a plazo fijo, basándose en datos históricos de campañas de marketing bancario presentados en el caso de estudio: Bank Marketing.

Características del proyecto:
* **Modelo Predictivo:** Random Forest con un 76% de precisión
* **Base de Datos:** Integración en tiempo real con Supabase (PostgreSQL).
* **API:** Documentación interactiva con Swagger UI.
* **Procesamiento de Datos:** Limpieza y codificación de variables categóricas.

Tecnologías: 
* Python 3.10+
* **FastAPI** Framework de la API
* **Scikit-learn** Entrenamiento del modelo
* **Psycopg** Conector de base de datos
* **Joblib** Persistencia del modelo
* **Pandas** Análisis de datos
  
Instalación y Uso:
1. Clonar el repositorio
   En bash:
   git clone [https://github.com/kuaruan/proyecto-caso-banco.git](https://github.com/kuaruan/proyecto-caso-banco.git)
   cd proyecto-caso-banco

2. Configurar variables de entorno con credenciales de Supabase (.env.example)

3. Ejeructar API:
   En bash:
   uvicorn app.main:app --reload

 4. Documentación -> http://127.0.0.1:8000/docs
     GET /predict/{cliente_id}: Predicción por medio de consulta
     GET /suscripciones/estadisticas: Análisis descriptivo de la campaña de marketing
     GET /servicio: Lista de registros de la base de datos
   ------------------------------------------------------------------------------------------------
   Con Docker:
   En la cmd:
    docker build -t proyecto-caso-banco .
    
    docker run --env-file .env -p 8000:8000 proyecto-caso-banco
    
   En navegador:
    http://localhost:8000
    
    http://localhost:8000/health

   -------------------------------------------------------------------------------------------------
   Links:
   Render: https://dashboard.render.com/web/srv-d8855vl7vvec738fe21g
   Supabase: https://supabase.com/dashboard/project/fwmgjqsqacfhvjnbyofo/sql/654c4ef6-585c-4e8f-a759-c05c80bab3f5?schema=public
   Endpoints: http://localhost:8000/docs
